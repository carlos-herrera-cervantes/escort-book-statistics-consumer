from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def process_message(self, message: dict) -> None:
        pass
