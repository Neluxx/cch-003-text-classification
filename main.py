import argparse
import sys
from pathlib import Path

from src.classifier import Classifier, DEFAULT_MODEL
from src.formatting import print_result, print_error, format_result_text


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
    parser.add_argument(
        "--output",
        default=None,
        metavar="FILE",
        help="Optional file path to save the classification results as plain text.",
    )
    args = parser.parse_args()

    exit_code = 0
    output_lines: list[str] = []

    for file_path in args.files:
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            print_error(f"File not found: {file_path}")
            exit_code = 1
            continue

        try:
            classifier = Classifier(model=args.model)
            result = classifier.classify_file(str(path))
            print_result(result)
            if args.output:
                output_lines.append(format_result_text(result))
        except ConnectionError as exc:
            print_error("Connection Error", exc)
            return 1
        except Exception as exc:
            print_error(f"Unexpected error for {file_path}", exc)
            exit_code = 1

    if args.output and output_lines:
        try:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text("\n".join(output_lines), encoding="utf-8")
            print(f"Results saved to: {out_path}")
        except OSError as exc:
            print_error(f"Could not write output file: {args.output}", exc)
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
