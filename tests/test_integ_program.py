import pytest

from ram_machine.program import Commands, InputTape, OutputTape, Program, Register


class TestFullProgram:
    @pytest.fixture
    def program(self) -> None:
        return Program(
            command_cls=Commands,
            reg=Register({}),
            input_tape=InputTape([5, 1, 2, 3, 4, 5]),
            output_tape=OutputTape(),
            command_str_list=[""]
        )

    def test_example(self, program: Program) -> None:
        program.command_str_list = [
            "LOAD 2, [0]",
            "JNZ [0], 12345",
            "ADD 2, [0]",
            "12345:",
            "WRITE",
            "HALT",
        ]
        program.exec_many_steps()
        assert program.output_tape.data[0] == 2

    def test_sum(self, program: Program) -> None:
        program.command_str_list = [
            "READ",
            "LOAD 0, [2]",
            "CPY [0], [1]",

            "12345:",
            "READ",
            "ADD [0], [2], [2]",
            "SUB [1], 1, [1]",
            "JNZ [1], 12345",
            "CPY [2], [0]",
            "WRITE",
            "HALT",
        ]
        program.exec_many_steps()
        assert program.output_tape.data[0] == 15

    def test_max(self, program: Program) -> None:
        program.input_tape = InputTape([5, 5, 1, 8, -3, 7])
        program.command_str_list = [
            "READ",
            "LOAD 0, [1]",  # [1] - max_val
            "LOAD 0, [2]",  # [2] - diff
            "LOAD 0, [3]",  # [3] - counter
            "CPY [0], [3]",

            "0:",
            "READ",
            "SUB [1], [0], [2]",
            "JNZ [2], 1",
            "CPY [0], [1]",

            "1:",
            "SUB [3], 1, [3]",
            "JNZ [3], 0",

            "CPY [1], [0]",
            "WRITE",
            "HALT",
        ]
        program.exec_many_steps()
        assert program.output_tape.data[0] == 8

    def test_mul(self, program: Program) -> None:
        program.input_tape = InputTape([28, 11])
        program.command_str_list = [
            "READ",
            "CPY [0], [1]",
            "READ",
            "CPY [0], [2]",
            "LOAD 0, [3]",

            "loop:",
            "ADD [1], [3], [3]",
            "SUB [0], 1, [0]",
            "JNZ [0], loop",

            "CPY [3], [0]",
            "WRITE",
            "HALT",
        ]
        program.exec_many_steps()
        assert program.output_tape.data[0] == 308
