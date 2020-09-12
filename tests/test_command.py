import threading

from design_patterns.command import Command, Invoker


class TestCommand(Command):
    def __init__(self, event: threading.Event):
        self.__event = event

    def execute(self) -> None:
        self.__event.set()


class TestCommandExecution:
    def test_command_executed(self):
        invoker = Invoker()
        event = threading.Event()
        command = TestCommand(event)

        invoker.store_command(command)
        invoker.execute_commands()

        assert event.is_set()
