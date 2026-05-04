# Legal AI Hub

A multi-feature AI-powered legal assistant built with **Streamlit**, **LangChain**, and **ChromaDB**. It provides a unified interface for several legal document analysis workflows.

## Features

| Tool | Description |
|------|-------------|
| **Contract Q&A** | Upload a contract and ask questions against it using RAG |
| **Policies Q&A** | Query internal policy documents |
| **Contract Risk** | Identify risky clauses in contracts |
| **Litigation Support** | Assist with litigation research and document review |
| **Compliance** | Check documents against compliance requirements |

## Project Structure

```
LegalAI/
├── streamlit_app.py          # Streamlit entry point
├── requirements.txt
├── src/
│   ├── core/                 # Shared utilities
│   │   ├── config.py         # Environment & directory setup
│   │   ├── embeddings.py     # Embedding model wrappers
│   │   ├── vectordb.py       # ChromaDB helpers
│   │   ├── chunking.py       # Text splitting strategies
│   │   ├── retrievers.py     # Retriever factories (dense + BM25)
│   │   ├── llm.py            # LLM wrappers (Groq)
│   │   ├── loaders.py        # PDF / CSV document loaders
│   │   ├── schemas.py        # Pydantic models
│   │   └── ui.py             # Shared Streamlit UI components
│   └── features/             # One folder per feature
│       ├── contract_qna/
│       ├── policies_qna/
│       ├── litigation/
│       └── ...
└── data/                     # Runtime data (gitignored)
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/YashPadhye/LegalAI.git
cd LegalAI
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the app

```bash
streamlit run streamlit_app.py
```

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [LangChain](https://www.langchain.com/) — LLM orchestration & RAG pipelines
- [ChromaDB](https://www.trychroma.com/) — Local vector store
- [Sentence Transformers](https://www.sbert.net/) — Embeddings
- [Groq](https://groq.com/) — Fast LLM inference
- [Pydantic v2](https://docs.pydantic.dev/) — Data validation
