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
    vector_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT NOT NULL,
    index_id INTEGER,
    text TEXT,
    embedding BLOB NOT NULL,
    metadata TEXT,
    UNIQUE(id, index_id),
    FOREIGN KEY(index_id) REFERENCES index_manager(index_id) ON DELETE CASCADE
);
'''

DELETE_VECTORS_FROM_INDEX = '''
DELETE FROM index_data
WHERE id IN ({}) AND index_id = ?
RETURNING vector_id
'''

GET_ALL_INDEX_DETAILS = '''
SELECT index_id, name, dimensions, max_elements, m, ef, ef_construction, allow_replace_deleted
FROM index_manager
'''

GET_INDEX_DETAILS_BY_NAME = '''
SELECT index_id, name, dimensions, max_elements, m, ef, ef_construction, allow_replace_deleted
FROM index_manager
WHERE name = ?
'''

GET_VECTOR_IDS_OF_RESULTS = '''
SELECT id
FROM index_data
WHERE vector_id IN ({}) AND index_id = ?
'''

INSERT_DATA_TO_INDEX = '''
INSERT INTO index_data
(id, index_id, text, embedding, metadata)
VALUES(?, ?, ?, ?, ?)
ON CONFLICT(id, index_id)
DO UPDATE SET id = ?, index_id = ?, text = ?, embedding = ?, metadata = ?
RETURNING vector_id
'''

INSERT_INDEX_TO_MANAGER = '''
INSERT INTO index_manager
(name, dimensions, max_elements, m, ef, ef_construction, allow_replace_deleted)
VALUES (?, ?, ?, ?, ?, ?, ?);
'''

UPDATE_EF = '''
UPDATE index_manager
SET ef = ?
WHERE name = ?
'''
