import json
from abc import ABC
from datetime import datetime
from typing import List


class Memento:
    def __init__(self, state: bytes) -> None:
        self.__state = state
        self.__created_time = datetime.now()

    @property
    def state(self) -> bytes:
        return self.__state

    @property
    def created_time(self) -> datetime:
        return self.__created_time


class Originator(ABC):
    def create_memento(self) -> Memento:
        return Memento(json.dumps(vars(self)).encode())

    def set_memento(self, memento: Memento) -> None:
        state = json.loads(memento.state)
        vars(self).clear()
        vars(self).update(state)


class CareTaker:
    def __init__(self) -> None:
        self.__mementos: List[Memento] = []

    def add_memento(self, memento: Memento) -> None:
        self.__mementos.append(memento)

    def get_memento(self, idx: int = -1) -> Memento:
        return self.__mementos[idx]

    def delete_newer_mementos(self, idx: int) -> None:
        self.__mementos = self.__mementos[:idx]

    def memento_history_length(self) -> int:
        return len(self.__mementos)
