class IdGenerator:
    __CURRENT_GLOBAL_ID: int = 0

    @staticmethod
    def next_id() -> int:
        id = IdGenerator.__CURRENT_GLOBAL_ID
        IdGenerator.__CURRENT_GLOBAL_ID += 1
        return id
