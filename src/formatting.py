import sys
from dataclasses import dataclass
from typing import Optional

from src.constants import *


@dataclass
class Section:
    """A labelled classification section (e.g. the E-Mail Type block)."""
    label: str
    value: str
    value_color: str
    confidence: str
    reasoning: str


def _colored(text: str, color: str, use_color: bool) -> str:
    return f"{color}{text}{RESET}" if use_color else text


def _safe_upper(value: Optional[str]) -> str:
    return value.upper() if value else "UNKNOWN"


def _build_sections(result) -> list[Section]:
    sections: list[Section] = []

    if result.email_type is not None:
        sections.append(Section(
            label="E-Mail Type",
            value=EMAIL_TYPE_LABELS.get(result.email_type, result.email_type),
            value_color=CYAN,
            confidence=result.email_type_confidence or "low",
            reasoning=result.email_type_reasoning or "",
        ))

    if result.mood is not None:
        sections.append(Section(
            label="Mood       ",
            value=MOOD_LABELS.get(result.mood, result.mood),
            value_color=MOOD_COLORS.get(result.mood, YELLOW),
            confidence=result.mood_confidence or "low",
            reasoning=result.mood_reasoning or "",
        ))

    if result.article_topic is not None:
        sections.append(Section(
            label="Topic      ",
            value=ARTICLE_TOPIC_LABELS.get(result.article_topic, result.article_topic),
            value_color=CYAN,
            confidence=result.article_topic_confidence or "low",
            reasoning=result.article_topic_reasoning or "",
        ))

    return sections


def _render(result, use_color: bool) -> str:
    type_label = LABELS.get(result.document_type, result.document_type)
    type_color = TYPE_COLORS.get(result.document_type, YELLOW)
    conf_color = CONFIDENCE_COLORS.get(result.confidence, YELLOW)

    def b(text: str) -> str:
        return _colored(text, BOLD, use_color)

    lines = [
        _colored(OUTER_RULE, BOLD, use_color),
        f"  {b('Model      :')} {result.model}",
        f"  {b('File       :')} {result.raw_file}",
        f"  {b('Type       :')} {_colored(type_label, type_color, use_color)}",
        f"  {b('Confidence :')} {_colored(_safe_upper(result.confidence), conf_color, use_color)}",
        f"  {b('Reasoning  :')} {result.reasoning}",
    ]

    for section in _build_sections(result):
        section_conf_color = CONFIDENCE_COLORS.get(section.confidence, YELLOW)
        lines += [
            f"  {_colored(INNER_RULE, BOLD, use_color)}",
            f"  {b(f'{section.label}:')} {_colored(section.value, section.value_color, use_color)}",
            f"  {b('Confidence :')} {_colored(_safe_upper(section.confidence), section_conf_color, use_color)}",
            f"  {b('Reasoning  :')} {section.reasoning}",
        ]

    lines.append(_colored(OUTER_RULE, BOLD, use_color))
    return "\n".join(lines)


def print_result(result) -> None:
    print(_render(result, use_color=True))
    print()


def format_result_text(result) -> str:
    return _render(result, use_color=False) + "\n"


def print_error(message: str, exc: Exception | None = None) -> None:
    if exc is not None:
        message = f"{message}: {exc}"
    print(f"{_colored('ERROR:', RED, True)} {message}", file=sys.stderr)
