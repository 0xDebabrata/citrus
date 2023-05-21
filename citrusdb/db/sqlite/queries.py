CREATE_INDEX_MANAGER_TABLE = '''
CREATE TABLE index_manager (
    index_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dimensions INTEGER
    max_elements INTEGER,
    m INTEGER,
    ef INTEGER,
    ef_construction INTEGER,
    allow_replace_deleted INTEGER
)
'''
