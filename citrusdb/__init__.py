from typing import Optional

def Client(
    persist_directory: Optional[str] = None,
    database_type: Optional[str] = "sqlite",
    **kwargs
):
    from citrusdb.api.local import LocalAPI

    return LocalAPI(persist_directory, database_type=database_type, **kwargs)

def Console(
    persist_directory: Optional[str] = None,
    database_type: Optional[str] = "sqlite",
    **kwargs
):
    from citrusdb.api.console import ConsoleAPI

    return ConsoleAPI(persist_directory, database_type=database_type, **kwargs)
