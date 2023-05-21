CREATE_INDEX_MANAGER_TABLE = '''
CREATE TABLE IF NOT EXISTS index_manager (
    index_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    dimensions INTEGER NOT NULL,
    max_elements INTEGER NOT NULL,
    m INTEGER NOT NULL,
    ef INTEGER NOT NULL,
    ef_construction INTEGER NOT NULL,
    allow_replace_deleted INTEGER NOT NULL
);
'''

CREATE_INDEX_DATA_TABLE = '''
CREATE TABLE IF NOT EXISTS index_data (
    id TEXT PRIMARY KEY,
    index_id INTEGER,
    text TEXT,
    embedding BLOB,
    metadata TEXT,
    FOREIGN KEY(index_id) REFERENCES index_manager(index_id) ON DELETE CASCADE
);
'''

INSERT_INDEX_TO_MANAGER = '''
INSERT INTO index_manager
(name, dimensions, max_elements, m, ef, ef_construction, allow_replace_deleted)
VALUES (?, ?, ?, ?, ?, ?, ?);
'''

GET_INDEX_BY_NAME = '''
SELECT index_id
FROM index_manager
WHERE name = ?
'''
