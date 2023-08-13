from unittest.mock import MagicMock

import pytest

from ram_machine.command import Commands
from ram_machine.register import Register
from ram_machine.tapes import InputTape, InputTapeError, OutputTape


class TestCommands:
    def test_read(self):
        itape = InputTape([1, 2, -5])
        reg = Register({})
        Commands.read(itape, reg)
        assert reg.summator == 1
        Commands.read(itape, reg)
        assert reg.summator == 2
        Commands.read(itape, reg)
        assert reg.summator == -5
        with pytest.raises(InputTapeError):
            Commands.read(itape, reg)

    def test_write(self):
        otape = OutputTape()
        reg = Register({})
        reg.summator = 1
        Commands.write(otape, reg)
        reg.summator = 2
        Commands.write(otape, reg)
        assert otape.data == [1, 2]

    def test_load(self):
        reg = Register({})
        Commands.load(reg, 10, 1)
        assert reg[1] == 10

    def test_add(self):
        reg = Register({})
        val1 = 2
        val2 = -3
        Commands.add(reg, val1, val2, 1)
        assert reg[1] == -1

    def test_sub(self):
        reg = Register({})
        val1 = 2
        val2 = -3
        Commands.sub(reg, val1, val2, 1)
        assert reg[1] == 5

    def test_cpy(self):
        reg = Register({1: 5, 2: 10})
        Commands.cpy(reg, 2, 1)
        assert reg[1] == 10

    def test_halt(self):
        program = MagicMock()
        program.running = True
        Commands.halt(program)
        assert program.running is False
