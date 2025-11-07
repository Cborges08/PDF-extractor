# app/extractor/preprocess.py
import fitz  # PyMuPDF

def extract_words_with_boxes(pdf_bytes: bytes):
    """
    Lê o PDF a partir de bytes e retorna:
    - words: lista de dicionários com texto e bounding box
    - full_text: todo o texto concatenado
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    words = []
    full_text = []

    for page_number, page in enumerate(doc, start=1):
        text = page.get_text("text")
        full_text.append(text)

        # Extrai cada palavra com bounding box
        for (x0, y0, x1, y1, word, block_no, line_no, word_no) in page.get_text("words"):
            words.append({
                "page": page_number,
                "text": word,
                "x0": x0,
                "y0": y0,
                "x1": x1,
                "y1": y1,
            })

    full_text = "\n".join(full_text)
    return words, full_text
