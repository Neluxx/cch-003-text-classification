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
│       ├── classify_email_type.txt      # Stage 2a: support vs. complaint
│       ├── classify_email_mood.txt      # Stage 3: mood of the email sender
│       └── classify_article_topic.txt   # Stage 2b: topic area of the article
└── test_files/
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

For an **e-mail**, classification runs in three stages. Stage 1 identifies the
document type, stage 2 determines whether it is a support case or a complaint,
and stage 3 classifies the sender's mood:

```
────────────────────────────────────────────────────────────
  Model      : qwen2.5:3b
  File       : test_files/email_complaint_damaged_product.txt
  Type       : E-Mail
  Confidence : HIGH
  Reasoning  : The text is structured as an e-mail with headers and a message body.
  ────────────────────────────────────────────────────────
  E-Mail Type: Complaint
  Confidence : HIGH
  Reasoning  : The sender reports a damaged product and demands a replacement.
  ────────────────────────────────────────────────────────
  Mood       : Angry
  Confidence : HIGH
  Reasoning  : The sender uses strong language and threatens further action.
────────────────────────────────────────────────────────────
```

For a **scientific article**, stage 2 determines the primary subject area:

```
────────────────────────────────────────────────────────────
  Model      : qwen2.5:3b
  File       : test_files/scientific_article_crispr_scd.txt
  Type       : Scientific Article
  Confidence : HIGH
  Reasoning  : The text follows the structure of a peer-reviewed research paper.
  ────────────────────────────────────────────────────────
  Topic      : Medicine
  Confidence : HIGH
  Reasoning  : The paper reports a clinical trial for a genetic blood disorder.
────────────────────────────────────────────────────────────
```

---

## Classification logic

E-mails are classified in three stages; scientific articles in two:

| Stage | Trigger              | Output                                                                                                                            |
|-------|----------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| 1     | Any document         | `email` or `scientific_article`                                                                                                   |
| 2a    | E-mails only         | `support` or `complaint`                                                                                                          |
| 2b    | Scientific articles  | `computer_science`, `medicine`, `biology`, `physics`, `chemistry`, `environmental_science`, `economics`, `psychology`, or `other` |
| 3     | E-mails only         | `neutral`, `friendly`, or `angry`                                                                                                 |

---

## Configuration

The default model is `qwen2.5:3b`. Change it per-run with `--model <name>` or
edit `DEFAULT_MODEL` in `src/classifier.py`.