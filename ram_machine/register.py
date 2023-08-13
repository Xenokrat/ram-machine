class RegisterError(Exception):
    pass


class Register:
    def __init__(self, dict_: dict) -> None:
        for k, v in dict_.items():
            self._validate_key_value(k, v)
        self.__data = dict_

    @property
    def summator(self) -> int:
        return self[0]

    @summator.setter
    def summator(self, value) -> None:
        self._validate_key_value(0, value)
        self[0] = value

    @summator.getter
    def summator(self) -> int:
        return self[0]

    def __setitem__(self, key: int, value: int) -> None:
        self._validate_key_value(key, value)
        self.__data[key] = value

    def __getitem__(self, key: int) -> int:
        self._validate_key_value(key, 0)
        try:
            return self.__data[key]
        except KeyError:
            raise RegisterError("Trying to get non-existing value from register")

    def __delitem__(self, key: int):
        self._validate_key_value(key, 0)
        try:
            del self.__data[key]
        except RegisterError:
            raise RegisterError("Trying to delete non-existing value from register")

    def _validate_key_value(self, key: int, value: int) -> None:
        if not isinstance(key, int):
            raise TypeError(f"key should be int, got {type(key).__name__}")

        if not isinstance(value, int):
            raise TypeError(
                f"value should be int, got {type(value).__name__}"
            )
