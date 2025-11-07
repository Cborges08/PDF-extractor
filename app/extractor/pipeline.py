# app/extractor/pipeline.py
from dotenv import load_dotenv
load_dotenv()
import hashlib
import json
import time
from app.extractor.preprocess import extract_words_with_boxes
from app.extractor.heuristics import extract_field_via_heuristics
from app.extractor.llm import llm_extract_field
from app.extractor.cache import SessionCache
from app.extractor.metrics import metrics

# Cache local por sessão
cache = SessionCache(maxsize=512)


def extract_from_pdf(label: str, schema: dict, pdf_bytes: bytes):
    start_total = time.time()

    metrics.start("preprocess")
    words, full_text = extract_words_with_boxes(pdf_bytes)
    metrics.stop("preprocess")

    text_hash = hashlib.sha256(full_text.encode()).hexdigest()
    cache_key = (text_hash, label, json.dumps(schema, sort_keys=True))

    if cache.exists(cache_key):
        metrics.record("cache_hit", 1)
        print("[CACHE] Reusing previous result")
        return cache.get(cache_key)

    output = {}
    meta = {}

    for field_name, description in schema.items():
        metrics.start("heuristics")
        value, confidence, method = extract_field_via_heuristics(words, full_text, field_name, description)
        metrics.stop("heuristics")

        # --- OTIMIZAÇÃO DE LLM ---
        # Se a heurística encontrou algo com confiança >= 0.75, não usa LLM
        if value and confidence >= 0.75:
            print(f"[FAST] {field_name}: {value} ({method}, conf={confidence})")
            output[field_name] = value
            meta[field_name] = {"confidence": confidence, "method": method}
            continue

        # --- FALLBACK: LLM ---
        print(f"[LLM USED] {field_name} (fallback)")
        metrics.start("llm")
        value_llm = llm_extract_field(field_name, description, words, full_text)
        metrics.stop("llm")

        if value_llm:
            value = value_llm
            confidence = 0.9
            method = "gpt-5-mini"
        else:
            value = None
            confidence = 0.0
            method = "none"

        output[field_name] = value
        meta[field_name] = {"confidence": confidence, "method": method}

    elapsed = round(time.time() - start_total, 2)
    metrics.record("requests_total", 1)
    metrics.record("latency_total", elapsed)

    response = {
        "label": label,
        "data": output,
        "meta": meta,
        "elapsed_sec": elapsed,
        "metrics": metrics.summary(),
    }

    cache.set(cache_key, response)
    print(f"[DONE] Processed '{label}' in {elapsed}s\n")
    return response
