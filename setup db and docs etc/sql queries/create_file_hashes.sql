CREATE TABLE imports (
    id INTEGER PRIMARY KEY,
    file_hash TEXT UNIQUE,
    file_name TEXT,
    status TEXT,
);