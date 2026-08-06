CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    german TEXT NOT NULL UNIQUE,
    english TEXT NOT NULL,

    article TEXT NOT NULL CHECK (article IN ('der', 'die', 'das')),
    plural TEXT,

    level TEXT CHECK (level IN ('A1', 'A2', 'B1', 'B2', 'C1', 'C2')),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);