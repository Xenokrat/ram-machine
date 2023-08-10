numeric = int | float


class Register:
    def __init__(self, dict_: dict) -> None:
        for k, v in dict_.items():
            self._validate_key_value(k, v)
        self.__data = dict_

    @property
    def summator(self) -> numeric | None:
        return self[0]

    @summator.setter
    def summator(self, value) -> None:
        self._validate_key_value(0, value)
        self[0] = value

    @summator.getter
    def summator(self) -> numeric | None:
        try:
            return self[0]
        except KeyError:
            return None

    def __setitem__(self, key: int, value: numeric) -> None:
        self._validate_key_value(key, value)
        self.__data[key] = value

    def __getitem__(self, key: int) -> numeric | None:
        self._validate_key_value(key, 0)
        try:
            return self.__data[key]
        except KeyError:
            return None

    def __delitem__(self, key: int):
        self._validate_key_value(key, 0)
        del self.__data[key]

    def _validate_key_value(self, key: int, value: int | float) -> None:
        if not isinstance(key, int):
            raise TypeError(f"key should be int, got {type(key).__name__}")

        if not isinstance(value, (int, float)):
            raise TypeError(
                f"value should be numeric, got {type(value).__name__}"
            )
