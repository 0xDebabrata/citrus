from numpy import float32
from numpy._typing import NDArray
from typing import Optional, TypedDict

class Document(TypedDict):
    id: int
    text: Optional[str]
    embedding: Optional[NDArray[float32]]
