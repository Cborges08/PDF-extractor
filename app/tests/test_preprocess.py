# app/tests/test_preprocess.py
from app.extractor.preprocess import extract_words_with_boxes

def test_extract_words_with_boxes():
    # PDF mínimo de teste
    pdf_path = "app/tests/sample.pdf"

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    words, full_text = extract_words_with_boxes(pdf_bytes)

    assert isinstance(words, list)
    assert isinstance(full_text, str)
    assert len(full_text) > 0
