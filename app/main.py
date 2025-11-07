# app/main.py
from fastapi import FastAPI, File, UploadFile, Form
import json
from app.extractor.pipeline import extract_from_pdf

app = FastAPI(title="PDF Extractor Service", version="0.2.0")

@app.post("/extract")
async def extract(label: str = Form(...), extraction_schema: str = Form(...), pdf: UploadFile = File(...)):
    schema = json.loads(extraction_schema)
    pdf_bytes = await pdf.read()
    result = extract_from_pdf(label, schema, pdf_bytes)
    return result

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # porta do Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)