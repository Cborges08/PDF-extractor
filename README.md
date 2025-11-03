# PDF Extractor Service

Pipeline híbrido (heurística + LLM) para extração de dados estruturados de PDFs.

## Como rodar localmente

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
