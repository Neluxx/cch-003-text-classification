# CCH-003: Text Classification Tool

A CLI tool that classifies text files using a local LLM via Ollama.

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally (`ollama serve`)
- A pulled model, e.g. `ollama pull qwen2.5:3b`

---

## Usage

```bash
# Classify a single file
python main.py test_files/email_support.txt

# Classify multiple files at once
python main.py test_files/email_support.txt test_files/scientific_article.txt
```

### Example output

```
  File       : test_files/email_support.txt
  Type       : email
  Confidence : high
  Reasoning  : The text contains typical e-mail headers (From, To, Subject)
               and a personal support request.
```

---

## Configuration

Ollama is expected at `http://localhost:11434`.  
To use a remote instance, change `OLLAMA_BASE_URL` in `src/classifier.py`.