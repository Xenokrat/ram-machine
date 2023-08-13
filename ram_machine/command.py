from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ram_machine.program import Program
    from ram_machine.register import Register
    from ram_machine.tapes import InputTape, OutputTape


class Commands:

    @staticmethod
    def read(itape: InputTape, reg: Register) -> None:
        val = itape.read()
        if val is not None:
            reg.summator = val

    @staticmethod
    def write(otape: OutputTape, reg: Register) -> None:
        val = reg.summator
        if val is not None:
            otape.write(val)

    @staticmethod
    def load(reg: Register, value: int, address: int) -> None:
        reg[address] = value

    @staticmethod
    def add(reg: Register, value1: int, value2: int, address: int) -> None:
        reg[address] = round(value1 + value2, 2)

    @staticmethod
    def sub(reg: Register, value1: int, value2: int, address: int) -> None:
        reg[address] = round(value1 - value2, 2)

    @staticmethod
    def cpy(reg: Register, address1: int, address2: int) -> None:
        reg[address2] = reg[address1]

    @staticmethod
    def jnz(prog: Program, value: int, mark: str) -> None:
        if value > 0:
            prog.current_command = prog.command_str_list.index(mark)

    @staticmethod
    def halt(prog: Program) -> None:
        prog.running = False
