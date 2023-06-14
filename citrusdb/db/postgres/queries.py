CREATE_INDEX_MANAGER_TABLE = '''
CREATE TABLE IF NOT EXISTS index_manager (
    index_id BIGSERIAL PRIMARY KEY,
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
    id BIGINT,
    index_id BIGINT,
    text TEXT,
    embedding JSONB NOT NULL,
    metadata JSONB,
    PRIMARY KEY(id, index_id),
    FOREIGN KEY(index_id) REFERENCES index_manager(index_id) ON DELETE CASCADE
);
'''

DELETE_VECTORS_FROM_INDEX = '''
DELETE FROM index_data
WHERE id IN %s AND index_id = %s
'''

GET_ALL_INDEX_DETAILS = '''
SELECT index_id, name, dimensions, max_elements, m, ef, ef_construction, allow_replace_deleted
FROM index_manager
'''

GET_INDEX_DETAILS_BY_NAME = '''
SELECT index_id, name, dimensions, max_elements, m, ef, ef_construction, allow_replace_deleted
FROM index_manager
WHERE name = %s
'''

INSERT_DATA_TO_INDEX = '''
INSERT INTO index_data
VALUES(%s, %s, %s, %s, %s)
ON CONFLICT(id, index_id)
DO UPDATE SET id = %s, index_id = %s, text = %s, embedding = %s, metadata = %s
'''

INSERT_INDEX_TO_MANAGER = '''
INSERT INTO index_manager
(name, dimensions, max_elements, m, ef, ef_construction, allow_replace_deleted)
VALUES (%s, %s, %s, %s, %s, %s, %s);
'''

UPDATE_EF = '''
UPDATE index_manager
SET ef = %s
WHERE name = %s
'''
