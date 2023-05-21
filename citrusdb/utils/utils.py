import os
from typing import Optional

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
