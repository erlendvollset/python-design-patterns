from dataclasses import dataclass

import pytest

from design_patterns.observer import Observable, Observer, State


@dataclass
class TestState(State):
    x: int = 100
    y: int = 200


@pytest.fixture
def state():
    yield TestState()


@pytest.fixture
def observable(state):
    yield Observable[TestState](state)


@pytest.fixture
def attach_observers(observable):
    notifs = {}

    class TestObserver(Observer[TestState]):
        def notify(self, state: TestState) -> None:
            notifs[self.id] = state.x

    n_observers = 10

    for _ in range(n_observers):
        observable.attach(TestObserver())

    yield n_observers, notifs


class TestObserversNotified:
    def test_observers_notified(self, observable, attach_observers):
        n_observers, notifs = attach_observers
        observable.state.x = 1
        assert notifs == {i: 1 for i in range(n_observers)}
