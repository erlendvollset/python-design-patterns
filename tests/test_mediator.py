import pytest

from design_patterns.mediator import Mediator
from design_patterns.utils.counter import Counter
from design_patterns.utils.runnable import Runnable


class Producer(Runnable):
    def __init__(self, mediator: Mediator, messages_to_produce: int):
        self.messages_to_produce = messages_to_produce
        self.__mediator = mediator

    def run(self):
        for _ in range(self.messages_to_produce):
            self.__mediator.add_message("message")


class Consumer(Runnable):
    def __init__(self, mediator: Mediator, counter: Counter):
        self.counter = counter
        self.__mediator = mediator

    def run(self) -> None:
        while not self.counter.finished():
            self.__mediator.retrieve_message(timeout=0.5)
            self.counter.inc()


@pytest.fixture
def mediator():
    return Mediator(max_messages=100)


@pytest.fixture
def consumption_counter():
    return Counter(500)


@pytest.fixture
def consumers(consumption_counter, mediator):
    for _ in range(10):
        Consumer(mediator, consumption_counter).run_in_thread()


@pytest.fixture
def producers(mediator):
    for _ in range(5):
        Producer(mediator, 100).run_in_thread()


class TestMediator:
    def test_all_messages_consumed(self, producers, consumers, consumption_counter):
        consumption_counter.wait_until_finished()
        assert consumption_counter.count() == 500
