import pytest

from ram_machine.tapes import InputTape, OutputTape, numeric, validate_numeric_data


class TestValidate:
    def test_validate_numeric_data(value: numeric) -> None:
        assert validate_numeric_data(5) == 5
        assert validate_numeric_data(1.2) == 1.2

    def test_validate_numeric_data_fail(value: numeric) -> None:
        with pytest.raises(TypeError):
            validate_numeric_data('5')


class TestInputTape:
    def test_init(self) -> None:
        data = [1, 2.2, -5.53]
        itape = InputTape(data)
        assert itape._InputTape__data == [1, 2.2, -5.53]

    def test_init_fail(self) -> None:
        data = ['1', '2.2', '-5.53']
        with pytest.raises(TypeError):
            InputTape(data)

    def test_getter(self) -> None:
        data = [1, 2.2, -5.53]
        itape = InputTape(data)
        assert itape.data == [1, 2.2, -5.53]

    def test_setter(self) -> None:
        data = [1, 2.2, -5.53]
        itape = InputTape(data)
        itape.data = [4, 5, 6]
        assert itape._InputTape__data == [4, 5, 6]

    def test_read(self) -> None:
        data = [1, 2.2, -5.53]
        itape = InputTape(data)
        assert itape.current_cell == 0
        assert itape.read() == 1
        assert itape.current_cell == 1
        assert itape.read() == 2.2
        assert itape.current_cell == 2
        assert itape.read() == -5.53
        assert itape.current_cell == 3
        assert itape.read() is None
        assert itape.current_cell == 3


class TestOutputTape:
    def test_write(self) -> None:
        otape = OutputTape()
        otape.write(1)
        otape.write(2.2)
        assert otape.data == [1, 2.2]

    def test_write_fail(self) -> None:
        otape = OutputTape()
        with pytest.raises(TypeError):
            otape.write('1')
