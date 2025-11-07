```markdown
# 🧠 Enter Extract AI
**Extração Inteligente de Dados de Documentos PDF com IA**

> Plataforma completa que realiza **extração de dados estruturados** a partir de PDFs utilizando heurísticas otimizadas e fallback com modelo LLM (`gpt-5-mini`).

---

## 🚀 Visão Geral

O **Enter Extract AI** é uma aplicação composta por:
- **Backend (FastAPI + Python)**: responsável pelo pipeline de extração.
- **Frontend (React + Vite + Tailwind)**: interface moderna e interativa para upload de PDFs e visualização dos resultados.

O sistema foi projetado para ser:
- ⚡ **Rápido** — cache local e heurísticas para reduzir chamadas ao modelo LLM.
- 💸 **Eficiente** — uso mínimo de IA quando as heurísticas têm alta confiança.
- 🔒 **Confiável** — arquitetura modular, testável e extensível.

---

## 🧩 Arquitetura

```

pdf-extractor/
├── app/
│   ├── extractor/
│   │   ├── cache.py
│   │   ├── heuristics.py
│   │   ├── llm.py
│   │   ├── pipeline.py
│   │   └── preprocess.py
│   ├── tests/
│   │   ├── test_heuristics.py
│   │   ├── test_llm.py
│   │   ├── test_pipeline.py
│   │   └── test_preprocess.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   │   └── favicon.png
│   └── index.html
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md

````

---

## ⚙️ Funcionalidades Principais

### 🧾 Extração de Dados
- Leitura de PDFs via **OCR e PyMuPDF**
- Pré-processamento com bounding boxes (`extract_words_with_boxes`)
- Extração por **heurísticas** (regex, padrões, palavras-chave)
- Fallback automático via **LLM (gpt-5-mini)**

### 🧠 Inteligência Híbrida
- **Heurística** → Rápida e barata  
- **LLM Fallback** → Garantia de precisão

### 📊 Métricas em Tempo Real
Cada requisição gera métricas como:
```json
{
  "elapsed_sec": 32.9,
  "metrics": {
    "heuristics": {"count": 7, "avg": 0.0001},
    "llm": {"count": 6, "avg": 5.46},
    "latency_total": {"avg": 32.9}
  }
}
````

### 💾 Cache Inteligente

* Armazena respostas anteriores com hash SHA-256 do conteúdo.
* Reduz tempo de resposta e custo de API.

---

## 🧰 Tecnologias

### Backend

* [FastAPI](https://fastapi.tiangolo.com/)
* [PyMuPDF](https://pymupdf.readthedocs.io/)
* [Cachetools](https://pypi.org/project/cachetools/)
* [OpenAI API](https://platform.openai.com/)
* [Pytest](https://docs.pytest.org/)

### Frontend

* [React 18 + TypeScript](https://react.dev/)
* [Vite](https://vitejs.dev/)
* [TailwindCSS](https://tailwindcss.com/)
* [React Query](https://tanstack.com/query/latest)
* [Lucide Icons](https://lucide.dev/)

---

## 🧑‍💻 Instalação

### 🔹 Backend (FastAPI)

```bash
# 1. Clonar o repositório
git clone https://github.com/seuusuario/pdf-extractor.git
cd pdf-extractor

# 2. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # (Linux/Mac)
# ou no Windows:
# .venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar servidor FastAPI
uvicorn app.main:app --reload --port 8000
```

A API estará disponível em:

> [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 🔹 Frontend (Vite + React)

```bash
cd frontend
npm install
npm run dev
```

A interface abrirá em:

> [http://localhost:8080](http://localhost:8080)

---

## 🧩 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com:

```bash
OPENAI_API_KEY=sk-xxxxxx
```

---

## 🧪 Testes

Executar todos os testes automatizados:

```bash
pytest -v
```

Exemplo de saída:

```
============================= test session starts ==============================
platform darwin -- Python 3.11
collected 4 items

test_heuristics.py::test_extract_cpf_regex PASSED
test_llm.py::test_llm_function_signature PASSED
test_pipeline.py::test_end_to_end PASSED
test_preprocess.py::test_extract_words_with_boxes PASSED
======================== 4 passed, 0 warnings in 1.12s =========================
```

---

## 🧱 Estrutura do Pipeline

```mermaid
flowchart LR
A[PDF Upload] --> B[Preprocess - OCR + Tokens]
B --> C[Heuristics - Regex / Pattern]
C -->|Confidence < 0.6| D[LLM (GPT-5-mini)]
C -->|Confidence >= 0.6| E[Cache Store]
D --> E[Cache Store]
E --> F[Response + Metrics]
```

---

## 🪄 Exemplo de Requisição

### POST `/extract`

**Request:**

```bash
curl -X POST "http://127.0.0.1:8000/extract" \
-F "label=oab" \
-F "extraction_schema={
  \"nome\": \"Nome completo do profissional\",
  \"inscricao\": \"Número de inscrição\"
}" \
-F "pdf=@oab_1.pdf"
```

**Response:**

```json
{
  "label": "oab",
  "data": {
    "nome": "JOANA D'ARC",
    "inscricao": "101943",
    "situacao": "REGULAR"
  },
  "meta": {
    "nome": {"confidence": 0.9, "method": "pattern"},
    "inscricao": {"confidence": 0.9, "method": "gpt-5-mini"}
  },
  "elapsed_sec": 32.9
}
```

---

## 🎨 Interface

* Upload de PDF
* Edição do schema JSON
* Exibição de resultado estruturado
* Spinner de carregamento e alertas interativos

---

## 🧠 Autor

**Caio Fernandes**
Desenvolvedor de Software • Inteligência Artificial & Backend
📧 contato: caiofeborges@gmail.com
🌐 GitHub: [github.com/Cborges08](https://github.com/Cborges08)

---

