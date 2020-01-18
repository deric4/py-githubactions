from typing import Dict, Optional, Any
from enum import Enum


CMD_STR = "::"

CommandProperties = Dict[str, str]

def escape(s: str) -> str:
    return s.replace('\r', '%0D').replace('\n', '%0A')

def data_escape(s: str) -> str:
    return s.replace('\r', '%0D').replace('\n', '%0A').replace(']', '%5D').replace(';', '%3B')

class ExitCodes(Enum):
    Success = 0
    Failure = 1

class Command:
    def __init__(self, command: str = None, properties: CommandProperties = {}, message: str = None ) -> None:
        self.command = command or 'missing.command'
        self.properties = properties
        self.message = message or ''

    def __repr__(self) -> str:
        cmd_str = CMD_STR + self.command
        
        first = True
        if self.properties:
            cmd_str += ' '
            for k, v in self.properties.items():
                if self.properties.get(k):
                    if first:
                        first = False
                    else:
                        cmd_str += ','

                    cmd_str += f'{k}={data_escape(v)}'

        cmd_str += CMD_STR

        message = self.message or ''

        cmd_str += data_escape(message)

        return cmd_str

def issue_command(command: str, properties: CommandProperties, message: str) -> None:
    cmd = Command(command, properties, message)
    print(cmd)

def issue(name: str, message: str = '') -> None:
    issue_command(name, {}, message)

