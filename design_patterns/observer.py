from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Generic, Optional, TypeVar

from design_patterns.utils.id_generator import IdGenerator


@dataclass
class State:
    __observable: Optional[Observable] = field(default=None)

    def __setattr__(self, key: Any, value: Any) -> None:
        super().__setattr__(key, value)
        if self.__observable:
            self.__observable._notify_observers()


StateT = TypeVar("StateT", bound=State)


class Observer(Generic[StateT], ABC):
    __next_id = IdGenerator()

    def __init__(self) -> None:
        self.__id = self.__next_id()

    @property
    def id(self) -> int:
        return self.__id

    @abstractmethod
    def notify(self, state: StateT) -> None:
        pass


class Observable(Generic[StateT]):
    def __init__(self, state: StateT) -> None:
        self.__state: StateT = state
        self.__observers: Dict[int, Observer[StateT]] = dict()
        self.__state._State__observable = self

    def _notify_observers(self) -> None:
        for observer in self.__observers.values():
            observer.notify(self.__state)

    def attach(self, observer: Observer[StateT]) -> None:
        self.__observers[observer.id] = observer

    def detach(self, observer: Observer[StateT]) -> None:
        self.__observers.pop(observer.id)

    @property
    def state(self) -> StateT:
        return self.__state

    @state.setter
    def state(self, state: StateT) -> None:
        self.__state = state
        self._notify_observers()
