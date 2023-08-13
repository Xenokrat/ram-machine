import pytest

from ram_machine.tapes import InputTape, InputTapeError, OutputTape, validate_int_data


class TestValidate:
    def test_validate_int_data(value: int) -> None:
        assert validate_int_data(5) == 5

    def test_validate_int_data_fail(value: int) -> None:
        with pytest.raises(TypeError):
            validate_int_data('5')


class TestInputTape:
    def test_init(self) -> None:
        data = [1, 2, -5]
        itape = InputTape(data)
        assert itape._InputTape__data == [1, 2, -5]

    def test_init_fail(self) -> None:
        data = ['1', '2', '-5']
        with pytest.raises(TypeError):
            InputTape(data)

    def test_getter(self) -> None:
        data = [1, 2, -5]
        itape = InputTape(data)
        assert itape.data == [1, 2, -5]

    def test_setter(self) -> None:
        data = [1, 2, -5]
        itape = InputTape(data)
        itape.data = [4, 5, 6]
        assert itape._InputTape__data == [4, 5, 6]

    def test_read(self) -> None:
        data = [1, 2, -5]
        itape = InputTape(data)
        assert itape.current_cell == 0
        assert itape.read() == 1
        assert itape.current_cell == 1
        assert itape.read() == 2
        assert itape.current_cell == 2
        assert itape.read() == -5
        assert itape.current_cell == 3
        with pytest.raises(InputTapeError):
            itape.read()


class TestOutputTape:
    def test_write(self) -> None:
        otape = OutputTape()
        otape.write(1)
        otape.write(2)
        assert otape.data == [1, 2]

    def test_write_fail(self) -> None:
        otape = OutputTape()
        with pytest.raises(TypeError):
            otape.write('1')
