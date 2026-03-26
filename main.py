import argparse
import sys
from pathlib import Path

from src.classifier import Classifier, DEFAULT_MODEL


def print_result(result) -> None:
    print(f"Model      : {result.model}")
    print(f"File       : {result.raw_file}")
    print(f"Type       : {result.document_type}")
    print(f"Confidence : {result.confidence}")
    print(f"Reasoning  : {result.reasoning}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Text Classification Tool")
    parser.add_argument("files", nargs="+", help="One or more text files to classify.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model name to use (default: {DEFAULT_MODEL}).")
    args = parser.parse_args()

    exit_code = 0
    for file_path in args.files:
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            print(f"ERROR: File not found: {file_path}", file=sys.stderr)
            exit_code = 1
            continue

        try:
            classifier = Classifier()
            result = classifier.classify_file(str(path), model=args.model)
            print_result(result)
        except ConnectionError as exc:
            print(f"\nConnection Error: {exc}", file=sys.stderr)
            return 1
        except Exception as exc:
            print(f"\nUnexpected error for {file_path}: {exc}", file=sys.stderr)
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
