from dataclasses import dataclass

import pytest

from design_patterns.chain_of_responsibility import Handler


@dataclass
class TestRequest:
    visited: int = 0
    max_visited: int = 100


class TestHandler(Handler[TestRequest]):
    def __call__(self, request: TestRequest) -> None:
        request.visited += 1
        if request.visited < request.max_visited and self._next is not None:
            self._next(request)


@pytest.fixture
def root_handler():
    yield TestHandler(TestHandler(TestHandler()))


class TestChainOfResponsibility:
    def test_all_handlers_visted(self, root_handler):
        request = TestRequest()
        root_handler(request)
        assert request.visited == 3

    def test_wraparound_handling_loop(self, root_handler):
        root_handler.wrap_around()
        request = TestRequest()
        root_handler(request)
        assert request.visited == request.max_visited
