"""Color codes, labels, and rendering constants for classification output."""

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Layout
OUTER_RULE = "─" * 60
INNER_RULE = "─" * 56

# Color codes
CONFIDENCE_COLORS = {
    "high": GREEN,
    "medium": YELLOW,
    "low": RED,
}

TYPE_COLORS = {
    "email": CYAN,
    "scientific_article": CYAN,
    "unknown": YELLOW,
}

MOOD_COLORS = {
    "neutral": CYAN,
    "friendly": GREEN,
    "angry": RED,
    "unknown": YELLOW,
}

# Display labels
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
