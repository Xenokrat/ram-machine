class InputTapeError(Exception):
    pass


def validate_int_data(value: int) -> int:
    if not isinstance(value, int):
        raise TypeError(f"value should be int, got {type(value).__name__}")
    return value


class InputTape:
    def __init__(self, data: list[int]) -> None:
        for val in data:
            validate_int_data(val)
        self.__data = data
        self.current_cell = 0

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: list[int]):
        for val in data:
            validate_int_data(val)
        self.__data = data

    @data.getter
    def data(self):
        return self.__data

    def read(self) -> int:
        try:
            res = self.__data[self.current_cell]
        except IndexError:
            raise InputTapeError("READ non-existing value")
        self.current_cell += 1
        return res


class OutputTape:
    def __init__(self) -> None:
        self.__data: list[int] = []

    @property
    def data(self):
        return self.__data

    @data.getter
    def data(self):
        return self.__data

    def write(self, value: int) -> None:
        validate_int_data(value)
        self.__data.append(value)
