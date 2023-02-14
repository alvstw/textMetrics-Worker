from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')


@dataclass
class ServerResponse(Generic[T]):
    succeeded: bool
    message: str
    errors: list
    data: T
