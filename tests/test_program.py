from unittest.mock import patch

import pytest

from ram_machine.command import NonValidCommand
from ram_machine.program import (
    Commands,
    DeadlockError,
    InputTape,
    OutputTape,
    Program,
    Register,
)


class TestProgram:

    @pytest.fixture
    def mock_program(self):
        reg = Register({})
        itape = InputTape([1, 2, 3, 4, 5])
        otape = OutputTape()
        return Program(Commands, reg, itape, otape, [])

    def test_parse_command(self, mock_program: Program) -> None:
        mock_program.command_str_list = ["LOAD 2, [0]"]
        assert mock_program.parse_command() == ("load", "2, [0]")

    @patch("ram_machine.command.Commands.load")
    def test_command_called(self, mock_load) -> None:
        program = Program(
            Commands, Register({}), InputTape([]), OutputTape, ["LOAD 2, [0]"]
        )
        program.exec_command()
        mock_load.assert_called_with(program, "2, [0]")

    # Testing Commands inside Program
    def test_do_read(self, mock_program: Program) -> None:
        mock_program.command_str_list = ["READ",]
        mock_program.exec_command()
        assert mock_program.reg.summator == 1

    def test_do_write(self, mock_program: Program) -> None:
        mock_program.command_str_list = ["WRITE"]
        mock_program.reg.summator = 5
        mock_program.exec_command()
        assert mock_program.output_tape.data[0] == 5

    def test_do_halt(self, mock_program: Program) -> None:
        mock_program.command_str_list = ["HALT",]
        mock_program.running = True
        mock_program.exec_command()
        assert mock_program.running is False

    def test_load(self, mock_program: Program) -> None:
        mock_program.command_str_list = ["LOAD 5, [1]", "LOAD 1, [2]"]
        mock_program.exec_command()
        assert mock_program.reg[1] == 5
        mock_program.exec_command()
        assert mock_program.reg[2] == 1

    def test_load_fail(self, mock_program: Program) -> None:
        mock_program.command_str_list = ["LOAD 5, [1], 1",]
        with pytest.raises(NonValidCommand):
            mock_program.exec_command()

    def test_add(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        mock_program.command_str_list = ["ADD 5, [[0]], [3]"]
        mock_program.exec_command()
        assert mock_program.reg[3] == 1

    def test_add_fail(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        mock_program.command_str_list = ["ADD 5, [[0]]"]
        with pytest.raises(NonValidCommand):
            mock_program.exec_command()

    def test_sub(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        mock_program.command_str_list = ["SUB 5, [[0]], [3]"]
        mock_program.exec_command()
        assert mock_program.reg[3] == 9

    def test_cpy(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        mock_program.command_str_list = ["CPY [1], [0]"]
        mock_program.exec_command()
        assert mock_program.reg.summator == -4

    def test_jnz_gt_zero(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        command_str_list = ["JNZ [0], 1234", "LOAD 2, [0]", "READ", "1234:", "WRITE"]
        mock_program.command_str_list = command_str_list
        mock_program.exec_command()
        mock_program.exec_command()
        assert mock_program.output_tape.data[0] == 1
        assert mock_program.reg.summator == 1

    def test_jnz_lt_zero(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        command_str_list = ["JNZ [1], 1234", "LOAD 2, [0]", "READ", "1234", "WRITE"]
        mock_program.command_str_list = command_str_list
        mock_program.exec_command()
        mock_program.exec_command()
        assert mock_program.reg.summator == 2

    def test_deadlock(self, mock_program: Program) -> None:
        mock_program.command_str_list = [
            "deadlock:",
            "LOAD 2, [0]",
            "JNZ [0], deadlock",
            "WRITE",
            "HALT"
        ]
        with pytest.raises(DeadlockError):
            mock_program.exec_many_steps()
