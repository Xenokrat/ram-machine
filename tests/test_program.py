from unittest.mock import MagicMock

import pytest

from ram_machine.program import (
    Commands,
    InputTape,
    NonValidCommand,
    OutputTape,
    Program,
    Register,
    DeadlockError,
)


class TestProgram:

    @pytest.fixture
    def mock_program(self):
        reg = Register({})
        itape = InputTape([1, 2, 3, 4, 5])
        otape = OutputTape()
        return Program(Commands, reg, itape, otape, [])

    def test_parsed_command_args(self, mock_program: Program) -> None:
        command_str_list = ["JNZ [0], 12345",]
        mock_program.command_str_list = command_str_list
        mock_program.do_jnz = MagicMock()
        mock_program.parse_command()
        mock_program.do_jnz.assert_called_with("[0], 12345")

    def test_parsed_command_no_args(self, mock_program: Program) -> None:
        command_str_list = ["READ",]
        mock_program.command_str_list = command_str_list
        mock_program.do_read = MagicMock()
        mock_program.parse_command()
        mock_program.do_read.assert_called()

    def test_parsed_command_mark(self, mock_program: Program) -> None:
        command_str_list = ["12345:",]
        mock_program.command_str_list = command_str_list
        assert mock_program.current_command == 0
        mock_program.parse_command()
        assert mock_program.current_command == 1

    def test_parsed_command_fail(self, mock_program: Program) -> None:
        command_str_list = ["READ 1,2,3",]
        mock_program.command_str_list = command_str_list
        with pytest.raises(NonValidCommand):
            mock_program.parse_command()

    def test_do_read(self, mock_program: Program) -> None:
        command_str_list = ["READ",]
        mock_program.command_str_list = command_str_list
        mock_program.parse_command()
        assert mock_program.reg.summator == 1

    def test_do_write(self, mock_program: Program) -> None:
        command_str_list = ["WRITE"]
        mock_program.command_str_list = command_str_list
        mock_program.reg.summator = 5
        mock_program.parse_command()
        assert mock_program.output_tape.data[0] == 5

    def test_do_halt(self, mock_program: Program) -> None:
        command_str_list = ["HALT",]
        mock_program.command_str_list = command_str_list
        mock_program.running = True
        mock_program.parse_command()
        assert mock_program.running is False

    def test_parse_const_arg(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: 5, -1: 10, 5: 100})
        assert mock_program.parse_const_or_address_arg("5") == 5
        assert mock_program.parse_const_or_address_arg("[-1] ") == 10
        assert mock_program.parse_const_or_address_arg("[[1]]") == 100

    def test_parse_const_arg_fail(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: 5, -1: 10, 5: 100})
        with pytest.raises(NonValidCommand):
            mock_program.parse_const_or_address_arg("[[1]")

    def test_parse_address_arg(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: 5, -1: 10, 5: 100})
        assert mock_program.parse_address_arg("[-1]") == -1
        assert mock_program.parse_address_arg("[[1]] ") == 5

    def test_parse_address_arg_fail(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: 5, -1: 10, 5: 100})
        with pytest.raises(NonValidCommand):
            mock_program.parse_const_or_address_arg("[[1]")
        with pytest.raises(NonValidCommand):
            mock_program.parse_address_arg("5")

    def test_do_load(self, mock_program: Program) -> None:
        mock_program.reg = Register({})
        mock_program.do_load("5, [1]")
        assert mock_program.reg[1] == 5
        mock_program.do_load("[1], [2]")
        assert mock_program.reg[2] == 5

    def test_do_load_fail(self, mock_program: Program) -> None:
        mock_program.reg = Register({})
        with pytest.raises(NonValidCommand):
            mock_program.do_load("5, [1], 1")

    def test_do_add(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        mock_program.do_add("5, [[0]], [3]")
        assert mock_program.reg[3] == 1

    def test_do_add_fail(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        with pytest.raises(NonValidCommand):
            mock_program.do_add("5, [[0]]")

    def test_do_sub(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        mock_program.do_sub("5, [[0]], [3]")
        assert mock_program.reg[3] == 9

    def test_do_cpy(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        mock_program.do_cpy("[1], [0]")
        assert mock_program.reg.summator == -4

    def test_do_jnz_gt_zero(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        command_str_list = ["JNZ [0], 1234", "LOAD 2, [0]", "READ", "1234:", "WRITE"]
        mock_program.command_str_list = command_str_list
        mock_program.parse_command()
        mock_program.parse_command()
        assert mock_program.output_tape.data[0] == 1
        assert mock_program.reg.summator == 1

    def test_do_jnz_lt_zero(self, mock_program: Program) -> None:
        mock_program.reg = Register({0: 1, 1: -4})
        command_str_list = ["JNZ [1], 1234", "LOAD 2, [0]", "READ", "1234", "WRITE"]
        mock_program.command_str_list = command_str_list
        mock_program.parse_command()
        mock_program.parse_command()
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
