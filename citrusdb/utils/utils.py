import os
import json
from typing import Dict, Optional, Tuple

def convert_row_to_dict(row: Tuple, include: Dict, with_embedding: bool = False):
    if with_embedding:
        returning_dict = {"id": row[2], "embedding": json.loads(row[1])}
        if include["document"]:
            returning_dict["document"] = row[3]
            if include["metadata"]:
                returning_dict["metadata"] = row[4]
        elif include["metadata"]:
            returning_dict["metadata"] = row[3]

        return returning_dict
    else:
        returning_dict = {"id": row[1]}
        if include["document"]:
            returning_dict["document"] = row[2]
            if include["metadata"]:
                returning_dict["metadata"] = row[3]
        elif include["metadata"]:
            returning_dict["metadata"] = row[2]

        return returning_dict

def ensure_valid_path(persist_directory: str, file_name: Optional[str] = None) -> bool:
    """
    Creates required directories if they do not exist.

    If only persist_directory is passed, returns True.
    When file_name is passed, function returns boolean based on whether the
    file can be found in given path.
    """
    # Ensure directory exists
    if not (os.path.isdir(persist_directory)):
        os.makedirs(persist_directory)

    if file_name is None:
        return True

    if os.path.exists(
        os.path.join(persist_directory, file_name)
    ):
        return True
    else:
        return False
