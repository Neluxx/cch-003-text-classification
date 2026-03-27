import sys

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

TYPE_COLORS = {
    "email": CYAN,
    "scientific_article": CYAN,
    "unknown": YELLOW,
}

CONFIDENCE_COLORS = {
    "high": GREEN,
    "medium": YELLOW,
    "low": RED,
}

LABELS = {
    "email": "E-Mail",
    "scientific_article": "Scientific Article",
    "unknown": "Unknown",
}


def colored(text: str, color: str) -> str:
    return f"{color}{text}{RESET}"


def print_result(result) -> None:
    type_colour = TYPE_COLORS.get(result.document_type, YELLOW)
    conf_colour = CONFIDENCE_COLORS.get(result.confidence, YELLOW)
    label = LABELS.get(result.document_type, result.document_type)

    print(colored("─" * 60, BOLD))
    print(f"  {BOLD}Model      :{RESET} {result.model}")
    print(f"  {BOLD}File       :{RESET} {result.raw_file}")
    print(f"  {BOLD}Type       :{RESET} {colored(label, type_colour)}")
    print(f"  {BOLD}Confidence :{RESET} {colored(result.confidence.upper(), conf_colour)}")
    print(f"  {BOLD}Reasoning  :{RESET} {result.reasoning}")
    print(colored("─" * 60, BOLD))
    print()


def print_error(message: str, exc: Exception | None = None) -> None:
    if exc is not None:
        message = f"{message}: {exc}"
    print(f"{colored('ERROR:', RED)} {message}", file=sys.stderr)
