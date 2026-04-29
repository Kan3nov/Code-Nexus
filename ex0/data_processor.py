from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self._storage = []
        self._rank = 0

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


def main():
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")
    num_proc = NumericProcessor()
    print("Trying to validate input '42':", num_proc.validate(42))
    print("Trying to validate input 'Hello':", num_proc.validate("Hello"))
    print("Test invalid ingestion of string 'foo' without  prior validation:")
    try:
        num_proc.ingest("foo")
    except ValueError as e:
        print(e)
    num_data = [1, 2, 3, 4, 5]
    print("Processing data:", num_data)
    num_proc.ingest(num_data)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = num_proc.output()
        print(f"Numeric value {rank}:", value)
    print()

    print("Testing Text Processor...")
    text_proc = TextProcessor()
    print("Trying to validate input '42':", text_proc.validate(42))
    text_data = ['Hello', "Nexus", 'World']
    print("Processing data:", text_data)
    text_proc.ingest(text_data)
    print("Extracting 1 value...")
    rank, value = text_proc.output()
    print(f"Text value {rank}:", value)
    print()
    print("Testing Log Processor...")
    log_proc = LogProcessor()
    print("Trying to validate input 'Hello':", log_proc.validate('Hello'))
    log_data = [{'log_level': 'NOTICE', 'log_message':
                 'Connection to server'}, {'log_level': 'ERROR', 'log_message':
                'Unauthorized access!!'}]
    print("Processing data: ", log_data)
    log_proc.ingest(log_data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log_proc.output()
        print(f"Log entry {rank}:", value)


if __name__ == "__main__":
    main()
