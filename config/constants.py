SUPPORTED_LANGUAGES = [
    "German",
    "English",
]

DEFAULT_LANGUAGE = SUPPORTED_LANGUAGES[0]

VALID_ARTICLES = {"der", "die", "das"}

PRACTICE_SESSION_TYPE = "practice"
QUIZ_SESSION_TYPE = "quiz"

PRACTICE_MODE_NAMES = {
    "article": "German → Article",
    "english": "German → English",
    "german": "English → German",
    "plural": "German → Plural",
}

VALID_LEVELS = {
    "A1",
    "A2",
    "B1",
    "B2",
    "C1",
    "C2",
}

VALID_SESSION_TYPES = {
    "practice",
    "quiz",
}

VALID_PRACTICE_MODES = {
    "article",
    "english",
    "german",
    "plural",
}

# Quiz questions templates

QUIZ_TEMPLATE_QUESTION_COUNTS = {
    "short": {
        "article": 3,
        "english": 3,
        "german": 3,
        "plural": 3,
    },
    "medium": {
        "article": 5,
        "english": 5,
        "german": 5,
        "plural": 5,
    },
    "long": {
        "article": 10,
        "english": 10,
        "german": 10,
        "plural": 10,
    },
}