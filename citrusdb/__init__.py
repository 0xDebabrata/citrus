from typing import Optional

def Client(persist_directory: Optional[str] = None):
    from citrusdb.api.local import LocalAPI

    return LocalAPI(persist_directory)
