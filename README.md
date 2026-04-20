# Python GenAI + Agentic AI (Learning Repo)

This repo is my hands-on notebook while learning **Python Generative AI** and **Agentic AI** using open-source tools and APIs.

## What you'll learn here

- Prompting basics: zero-shot, few-shot, personas, chain-of-thought style prompting
- Tokenization: encode/decode experiments
- Structured outputs: using **Pydantic**
- RAG (Retrieval-Augmented Generation): PDF -> chunks -> embeddings -> vector DB -> answer with context
- Simple agents: tool-using "weather agent"
- Serving: basic **FastAPI** examples

## Repo structure

- `GenAi/` - prompting + tokenization examples (OpenAI SDK used with a Gemini OpenAI-compatible endpoint)
- `AgenticAi/` - basic agents + LangChain RAG with Qdrant
- `FastApi_setup/` - FastAPI + Pydantic basics (plus a simple Hugging Face router example)
- `Pydantic/` - small Pydantic examples
- `Data Type/` - Python mutable vs immutable examples

## Prerequisites

- Python 3.10+ (recommended: 3.11+)
- (Optional, for RAG) Docker Desktop / Docker Engine
- API keys (kept in `.env`, never commit secrets)

## Environment variables

Create a `.env` file inside the folder you're running from (example: `GenAi/.env` or `AgenticAi/.env`).

- `GEMINI_API_KEY` - used by scripts in `GenAi/` with `base_url="https://generativelanguage.googleapis.com/v1beta/openai/"`
- `HF_TOKEN` - used by scripts in `AgenticAi/` and `FastApi_setup/` with `base_url="https://router.huggingface.co/v1"`

## Quickstart (Windows / PowerShell)

From the repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install dependencies per module (pick what you want to run):

```powershell
pip install -r GenAi\requirements.txt
pip install -r AgenticAi\requirement.txt
pip install -r FastApi_setup\requirement.txt
```

Run examples:

```powershell
python GenAi\main.py
python GenAi\ZeroShotPrompt.py
python GenAi\FewShotPrompt.py
```

## RAG (LangChain + Qdrant)

1) Start Qdrant:

```powershell
cd AgenticAi
docker compose up -d
```

2) Index the PDF (`AgenticAi/SystemDesign.pdf`) into Qdrant:

```powershell
python .\LangChain_RAG.py
```

3) Chat using similarity search + retrieved context:

```powershell
python .\chatLangChainRAG.py
```

## Agents

- Weather tool agent: `AgenticAi/WeatherAgent.py`
- Advanced weather agent: `AgenticAi/WeatherAgentAdvance.py`

## FastAPI

Run the server (example):

```powershell
cd FastApi_setup
uvicorn server:app --reload
```

Then open:
- `GET /` -> hello world
- `POST /details` -> Pydantic-validated request body

## Learning checklist (suggested order)

1) `GenAi/` - prompts + roles + basic chat completions
2) `Pydantic/` - understand schemas + validation
3) `FastApi_setup/` - build a small API around models
4) `AgenticAi/WeatherAgent.py` - tool calling + step-by-step outputs
5) `AgenticAi/LangChain_RAG.py` + `chatLangChainRAG.py` - RAG end-to-end

## Notes

- Keep secrets in `.env`. The repo ignores `.env` by default via `.gitignore`.
- If something fails, verify:
  - your API key exists in the correct folder's `.env`
  - Qdrant is running on `http://localhost:6333`
  - you installed the correct requirements file for that module

## Contributing

This is a personal learning repo, but PRs are welcome for:
- small fixes (typos, broken commands)
- improved docs
- new learning examples (small + focused)

## License

Add a license if you plan to publish this publicly (MIT is a common choice for learning repos).
