import argparse
import sys
from pathlib import Path

from src.classifier import Classifier, DEFAULT_MODEL
from src.formatting import print_result, print_error


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
            print_error(f"File not found: {file_path}")
            exit_code = 1
            continue

        try:
            classifier = Classifier()
            result = classifier.classify_file(str(path), model=args.model)
            print_result(result)
        except ConnectionError as exc:
            print_error("Connection Error", exc)
            return 1
        except Exception as exc:
            print_error(f"Unexpected error for {file_path}", exc)
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
