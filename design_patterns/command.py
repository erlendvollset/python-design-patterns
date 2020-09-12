from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


class Invoker:
    def __init__(self) -> None:
        self.__commands: List[Command] = []

    def store_command(self, command: Command) -> None:
        self.__commands.append(command)

    def execute_commands(self) -> None:
        for command in self.__commands:
            command.execute()
