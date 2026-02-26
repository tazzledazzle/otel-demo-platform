# LangChain Tutorial

Hands-on LangChain for software engineers: chains, agents, and LLM integrations.

## Prerequisites

- **Python 3.10+**
- `pip install -r requirements.txt`

### Ollama (default)

1. Install [Ollama](https://ollama.com).
2. Pull the model used by the script: `ollama pull llama3.1`

No API key required.

### OpenAI (optional)

- `pip install langchain-openai`
- Set `OPENAI_API_KEY` in your environment or `.env`.

## Run

```bash
python 01_hello_chain.py
```

You should see a short LLM reply printed to the terminal.
