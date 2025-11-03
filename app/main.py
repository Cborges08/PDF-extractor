from fastapi import FastAPI, File, UploadFile, Form
import json

app = FastAPI(title="PDF Extractor Service", version="0.1.0")

@app.post("/extract")
async def extract(label: str = Form(...), extraction_schema: str = Form(...), pdf: UploadFile = File(...)):
    # placeholder até implementarmos o pipeline
    schema = json.loads(extraction_schema)
    content = await pdf.read()
    return {
        "label": label,
        "schema": schema,
        "pdf_size_bytes": len(content)
    }
