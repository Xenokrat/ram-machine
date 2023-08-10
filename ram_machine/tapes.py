numeric = int | float


def validate_numeric_data(value: numeric) -> numeric:
    if not isinstance(value, (int, float)):
        raise TypeError(f"value should be numeric, got {type(value).__name__}")
    return value


class InputTape:
    def __init__(self, data: list[numeric]) -> None:
        for val in data:
            validate_numeric_data(val)
        self.__data = data
        self.current_cell = 0

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: list[numeric]):
        for val in data:
            validate_numeric_data(val)
        self.__data = data

    @data.getter
    def data(self):
        return self.__data

    def read(self) -> numeric | None:
        try:
            res = self.__data[self.current_cell]
            self.current_cell += 1
        except IndexError:
            res = None
        return res


class OutputTape:
    def __init__(self) -> None:
        self.__data: list[numeric] = []

    @property
    def data(self):
        return self.__data

    @data.getter
    def data(self):
        return self.__data

    def write(self, value: numeric) -> None:
        validate_numeric_data(value)
        self.__data.append(value)
