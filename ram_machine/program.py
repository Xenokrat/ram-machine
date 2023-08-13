import re

from ram_machine.command import Commands
from ram_machine.register import Register
from ram_machine.tapes import InputTape, OutputTape

allowed_commands_with_args = {
    "LOAD",
    "ADD",
    "SUB",
    "CPY",
    "JNZ",
}
allowed_commands_no_args = {
    "READ",
    "WRITE",
    "HALT",
}


class NonValidCommand(Exception):
    pass


class Program:

    def __init__(
        self,
        command_cls: Commands,
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

    def parse_command(self) -> None:
        command_str = self.command_str_list[self.current_command]
        parsed = command_str.split(" ", 1)
        if len(parsed) == 1 and parsed[0][-1] == ":":
            pass
        elif len(parsed) == 1 and parsed[0] in allowed_commands_no_args:
            match parsed[0]:
                case "READ":
                    self.do_read()
                case "WRITE":
                    self.do_write()
                case "HALT":
                    self.do_halt()
                case _:
                    raise NonValidCommand(f"\"{command_str}\" is not a valid command")
        elif len(parsed) == 2 and parsed[0] in allowed_commands_with_args:
            command, args = parsed
            match command.upper():
                case "LOAD":
                    self.do_load(args)
                case "ADD":
                    self.do_add(args)
                case "SUB":
                    self.do_sub(args)
                case "CPY":
                    self.do_cpy(args)
                case "JNZ":
                    self.do_jnz(args)
                case _:
                    raise NonValidCommand(f"\"{command_str}\" is not a valid command")
        else:
            raise NonValidCommand(f"\"{command_str}\" is not a valid command")
        self.current_command += 1

    def do_read(self) -> None:
        if self.input_tape.current_cell >= len(self.input_tape.data):
            self.do_halt()
            return
        self.command_cls.read(self.input_tape, self.reg)

    def do_write(self) -> None:
        self.command_cls.write(self.output_tape, self.reg)

    def do_halt(self) -> None:
        self.command_cls.halt(self)

    def do_load(self, args: str) -> None:
        try:
            str_value, str_address = args.split(",")
        except ValueError:
            raise NonValidCommand(f"\"{args}\" are invalid arguments for LOAD")
        value = self.parse_const_arg(str_value)
        address = self.parse_address_arg(str_address)
        self.command_cls.load(self.reg, value, address)

    def do_add(self, args: str) -> None:
        try:
            str_value1, str_value2, str_address = args.split(",")
        except ValueError:
            raise NonValidCommand(f"\"{args}\" are invalid arguments for ADD")
        value1 = self.parse_const_arg(str_value1)
        value2 = self.parse_const_arg(str_value2)
        address = self.parse_address_arg(str_address)
        self.command_cls.add(self.reg, value1, value2, address)

    def do_sub(self, args: str) -> None:
        try:
            str_value1, str_value2, str_address = args.split(",")
        except ValueError:
            raise NonValidCommand(f"\"{args}\" are invalid arguments for SUB")
        value1 = self.parse_const_arg(str_value1)
        value2 = self.parse_const_arg(str_value2)
        address = self.parse_address_arg(str_address)
        self.command_cls.sub(self.reg, value1, value2, address)

    def do_cpy(self, args: str) -> None:
        try:
            str_address1, str_address2 = args.split(",")
        except ValueError:
            raise NonValidCommand(f"\"{args}\" are invalid arguments for CPY")
        address1 = self.parse_address_arg(str_address1)
        address2 = self.parse_address_arg(str_address2)
        self.command_cls.cpy(self.reg, address1, address2)

    def do_jnz(self, args: str) -> None:
        try:
            str_value, str_mark = args.split(",")
            mark = str_mark.strip() + ":"
        except ValueError:
            raise NonValidCommand(f"\"{args}\" are invalid arguments for JNZ")
        value = self.parse_const_arg(str_value)
        self.command_cls.jnz(self, value, mark)

    def parse_const_arg(self, arg: str) -> int:
        arg = arg.strip()
        if arg.isdigit():
            return int(arg)
        if match := re.match(r"\[(-?\d+)\]", arg):
            return self.reg[int(match.group(1))]
        if match := re.match(r"\[\[(-?\d+)\]\]", arg):
            address = self.reg[int(match.group(1))]
            return self.reg[address]
        raise NonValidCommand(f"\"{arg}\" is invalid argument")

    def parse_address_arg(self, arg: str) -> int:
        arg = arg.strip()
        if match := re.match(r"\[(-?\d+)\]", arg):
            return int(match.group(1))
        if match := re.match(r"\[\[(-?\d+)\]\]", arg):
            return self.reg[int(match.group(1))]
        raise NonValidCommand(f"\"{arg}\" is invalid argument")

    def exec_one_step(self) -> None:
        self.running = True
        self.parse_command()

    def exec_many_steps(self) -> None:
        self.running = True
        while self.running:
            self.parse_command()
