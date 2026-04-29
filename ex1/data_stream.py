from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self._storage = []
        self._rank = 0

    def get_stats(self):
        return (self._rank + 1, len(self.self._storage))

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        try:
            record = self._storage.pop()
            return record
        except Exception as e:
            print("Error: ", e)
            return (-1, "Error")


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if (isinstance(data, (int, float))):
            return True
        elif (isinstance(data, list)):
            for elem in data:
                if (not isinstance(elem, (int, float))):
                    return False
            return True
        else:
            return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if (not self.validate(data)):
            raise ValueError("Error : Data should be int, float," +
                             " or a list of both types " +
                             "(including mixedtype lists).")
        elif (isinstance(data, (float, int))):
            self._storage.insert(0, (self._rank, str(data)))
            self._rank += 1
        elif (isinstance(data, list)):
            for elem in data:
                self._storage.insert(0, (self._rank, str(elem)))
                self._rank += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if (isinstance(data, str)):
            return True
        elif (isinstance(data, list)):
            for elem in data:
                if (not isinstance(elem, str)):
                    return False
            return True
        else:
            return False

    def ingest(self, data: str | list[str]) -> None:
        if (not self.validate(data)):
            raise ValueError("Error: Data should be an str or a list of str")
        elif (isinstance(data, str)):
            self._storage.insert(0, (self._rank, data))
            self._rank += 1
        elif (isinstance(data, list)):
            for elem in data:
                self._storage.insert(0, (self._rank, elem))
                self._rank += 1


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if (isinstance(data, dict)):
            for key, value in data.items():
                if (not (isinstance(key, str) and isinstance(value, str))):
                    return False
            return True
        elif (isinstance(data, list)):
            for elem in data:
                if (isinstance(elem, (dict))):
                    for key, value in elem.items():
                        if (not (isinstance(key, str) and
                                 isinstance(value, str))):
                            return False
                else:
                    return False
            return True
        else:
            return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if (not self.validate(data)):
            raise ValueError("Error : data should be a dict of string " +
                             "key-value pairs" +
                             ", or a list of that type.")
        elif (isinstance(data, dict)):
            log = ": ".join(data.values())
            self._storage.insert(0, (self._rank, log))
            self._rank += 1
        elif (isinstance(data, list)):
            for elem in data:
                log = ": ".join(elem.values())
                self._storage.insert(0, (self._rank, log))
                self._rank += 1


class DataStream:
    def __init__(self):
        self._procs = []
        self._items_proced = 0
        self._

    def register_processor(self, proc: DataProcessor) -> None:
        self._procs.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for data in stream:
            for proc in self._procs:
                if (proc.validate(data)):
                    proc.ingest(data)
                    break
            else:
                print("DataStream Error: Can't process " +
                      "elemeint in stream:", data)

    def print_processors_stats(self) -> None:
        for 


def main():
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    print()


if __name__ == "__main__":
    main()
