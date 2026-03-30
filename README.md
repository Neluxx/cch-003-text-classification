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
│       ├── classify_document_type.txt   # Stage 1: email vs. scientific article
│       └── classify_email_type.txt      # Stage 2: support vs. complaint
└── test_files/
    ├── email_support.txt
    ├── email_complaint.txt
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

For an **e-mail**, classification runs in two stages. Stage 1 identifies the document type; stage 2 determines whether it is a support case or a complaint:

```
────────────────────────────────────────────────────────────
  Model      : qwen2.5:3b
  File       : test_files/email_support.txt
  Type       : E-Mail
  Confidence : HIGH
  Reasoning  : The text contains typical e-mail headers (From, To, Subject)
               and a personal support request.
  ────────────────────────────────────────────────────────
  E-Mail Type: Support
  Confidence : HIGH
  Reasoning  : The sender is asking for help resolving a technical issue.
────────────────────────────────────────────────────────────
```

For a **scientific article**, only stage 1 runs:

```
────────────────────────────────────────────────────────────
  Model      : qwen2.5:3b
  File       : test_files/scientific_article.txt
  Type       : Scientific Article
  Confidence : HIGH
  Reasoning  : The text follows the structure of a peer-reviewed research paper.
────────────────────────────────────────────────────────────
```

---

## Classification logic

Classification is performed in up to two stages:

| Stage | Input          | Output                              |
|-------|----------------|-------------------------------------|
| 1     | Any document   | `email` or `scientific_article`     |
| 2     | E-mails only   | `support` or `complaint`            |

Stage 2 is only triggered when stage 1 identifies the document as an e-mail.

---

## Configuration

The default model is `qwen2.5:3b`. Change it per-run with `--model <name>` or
edit `DEFAULT_MODEL` in `src/classifier.py`.