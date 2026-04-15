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

MOOD_COLORS = {
    "neutral": CYAN,
    "friendly": GREEN,
    "angry": RED,
    "unknown": YELLOW,
}

LABELS = {
    "email": "E-Mail",
    "scientific_article": "Scientific Article",
    "unknown": "Unknown",
}

EMAIL_TYPE_LABELS = {
    "support": "Support",
    "complaint": "Complaint",
    "unknown": "Unknown",
}

ARTICLE_TOPIC_LABELS = {
    "computer_science": "Computer Science",
    "medicine": "Medicine",
    "biology": "Biology",
    "physics": "Physics",
    "chemistry": "Chemistry",
    "environmental_science": "Environmental Science",
    "economics": "Economics",
    "psychology": "Psychology",
    "other": "Other",
    "unknown": "Unknown",
}

MOOD_LABELS = {
    "neutral": "Neutral",
    "friendly": "Friendly",
    "angry": "Angry",
    "unknown": "Unknown",
}


def colored(text: str, color: str) -> str:
    return f"{color}{text}{RESET}"


def print_result(result) -> None:
    """Print a classification result to stdout with ANSI colours."""
    type_colour = TYPE_COLORS.get(result.document_type, YELLOW)
    conf_colour = CONFIDENCE_COLORS.get(result.confidence, YELLOW)
    label = LABELS.get(result.document_type, result.document_type)

    print(colored("─" * 60, BOLD))
    print(f"  {BOLD}Model      :{RESET} {result.model}")
    print(f"  {BOLD}File       :{RESET} {result.raw_file}")
    print(f"  {BOLD}Type       :{RESET} {colored(label, type_colour)}")
    print(f"  {BOLD}Confidence :{RESET} {colored(result.confidence.upper(), conf_colour)}")
    print(f"  {BOLD}Reasoning  :{RESET} {result.reasoning}")

    if result.email_type is not None:
        email_label = EMAIL_TYPE_LABELS.get(result.email_type, result.email_type)
        email_conf_colour = CONFIDENCE_COLORS.get(result.email_type_confidence, YELLOW)
        print(f"  {colored('─' * 56, BOLD)}")
        print(f"  {BOLD}E-Mail Type:{RESET} {colored(email_label, CYAN)}")
        print(f"  {BOLD}Confidence :{RESET} {colored(result.email_type_confidence.upper(), email_conf_colour)}")
        print(f"  {BOLD}Reasoning  :{RESET} {result.email_type_reasoning}")

    if result.mood is not None:
        mood_label = MOOD_LABELS.get(result.mood, result.mood)
        mood_colour = MOOD_COLORS.get(result.mood, YELLOW)
        mood_conf_colour = CONFIDENCE_COLORS.get(result.mood_confidence, YELLOW)
        print(f"  {colored('─' * 56, BOLD)}")
        print(f"  {BOLD}Mood       :{RESET} {colored(mood_label, mood_colour)}")
        print(f"  {BOLD}Confidence :{RESET} {colored(result.mood_confidence.upper(), mood_conf_colour)}")
        print(f"  {BOLD}Reasoning  :{RESET} {result.mood_reasoning}")

    if result.article_topic is not None:
        topic_label = ARTICLE_TOPIC_LABELS.get(result.article_topic, result.article_topic)
        topic_conf_colour = CONFIDENCE_COLORS.get(result.article_topic_confidence, YELLOW)
        print(f"  {colored('─' * 56, BOLD)}")
        print(f"  {BOLD}Topic      :{RESET} {colored(topic_label, CYAN)}")
        print(f"  {BOLD}Confidence :{RESET} {colored(result.article_topic_confidence.upper(), topic_conf_colour)}")
        print(f"  {BOLD}Reasoning  :{RESET} {result.article_topic_reasoning}")

    print(colored("─" * 60, BOLD))
    print()


def format_result_text(result) -> str:
    """Return a plain-text (no ANSI) representation of a classification result."""
    label = LABELS.get(result.document_type, result.document_type)
    lines = [
        "─" * 60,
        f"  Model      : {result.model}",
        f"  File       : {result.raw_file}",
        f"  Type       : {label}",
        f"  Confidence : {result.confidence.upper()}",
        f"  Reasoning  : {result.reasoning}",
    ]

    if result.email_type is not None:
        email_label = EMAIL_TYPE_LABELS.get(result.email_type, result.email_type)
        lines += [
            "  " + "─" * 56,
            f"  E-Mail Type: {email_label}",
            f"  Confidence : {result.email_type_confidence.upper()}",
            f"  Reasoning  : {result.email_type_reasoning}",
        ]

    if result.mood is not None:
        mood_label = MOOD_LABELS.get(result.mood, result.mood)
        lines += [
            "  " + "─" * 56,
            f"  Mood       : {mood_label}",
            f"  Confidence : {result.mood_confidence.upper()}",
            f"  Reasoning  : {result.mood_reasoning}",
        ]

    if result.article_topic is not None:
        topic_label = ARTICLE_TOPIC_LABELS.get(result.article_topic, result.article_topic)
        lines += [
            "  " + "─" * 56,
            f"  Topic      : {topic_label}",
            f"  Confidence : {result.article_topic_confidence.upper()}",
            f"  Reasoning  : {result.article_topic_reasoning}",
        ]

    lines.append("─" * 60)
    return "\n".join(lines) + "\n"


def print_error(message: str, exc: Exception | None = None) -> None:
    if exc is not None:
        message = f"{message}: {exc}"
    print(f"{colored('ERROR:', RED)} {message}", file=sys.stderr)
