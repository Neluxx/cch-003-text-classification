import argparse
import sys
from pathlib import Path

from src.classifier import Classifier, DEFAULT_MODEL

# ── ANSI colours (graceful fallback on Windows) ──────────────────────────────
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

TYPE_COLOURS = {
    "email": CYAN,
    "scientific_article": CYAN,
    "unknown": YELLOW,
}

CONFIDENCE_COLOURS = {
    "high": GREEN,
    "medium": YELLOW,
    "low": RED,
}

LABELS = {
    "email": "E-Mail",
    "scientific_article": "Scientific Article",
    "unknown": "Unknown",
}


def _coloured(text: str, colour: str) -> str:
    return f"{colour}{text}{RESET}"


def print_result(result) -> None:
    type_colour = TYPE_COLOURS.get(result.document_type, YELLOW)
    conf_colour = CONFIDENCE_COLOURS.get(result.confidence, YELLOW)

    label = LABELS.get(result.document_type, result.document_type)

    print()
    print(_coloured("─" * 60, BOLD))
    print(f"  {BOLD}Model      :{RESET} {result.model}")
    print(f"  {BOLD}File       :{RESET} {result.raw_file}")
    print(f"  {BOLD}Type       :{RESET} {_coloured(label, type_colour)}")
    print(f"  {BOLD}Confidence :{RESET} {_coloured(result.confidence.upper(), conf_colour)}")
    print(f"  {BOLD}Reasoning  :{RESET} {result.reasoning}")
    print(_coloured("─" * 60, BOLD))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Text Classification Tool"
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="One or more text files to classify.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama model name to use (default: {DEFAULT_MODEL}).",
    )
    args = parser.parse_args()

    exit_code = 0
    for file_path in args.files:
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            print(f"{RED}ERROR:{RESET} File not found: {file_path}", file=sys.stderr)
            exit_code = 1
            continue

        try:
            classifier = Classifier()
            result = classifier.classify_file(str(path), model=args.model)
            print_result(result)
        except ConnectionError as exc:
            print(f"\n{RED}Connection Error:{RESET} {exc}", file=sys.stderr)
            return 1
        except Exception as exc:
            print(f"\n{RED}Unexpected error for {file_path}:{RESET} {exc}", file=sys.stderr)
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
