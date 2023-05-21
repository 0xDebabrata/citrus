CREATE_INDEX_MANAGER_TABLE = '''
CREATE TABLE index_manager (
    index_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dimensions INTEGER,
    max_elements INTEGER,
    m INTEGER,
    ef INTEGER,
    ef_construction INTEGER,
    allow_replace_deleted INTEGER
)
'''

CREATE_INDEX = '''
INSERT INTO index_manager
(name, dimensions, max_elements, m, ef, ef_construction, allow_replace_deleted)
VALUES (?, ?, ?, ?, ?, ?, ?)
'''

GET_INDEX_BY_NAME = '''
SELECT index_id
FROM index_manager
WHERE name = ?
'''
