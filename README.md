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
│   ├── prompt.txt       # Prompt for Ollama
│   ├── classifier.py    # Core classification logic
│   ├── formatting.py    # Output and error formatting
│   └── constants.py     # Color codes and labels
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

For an **e-mail**, the classification identifies the document type, determines
whether it is a support case or a complaint, and classifies the sender's mood:

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

For a **scientific article**, the classification returns the primary subject area:

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

Every document is classified using a unified prompt.
The model always returns the document type plus the sub-classifications
relevant to that type (fields for the inactive branch are returned as `null`).

| Dimension       | Applies to           | Possible values                                                                                                                   |
|-----------------|----------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| Document type   | Any document         | `email` or `scientific_article`                                                                                                   |
| E-mail type     | E-mails only         | `support` or `complaint`                                                                                                          |
| Mood            | E-mails only         | `neutral`, `friendly`, or `angry`                                                                                                 |
| Article topic   | Scientific articles  | `computer_science`, `medicine`, `biology`, `physics`, `chemistry`, `environmental_science`, `economics`, `psychology`, or `other` |

---

## Configuration

The default model is `qwen2.5:3b`. Change it per-run with `--model <name>` or
edit `DEFAULT_MODEL` in `src/classifier.py`.