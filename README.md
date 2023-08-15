# Simple Random Acceess Machine

## Setup

### Standard installation
```shell
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```
### Poetry
```shell
  poetry install
  poetry shell
```

## Start

```shell
  python main.py
```

## Buttons
- New - clear everything
- Step - execute a single step
- Run - execute until `HALT` command
- Delay box - set delay between executing commands during `run`
- Stop - stop `running` program
- Load - load saved program and input values
- Save - save program and input values in .json format

## Commands
- READ - read value from input tape to [0] register
- WRITE - write value from [0] to output
- LOAD val, address - load `val` to `address` register
- ADD val1, val2, address - adding `val1` to `val2` and write to `address`
- SUB val1, val2, address - subtract `val2` from `val1` and write to `address`
- CPY add1, add2 - copy `add1` value to `add2` register
- JNZ val, mark - goto `mark` if val (can be address) > 0
- mark - any value with `:` at the end
- HALT - stop the program

**Note**: different set of commands can be added by 
changing `command_cls` attribute in `Program` class.

## Program Examples
There are some examples of ready programs in /saved_states directory
- max.json
- sum.json
- imul.json
