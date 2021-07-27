from logging import Logger


class Loggi(Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        