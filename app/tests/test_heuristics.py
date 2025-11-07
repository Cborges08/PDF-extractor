# app/tests/test_heuristics.py
from app.extractor.heuristics import extract_field_via_heuristics

def test_extract_cpf_regex():
    text = "Nome: Caio\nCPF: 123.456.789-10\nEndereço: Rua Teste"
    words = [{"text": t, "x0": 0, "y0": 0, "x1": 0, "y1": 0, "page": 1} for t in text.split()]
    value, conf, method = extract_field_via_heuristics(words, text, "cpf", "")
    assert value == "123.456.789-10"
    assert conf > 0.9
    assert method == "regex"
