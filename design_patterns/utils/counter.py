import threading
from typing import Optional


class Counter:
    def __init__(self, count_to: int):
        self.__lock = threading.Lock()
        self.__finished = threading.Event()
        self.__counter: int = 0
        self.__count_to = count_to

    def inc(self) -> None:
        with self.__lock:
            self.__counter += 1
            if self.__counter >= self.__count_to:
                self.__finished.set()

    def count(self) -> int:
        return self.__counter

    def wait_until_finished(self, timeout: Optional[float] = None) -> bool:
        return self.__finished.wait(timeout=timeout)

    def finished(self) -> bool:
        return self.__finished.is_set()
