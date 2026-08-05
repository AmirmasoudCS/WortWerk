CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    german TEXT NOT NULL,
    english TEXT NOT NULL,

    word_type TEXT NOT NULL,

    article TEXT,
    plural TEXT,

    level TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);