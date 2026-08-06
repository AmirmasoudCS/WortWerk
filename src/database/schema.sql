CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    german TEXT NOT NULL UNIQUE,
    english TEXT NOT NULL,

    article TEXT NOT NULL CHECK (article IN ('der', 'die', 'das')),
    plural TEXT,

    level TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);