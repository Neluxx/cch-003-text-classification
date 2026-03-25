import json
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:3b"


@dataclass
class ClassificationResult:
    document_type: str
    confidence: str
    reasoning: str
    raw_file: str


def _call_ollama(prompt: str) -> str:
    """Send a prompt to the local Ollama instance and return the response text."""
    payload = json.dumps({
        "model": DEFAULT_MODEL,
        "prompt": prompt,
        "stream": False,
    }).encode("utf-8")

    request = urllib.request.Request(
        f"{OLLAMA_BASE_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
            return body.get("response", "").strip()
    except urllib.error.URLError as exc:
        raise ConnectionError(
            f"Could not reach Ollama at {OLLAMA_BASE_URL}. "
            "Make sure Ollama is running (`ollama serve`)."
        ) from exc


def _build_prompt(text: str) -> str:
    template = (PROMPTS_DIR / "classify_document_type.txt").read_text(encoding="utf-8")
    return template.replace("{text}", text[:4000])


def _classify_text(text: str) -> ClassificationResult:
    """Classify the provided text using a local Ollama LLM."""
    raw_response = _call_ollama(_build_prompt(text))

    try:
        data = json.loads(raw_response)
        return ClassificationResult(
            document_type=data.get("document_type", "unknown"),
            confidence=data.get("confidence", "low"),
            reasoning=data.get("reasoning", ""),
            raw_file="",
        )
    except (json.JSONDecodeError, KeyError):
        return ClassificationResult(
            document_type="unknown",
            confidence="low",
            reasoning=f"Could not parse LLM response: {raw_response}",
            raw_file="",
        )


def classify_file(path: str) -> ClassificationResult:
    """Read a file and classify its content."""
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    result = _classify_text(text)
    result.raw_file = path
    return result
