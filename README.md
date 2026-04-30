
# pharm-agent

## Gemini Gradio app (uses `google-genai` SDK)

This project provides a small Gradio chat UI that calls the Google Generative API using the `google-genai` Python SDK (`from google import genai`). The app reads `GEMINI_API_KEY` and `GEMINI_MODEL` from the environment and initializes a `genai.Client(api_key=...)` in non-Vertex mode.

Prerequisites:

- Python 3.9+
- The dependencies are listed in `pyproject.toml` (includes `google-genai`, `gradio`, `python-dotenv`). You can install them directly:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
# or install the core runtime packages directly:
pip install google-genai gradio python-dotenv
```

Environment:

- `GEMINI_API_KEY`: your API key or bearer token for the Generative API
- `GEMINI_MODEL`: the model id to use (e.g. `gemini-3-flash-preview`, `gemini-3-bison`)

Run:

```bash
export GEMINI_API_KEY="YOUR_KEY"
export GEMINI_MODEL="gemini-3-flash-preview"
python app.py
```

Open http://localhost:7860 in your browser.

Notes:

- The app uses `genai.Client(api_key=...)` and expects the SDK available as `google-genai` (see `pyproject.toml`).
- For local development you can keep credentials in a `.env` file and `python-dotenv` will load them. Do not commit `.env` to version control.

