from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ram_machine.program import Program


class NonValidCommand(Exception):
    pass


class Commands:

    @staticmethod
    def mark(program: Program, args: str | None) -> None:
        program.current_command += 1

    @staticmethod
    def read(program: Program, args: str | None) -> None:
        val = program.input_tape.read()
        if val is not None:
            program.reg.summator = val
        program.current_command += 1

    @staticmethod
    def write(program: Program, args: str | None) -> None:
        val = program.reg.summator
        if val is not None:
            program.output_tape.write(val)
        program.current_command += 1

    @staticmethod
    def load(program: Program, args: str | None) -> None:
        if args is None:
            raise NonValidCommand("got no arguments")
        try:
            str_const, str_address = args.split(",")
        except ValueError:
            raise NonValidCommand(f"\"{args}\" are invalid arguments for LOAD")
        const = program.parse_const_arg(str_const)
        address = program.parse_address_arg(str_address)
        print(f"Const {const}, address {address}")
        program.reg[address] = const
        program.current_command += 1

    @staticmethod
    def add(program: Program, args: str | None) -> None:
        if args is None:
            raise NonValidCommand("got no arguments")
        try:
            str_val1, str_val2, str_address = args.split(",")
        except ValueError:
            raise NonValidCommand(f"\"{args}\" are invalid arguments for ADD")
        value1 = program.parse_const_or_address_arg(str_val1)
        value2 = program.parse_const_or_address_arg(str_val2)
        address = program.parse_address_arg(str_address)
        program.reg[address] = value1 + value2
        program.current_command += 1

    @staticmethod
    def sub(program: Program, args: str | None) -> None:
        if args is None:
            raise NonValidCommand("got no arguments")
        try:
            str_val1, str_val2, str_address = args.split(",")
        except ValueError:
            raise NonValidCommand(f"\"{args}\" are invalid arguments for SUB")
        value1 = program.parse_const_or_address_arg(str_val1)
        value2 = program.parse_const_or_address_arg(str_val2)
        address = program.parse_address_arg(str_address)
        program.reg[address] = value1 - value2
        program.current_command += 1

    @staticmethod
    def cpy(program: Program, args: str | None) -> None:
        if args is None:
            raise NonValidCommand("got no arguments")
        try:
            str_address1, str_address2 = args.split(",")
        except ValueError:
            raise NonValidCommand(f"\"{args}\" are invalid arguments for CPY")
        address1 = program.parse_address_arg(str_address1)
        address2 = program.parse_address_arg(str_address2)
        program.reg[address2] = program.reg[address1]
        program.current_command += 1

    @staticmethod
    def jnz(program: Program, args: str | None) -> None:
        if args is None:
            raise NonValidCommand("got no arguments")
        try:
            str_value, str_mark = args.split(",")
            mark = str_mark.strip() + ":"
        except ValueError:
            raise NonValidCommand(f"\"{args}\" are invalid arguments for JNZ")
        program.check_deadlock(mark)
        value = program.parse_const_or_address_arg(str_value)
        if value > 0:
            program.current_command = program.command_str_list.index(mark) + 1
        else:
            program.current_command += 1

    @staticmethod
    def halt(prog: Program, args: str | None) -> None:
        prog.reg.clear()
        prog.current_command = 0
        prog.input_tape.current_cell = 0
        prog.running = False
