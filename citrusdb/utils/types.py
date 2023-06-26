from numpy import float32
from numpy._typing import NDArray
from typing import List, Optional, TypedDict

ID = str
IDs = List[ID]

class Document(TypedDict):
    id: int
    text: Optional[str]
    embedding: Optional[NDArray[float32]]
