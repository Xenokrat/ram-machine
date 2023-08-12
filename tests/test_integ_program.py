import pytest

from ram_machine.program import Commands, InputTape, OutputTape, Program, Register


class TestFullProgram:
    @pytest.fixture
    def program(self) -> None:
        return Program(
            command_cls=Commands,
            reg=Register({}),
            input_tape=InputTape([1, 2, 3, 4, 5]),
            output_tape=OutputTape(),
            command_str_list=[""]
        )

    def test_example(self, program: Program) -> None:
        program.command_str_list = [
            "LOAD 2, [0]",
            "JNZ [0], 12345",
            "ADD 2, [0]",
            "12345",
            "WRITE",
            "HALT",
        ]
        program.exec_many_steps()
        assert program.output_tape.data[0] == 2
        
    def test_sum(self, program: Program) -> None:
        program.command_str_list = [
            "LOAD 0, [1]",
            "0",
            "READ",
            "ADD [0], [1], [1]",
            "JNZ 1, 0",
            "WRITE",
            "HALT",
        ]
        program.exec_many_steps()
        assert program.output_tape.data[0] == 15
        
