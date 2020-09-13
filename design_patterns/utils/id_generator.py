class IdGenerator:
    def __init__(self) -> None:
        self.__CURRENT_GLOBAL_ID: int = -1

    def __call__(self) -> int:
        self.__CURRENT_GLOBAL_ID += 1
        return self.__CURRENT_GLOBAL_ID
