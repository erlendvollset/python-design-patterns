from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

Request = TypeVar("Request")


class Handler(Generic[Request], ABC):
    def __init__(self, next: Optional[Handler[Request]] = None):
        self._next: Optional[Handler] = next

    @abstractmethod
    def __call__(self, request: Request) -> None:
        raise NotImplementedError

    def wrap_around(self) -> None:
        self.__wrap_around(self)

    def __wrap_around(self, root: Handler) -> None:
        if self._next is None:
            self._next = root
        else:
            self._next.__wrap_around(root)
