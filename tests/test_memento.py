import pytest

from design_patterns.command import Command
from design_patterns.memento import CareTaker, Originator


class Thing(Originator):
    def __init__(self):
        self.x = 0


class ChangeCommand(Command):
    def __init__(self, thing: Thing):
        self._thing = thing


class AddOneCommand(ChangeCommand):
    def execute(self) -> None:
        self._thing.x += 1


class DoubleCommand(ChangeCommand):
    def execute(self) -> None:
        self._thing.x *= 2


class ThingCareTaker(CareTaker):
    def __init__(self, thing: Thing):
        super().__init__()
        self.__thing = thing
        self._add_memento(self.__thing.create_memento())

    def add_one(self) -> None:
        self._execute(AddOneCommand(self.__thing))

    def double(self) -> None:
        self._execute(DoubleCommand(self.__thing))

    def _restore_thing(self, memento_idx: int) -> None:
        self.__thing.set_memento(self._get_memento(idx=memento_idx))

    def _execute(self, command: ChangeCommand) -> None:
        command.execute()
        self._add_memento(self.__thing.create_memento())


class UndoRedoCaretaker(ThingCareTaker):
    def __init__(self, thing: Thing):
        super().__init__(thing=thing)
        self.__memento_idx: int = 0

    def _execute(self, command: ChangeCommand) -> None:
        self._delete_newer_mementos(self.__memento_idx)
        self.__memento_idx += 1
        super()._execute(command)

    def undo(self) -> bool:
        if self.__memento_idx <= 0:
            return False
        self.__memento_idx -= 1
        self._restore_thing(self.__memento_idx)
        return True

    def redo(self) -> bool:
        if self.__memento_idx + 1 >= self._memento_history_length():
            return False
        self.__memento_idx += 1
        self._restore_thing(self.__memento_idx)
        return True


@pytest.fixture
def thing():
    return Thing()


@pytest.fixture
def care_taker(thing):
    return UndoRedoCaretaker(thing)


class TestMemento:
    def test_undo_redo_has_no_effect_when_state_never_has_changed(self, care_taker):
        assert care_taker.undo() is False
        assert care_taker.redo() is False

    def test_undo(self, care_taker, thing):
        care_taker.add_one()
        care_taker.double()
        assert thing.x == 2
        assert care_taker.undo() is True
        assert thing.x == 1
        assert care_taker.undo() is True
        assert thing.x == 0
        assert care_taker.undo() is False

    def test_redo(self, care_taker, thing):
        care_taker.add_one()
        care_taker.add_one()
        care_taker.undo()
        care_taker.undo()

        assert care_taker.redo() is True
        assert thing.x == 1
        assert care_taker.redo() is True
        assert thing.x == 2
        assert care_taker.redo() is False

    def test_redo_has_no_effect_after_command_issued(self, care_taker):
        care_taker.add_one()
        care_taker.undo()
        care_taker.add_one()
        assert care_taker.redo() is False
