import json
from dataclasses import dataclass
from pathlib import Path

import ollama

DEFAULT_MODEL = "qwen2.5:3b"
PROMPTS_DIR = Path(__file__).parent / "prompts"


@dataclass
class ClassificationResult:
    document_type: str
    confidence: str
    reasoning: str
    raw_file: str
    model: str


class Classifier:
    def _call_ollama(self, prompt: str, model: str = DEFAULT_MODEL) -> str:
        """Send a prompt to the local Ollama instance and return the response text."""
        try:
            response = ollama.generate(model=model, prompt=prompt)
            return response.response.strip()
        except ollama.ResponseError as exc:
            raise ConnectionError(f"Ollama error: {exc}") from exc
        except Exception as exc:
            raise ConnectionError(f"Could not reach Ollama. Is it running?") from exc

    def _build_prompt(self, text: str) -> str:
        template = (PROMPTS_DIR / "classify_document_type.txt").read_text(encoding="utf-8")
        return template.replace("{text}", text[:4000])

    def _classify_text(self, text: str, model: str = DEFAULT_MODEL) -> ClassificationResult:
        """Classify the provided text using a local Ollama LLM."""
        prompt = self._build_prompt(text)
        raw_response = self._call_ollama(prompt, model=model)

        try:
            data = json.loads(raw_response)
            return ClassificationResult(
                document_type=data.get("document_type", "unknown"),
                confidence=data.get("confidence", "low"),
                reasoning=data.get("reasoning", ""),
                raw_file="",
                model=model,
            )
        except (json.JSONDecodeError, KeyError):
            return ClassificationResult(
                document_type="unknown",
                confidence="low",
                reasoning=f"Could not parse LLM response: {raw_response}",
                raw_file="",
                model=model,
            )

    def classify_file(self, path: str, model: str = DEFAULT_MODEL) -> ClassificationResult:
        """Read a file and classify its content."""
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()

        result = self._classify_text(text, model=model)
        result.raw_file = path
        return result
