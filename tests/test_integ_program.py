from ram_machine.program import Commands, InputTape, OutputTape, Program, Register


class TestFullProgram:
    def test_sum_program(self) -> None:
        program = Program(
            command_cls=Commands,
            reg=Register({}),
            input_tape=InputTape([1, 2, 3, 4, 5]),
            output_tape=OutputTape(),
            command_str_list=[""]
        )
