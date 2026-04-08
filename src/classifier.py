import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

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
    # E-mail subtype (SG-002)
    email_type: Optional[str] = None
    email_type_confidence: Optional[str] = None
    email_type_reasoning: Optional[str] = None
    # Article topic (SG-003)
    article_topic: Optional[str] = None
    article_topic_confidence: Optional[str] = None
    article_topic_reasoning: Optional[str] = None


class Classifier:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model

    def _call_ollama(self, prompt: str) -> str:
        """Send a prompt to the local Ollama instance and return the response text."""
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response.response.strip()
        except ollama.ResponseError as exc:
            raise ConnectionError(f"Ollama error: {exc}") from exc
        except Exception as exc:
            raise ConnectionError(f"Could not reach Ollama. Is it running?") from exc

    def _build_prompt(self, template_name: str, text: str) -> str:
        template = (PROMPTS_DIR / template_name).read_text(encoding="utf-8")
        return template.replace("{text}", text[:4000])

    def _classify_document_type(self, text: str) -> ClassificationResult:
        """Stage 1: classify text as email or scientific_article."""
        prompt = self._build_prompt("classify_document_type.txt", text)
        raw_response = self._call_ollama(prompt)

        try:
            data = json.loads(raw_response)
            return ClassificationResult(
                model=self.model,
                document_type=data.get("document_type", "unknown"),
                confidence=data.get("confidence", "low"),
                reasoning=data.get("reasoning", ""),
                raw_file="",
            )
        except (json.JSONDecodeError, KeyError):
            return ClassificationResult(
                model=self.model,
                document_type="unknown",
                confidence="low",
                reasoning=f"Could not parse LLM response: {raw_response}",
                raw_file="",
            )

    def _classify_email_type(self, text: str, result: ClassificationResult) -> None:
        """Stage 2a: classify email as support or complaint."""
        prompt = self._build_prompt("classify_email_type.txt", text)
        raw_response = self._call_ollama(prompt)

        try:
            data = json.loads(raw_response)
            result.email_type = data.get("email_type", "unknown")
            result.email_type_confidence = data.get("confidence", "low")
            result.email_type_reasoning = data.get("reasoning", "")
        except (json.JSONDecodeError, KeyError):
            result.email_type = "unknown"
            result.email_type_confidence = "low"
            result.email_type_reasoning = f"Could not parse LLM response: {raw_response}"

    def _classify_article_topic(self, text: str, result: ClassificationResult) -> None:
        """Stage 2b: classify the topic area of a scientific article."""
        prompt = self._build_prompt("classify_article_topic.txt", text)
        raw_response = self._call_ollama(prompt)

        try:
            data = json.loads(raw_response)
            result.article_topic = data.get("article_topic", "unknown")
            result.article_topic_confidence = data.get("confidence", "low")
            result.article_topic_reasoning = data.get("reasoning", "")
        except (json.JSONDecodeError, KeyError):
            result.article_topic = "unknown"
            result.article_topic_confidence = "low"
            result.article_topic_reasoning = f"Could not parse LLM response: {raw_response}"

    def _classify_text(self, text: str) -> ClassificationResult:
        """Classify the provided text using a local Ollama LLM."""
        result = self._classify_document_type(text)

        if result.document_type == "email":
            self._classify_email_type(text, result)
        elif result.document_type == "scientific_article":
            self._classify_article_topic(text, result)

        return result

    def classify_file(self, path: str) -> ClassificationResult:
        """Read a file and classify its content."""
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()

        result = self._classify_text(text)
        result.raw_file = path
        return result
