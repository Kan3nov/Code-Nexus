from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        return (1, "hello")


class NumericProcessor(DataProcessor):
    data: list = []

    def validate(self, data: Any) -> bool:
        return (True)

    def ingest(self, data: int | float | list[int | float]) -> None:
        return


class TextProcessor(DataProcessor):
    pass


class LogProcessor(DataProcessor):
    pass


def main():
    print("=== Code Nexus - Data Processor ===")


if __name__ == "__main__":
    main()
