import pytest

from ram_machine.register import Register


class TestRegister:
    def test_validate_key_value(self) -> None:
        reg = Register({})
        reg._validate_key_value(1, 1)

    def test_validate_key_value_fail(self) -> None:
        reg = Register({})
        with pytest.raises(TypeError):
            reg._validate_key_value(4.23, "word")

    def test_create_reg(self) -> None:
        reg = Register({1: 1, 2: 2.4, -3: -51})
        assert reg._Register__data == {1: 1, 2: 2.4, -3: -51}

    def test_not_create_reg(self) -> None:
        with pytest.raises(TypeError):
            reg = Register({'1': '2', 4.2: '3'})
            assert reg

    def test_set_item(self) -> None:
        reg = Register({})
        reg[0] = 10
        reg[10] = 10
        assert reg[0] == 10
        assert reg[10] == 10

    def test_set_summator(self) -> None:
        reg = Register({})
        reg.summator = 10
        assert reg[0] == 10

    def test_cannot_set_value(self) -> None:
        with pytest.raises(TypeError):
            reg = Register({})
            reg[0] = '10'

    def test_cannot_set_key(self) -> None:
        with pytest.raises(TypeError):
            reg = Register({})
            reg[1.2] = 10

    def test_summator(self) -> None:
        reg = Register({0: 0})
        reg.summator == 0

    def test_delitem(self) -> None:
        reg = Register({0: 0})
        assert reg[0] == 0
        del reg[0]
        assert reg[0] is None

    def test_getitem(self) -> None:
        reg = Register({0: 0})
        assert reg[0] == 0
        assert reg[1] is None
