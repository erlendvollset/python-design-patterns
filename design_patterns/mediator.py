import threading
from collections import deque
from typing import Deque, Generic, Optional, TypeVar

Message = TypeVar("Message")


class Mediator(Generic[Message]):
    """Implements a mediator handling a many-to-many relationship between producers and consumers.

     The mediator ensures that no more than max_messages messages is handled at a time and that exactly one
    consumer receives every produced message.
    """

    def __init__(self, max_messages: int = 10) -> None:
        self.max_messages = max_messages
        self.__rcv_cond = threading.Condition()
        self.__add_cond = threading.Condition()
        self.__messages: Deque[Message] = deque()

    def add_message(self, message: Message) -> None:
        with self.__add_cond:
            self.__add_cond.wait_for(self.__has_space)
            self.__messages.append(message)
            with self.__rcv_cond:
                self.__rcv_cond.notify()

    def retrieve_message(self, timeout: Optional[float] = None) -> Optional[Message]:
        with self.__rcv_cond:
            if not self.__rcv_cond.wait_for(self.__not_empty, timeout=timeout):
                return None
            message = self.__messages.popleft()
            with self.__add_cond:
                self.__add_cond.notify()
            return message

    def __has_space(self) -> bool:
        return len(self.__messages) < self.max_messages

    def __not_empty(self) -> bool:
        return len(self.__messages) > 0
