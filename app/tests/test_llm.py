# app/tests/test_llm.py
from app.extractor.llm import llm_extract_field

def test_llm_function_signature():
    # Não chama o modelo real, apenas garante que a função executa sem crash
    result = llm_extract_field("nome", "Nome completo do cliente", [], "Texto de teste simples.")
    assert result is None or isinstance(result, str)
