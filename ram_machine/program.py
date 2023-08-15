import re
from typing import Any, Type

from ram_machine.command import Commands
from ram_machine.register import Register
from ram_machine.tapes import InputTape, OutputTape


class NonValidProgram(Exception):
    pass


class DeadlockError(Exception):
    pass


class Program:

    def __init__(
        self,
        command_cls: Type[Commands],
        reg: Register,
        input_tape: InputTape,
        output_tape: OutputTape,
        command_str_list: list[str],
        current_command: int = 0,
    ) -> None:
        self.command_cls = command_cls
        self.reg = reg
        self.input_tape = input_tape
        self.output_tape = output_tape
        self.command_str_list = command_str_list
        self.current_command = current_command
        self.running: bool = False
        self.deadlock_checker: dict[str, Any] = dict()

    def parse_command(self) -> tuple[str, str | None]:
        command_str = self.command_str_list[self.current_command]
        parsed = command_str.split(" ", 1)
        command = parsed[0].strip().lower()
        args = parsed[1].strip() if len(parsed) > 1 else None
        # Mark
        if command[-1] == ":":
            return "mark", None
        if not hasattr(self.command_cls, command):
            raise NonValidProgram(f"\"{command}\" not implemented")
        return command, args

    def exec_command(self) -> None:
        command, args = self.parse_command()
        getattr(self.command_cls, command)(self, args)

    def parse_const_arg(self, arg: str) -> int:
        arg = arg.strip()
        if arg.isdigit():
            return int(arg)
        raise NonValidProgram(f"\"{arg}\" is invalid argument")

    def parse_const_or_address_arg(self, arg: str) -> int:
        arg = arg.strip()
        if arg.isdigit():
            return int(arg)
        if match := re.match(r"\[(-?\d+)\]", arg):
            return self.reg[int(match.group(1))]
        if match := re.match(r"\[\[(-?\d+)\]\]", arg):
            address = self.reg[int(match.group(1))]
            return self.reg[address]
        raise NonValidProgram(f"\"{arg}\" is invalid argument")

    def parse_address_arg(self, arg: str) -> int:
        arg = arg.strip()
        if match := re.match(r"\[(-?\d+)\]", arg):
            return int(match.group(1))
        if match := re.match(r"\[\[(-?\d+)\]\]", arg):
            return self.reg[int(match.group(1))]
        raise NonValidProgram(f"\"{arg}\" is invalid argument")

    def exec_one_step(self) -> None:
        self.running = True
        self.exec_command()

    def exec_many_steps(self) -> None:
        self.running = True
        while self.running:
            self.exec_command()

    def check_deadlock(self, mark: str) -> None:
        if mark in self.deadlock_checker:
            if self.deadlock_checker[mark] == self.reg:
                raise DeadlockError("Program faced a deadlock!")
        self.deadlock_checker[mark] = self.reg.copy()
