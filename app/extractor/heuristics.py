# app/extractor/heuristics.py
import re

"""
Heurísticas otimizadas para diferentes layouts de documentos:
- OAB (carteiras de advogados)
- Telas de sistema bancário / relatórios administrativos
- Qualquer PDF com texto OCR limpo
"""

def extract_field_via_heuristics(words, full_text, field_name, description):
    text = full_text.upper().replace("\n", " ").replace("\r", " ")

    # --- CAMPOS DE IDENTIFICAÇÃO PESSOAL ---
    if field_name.lower() in ["cpf", "cpf_cnpj"]:
        match = re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", text)
        if match:
            return match.group(), 0.98, "regex"
        match = re.search(r"\b\d{11}\b", text)
        if match:
            return match.group(), 0.95, "regex"

    if field_name.lower() in ["nome", "nome_completo", "cliente"]:
        # Padrão OAB (nome antes de INSCRIÇÃO)
        m = re.search(r"([A-ZÁÉÍÓÚÂÊÔÃÕÇ'\s]{3,})\s+INSCRIÇÃO", text)
        if m:
            return m.group(1).strip(), 0.9, "pattern"
        # Padrão telas de sistema (NOME: ou após 'Cliente')
        m = re.search(r"(CLIENTE|NOME)\s*[:\-]?\s*([A-Z\s]+)", text)
        if m:
            return m.group(2).strip(), 0.85, "regex"

    # --- CAMPOS JURÍDICOS / OAB ---
    if field_name.lower() == "inscricao":
        m = re.search(r"\bINSCRIÇÃO\s*[:\-]?\s*(\d{3,10})\b", text)
        if m:
            return m.group(1), 0.95, "regex"

    if field_name.lower() == "seccional":
        m = re.search(r"SECCIONAL\s*[:\-]?\s*([A-Z]{2})\b", text)
        if m:
            return m.group(1), 0.8, "regex"

    if field_name.lower() == "subsecao":
        m = re.search(r"SUBSEÇÃO\s*[:\-]?\s*([A-ZÀ-Ú\s\-]+)", text)
        if m:
            return m.group(1).strip(), 0.85, "regex"
        m = re.search(r"CONSELHO SECCIONAL\s*-\s*([A-ZÀ-Ú\s]+)", text)
        if m:
            return "CONSELHO SECCIONAL - " + m.group(1).strip(), 0.85, "pattern"

    if field_name.lower() == "categoria":
        for cat in ["ADVOGADO", "ADVOGADA", "SUPLEMENTAR", "ESTAGIARIO", "ESTAGIÁRIA"]:
            if cat in text:
                return cat, 0.9, "keyword"

    if field_name.lower() == "situacao":
        m = re.search(r"SITUAÇÃO\s*[:\-]?\s*([A-Z\s]+)", text)
        if m:
            return m.group(1).strip(), 0.9, "regex"

    if field_name.lower() in ["endereco_profissional", "endereco"]:
        m = re.search(r"ENDEREÇO\s*(PROFISSIONAL)?[:\-]?\s*(.*?)\s+(TELEFONE|CEP|SITUAÇÃO)", text)
        if m:
            return m.group(2).strip(), 0.9, "pattern"

    # --- CAMPOS FINANCEIROS (TELAS SISTEMA) ---
    if field_name.lower() in ["sistema", "tipo_sistema"]:
        m = re.search(r"SISTEMA\s*[:\-]?\s*([A-Z]+)", text)
        if m:
            return m.group(1).strip(), 0.9, "regex"

    if field_name.lower() in ["valor_total", "saldo", "total", "saldo_geral"]:
        m = re.search(r"TOTAL\s*[:\-]?\s*([\d\.,]+)", text)
        if m:
            return m.group(1).strip(), 0.9, "regex"
        m = re.search(r"R\$\s*([\d\.,]+)", text)
        if m:
            return m.group(1).strip(), 0.9, "regex"

    if field_name.lower() in ["cidade", "uf", "cep"]:
        m = re.search(r"CIDADE[:\-]?\s*([A-ZÀ-Ú\s]+)", text)
        if m:
            return m.group(1).strip(), 0.85, "regex"
        m = re.search(r"U\.?F\.?\s*[:\-]?\s*([A-Z]{2})\b", text)
        if m:
            return m.group(1).strip(), 0.85, "regex"
        m = re.search(r"CEP[:\-]?\s*(\d{5}-?\d{3})", text)
        if m:
            return m.group(1), 0.9, "regex"

    if field_name.lower() in ["status", "status_juridico", "status_notificacao"]:
        m = re.search(r"STATUS\s*(JURÍDICO|NOTIFICAÇÃO)?[:\-]?\s*([A-Z\s]+)", text)
        if m:
            return m.group(2).strip(), 0.85, "regex"

    if field_name.lower() in ["telefone", "telefone_profissional"]:
        m = re.search(r"(\(?\d{2,3}\)?\s?\d{4,5}-?\d{4})", text)
        if m:
            return m.group(1), 0.9, "regex"

    # --- CAMPOS GENÉRICOS ---
    # Busca genérica baseada em label e proximidade textual
    snippet = find_near_label(text, field_name)
    if snippet:
        return snippet, 0.7, "label-context"

    return None, 0.0, None


def find_near_label(text, field_name):
    """
    Busca genérica por valor próximo ao nome do campo (label textual).
    Exemplo: 'Cliente: João Silva' → retorna 'João Silva'
    """
    try:
        pattern = re.compile(rf"{field_name.upper()}[:\-]?\s*([A-Z0-9\s,./º°ª\-]+)", re.IGNORECASE)
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
    except:
        pass
    return None
