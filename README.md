# CCH-003: Text Classification Tool

A CLI tool that classifies text files using a local LLM via Ollama.

---

## Requirements

- [Python](https://www.python.org/) 3.14+
- [uv](https://docs.astral.sh/uv/) (package manager)
- [Ollama](https://ollama.com) running locally (`ollama serve`)
- A pulled model, e.g. `ollama pull qwen2.5:3b`

---

## Setup

### 1. Create virtual environment and install dependencies

```powershell
uv sync
```

### 2. Activate the virtual environment

```powershell
# Windows (PowerShell)
.\.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

> You need to activate the virtual environment once per terminal session before using the classifier.

---

## Project structure

```
cch-003-text-classification/
├── main.py              # CLI entry point
├── src/
│   ├── classifier.py    # Core classification logic
│   ├── formatting.py    # Colored output and error formatting
│   └── prompts/
│       └── classify_document_type.txt
└── test_files/
    ├── email_support.txt
    └── scientific_article.txt
```

---

## Usage

```bash
# Classify a single file
python main.py test_files/email_support.txt

# Classify multiple files at once
python main.py test_files/email_support.txt test_files/scientific_article.txt

# Use a different Ollama model
python main.py test_files/email_support.txt --model llama3.2:3b
```

### Example output

```
────────────────────────────────────────────────────────────
  Model      : qwen2.5:3b
  File       : test_files/email_support.txt
  Type       : E-Mail
  Confidence : HIGH
  Reasoning  : The text contains typical e-mail headers (From, To, Subject)
               and a personal support request.
────────────────────────────────────────────────────────────
```

---

## Configuration

The default model is `qwen2.5:3b`. Change it per-run with `--model <name>` or
edit `DEFAULT_MODEL` in `src/classifier.py`.
