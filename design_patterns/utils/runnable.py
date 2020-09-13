from abc import ABC, abstractmethod
from threading import Thread


class Runnable(ABC):
    def run_in_thread(self, daemon: bool = False) -> None:
        Thread(target=self.run, daemon=daemon).start()

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError
