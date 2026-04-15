import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import ollama

DEFAULT_MODEL = "qwen2.5:3b"
PROMPT_FILE = Path(__file__).parent / "prompt.txt"


@dataclass
class ClassificationResult:
    document_type: str
    confidence: str
    reasoning: str
    raw_file: str
    model: str
    # E-mail subtype (SG-002)
    email_type: Optional[str] = None
    email_type_confidence: Optional[str] = None
    email_type_reasoning: Optional[str] = None
    # Article topic (SG-003)
    article_topic: Optional[str] = None
    article_topic_confidence: Optional[str] = None
    article_topic_reasoning: Optional[str] = None
    # E-mail mood (SG-004)
    mood: Optional[str] = None
    mood_confidence: Optional[str] = None
    mood_reasoning: Optional[str] = None


class Classifier:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model

    def _call_ollama(self, prompt: str) -> str:
        """Send a prompt to the local Ollama instance and return the response text."""
        try:
            response = ollama.generate(model=self.model, prompt=prompt, format="json")
            return response.response.strip()
        except ollama.ResponseError as exc:
            raise ConnectionError(f"Ollama error: {exc}") from exc
        except Exception as exc:
            raise ConnectionError("Could not reach Ollama. Is it running?") from exc

    def _classify_text(self, text: str) -> ClassificationResult:
        """Classify the provided text in a single Ollama call."""
        prompt = PROMPT_FILE.read_text(encoding="utf-8").replace("{text}", text[:4000])
        raw_response = self._call_ollama(prompt)

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError:
            return ClassificationResult(
                model=self.model,
                document_type="unknown",
                confidence="low",
                reasoning=f"Could not parse LLM response: {raw_response}",
                raw_file="",
            )

        result = ClassificationResult(
            model=self.model,
            document_type=data.get("document_type", "unknown"),
            confidence=data.get("confidence", "low"),
            reasoning=data.get("reasoning", ""),
            raw_file="",
            email_type=data.get("email_type"),
            email_type_confidence=data.get("email_type_confidence"),
            email_type_reasoning=data.get("email_type_reasoning"),
            mood=data.get("mood"),
            mood_confidence=data.get("mood_confidence"),
            mood_reasoning=data.get("mood_reasoning"),
            article_topic=data.get("article_topic"),
            article_topic_confidence=data.get("article_topic_confidence"),
            article_topic_reasoning=data.get("article_topic_reasoning"),
        )

        return result

    def classify_file(self, path: str) -> ClassificationResult:
        """Read a file and classify its content."""
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()

        result = self._classify_text(text)
        result.raw_file = path
        return result
