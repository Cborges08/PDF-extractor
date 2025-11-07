# app/tests/test_pipeline.py
from app.extractor.pipeline import extract_from_pdf

def test_pipeline_basic():
    schema = {"cpf": "Número de CPF do cliente"}
    pdf_path = "app/tests/sample.pdf"

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    result = extract_from_pdf("test", schema, pdf_bytes)

    assert "data" in result
    assert "cpf" in result["data"]
    assert "meta" in result
    assert "elapsed_sec" in result
