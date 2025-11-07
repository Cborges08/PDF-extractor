# app/extractor/llm.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def llm_extract_field(field_name: str, description: str, words: list, full_text: str):
    """
    Extração de campos via modelo GPT (atualmente gpt-5-mini).
    Retorna o valor textual do campo ou None em caso de erro.
    """

    prompt = f"""
    Extraia o campo '{field_name}' a partir do texto abaixo.
    Descrição do campo: {description}

    Texto:
    {full_text}

    Retorne apenas o valor extraído, sem explicações ou formatação adicional.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",  # seu modelo alvo
            messages=[
                {"role": "system", "content": "Você é um extrator de dados estruturados de PDFs."},
                {"role": "user", "content": prompt},
            ],
        )

        content = response.choices[0].message.content.strip()
        print(f"[LLM SUCCESS] {field_name}: {content}")
        return content

    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return None
