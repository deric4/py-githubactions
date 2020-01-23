from typing import Dict, Optional, Any
from enum import Enum
import os

from githubactions.core.constants import *

CMD_STR = "::"

CommandProperties = Dict[str, str]

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

def add_mask(p: str) -> None:
    """Mask a value in log

    Masking a value prevents a string or variable from being printed in the log.
    Each masked word separated by whitespace is replaced with the * character.
    You can use an environment variable or string for the mask's value.
    """

    print(ADD_MASK_FMT.format(p))


def add_path(path: str) -> None:
    """Add a system path

    Prepends a directory to the system PATH variable for all subsequent actions in the current job.
    The currently running action cannot access the new path variable.
    """

    issue_command('add-path', {}, path)
    os.environ['PATH'] = f"{os.path.sep}".join([path, os.getenv('PATH')])


def add_matcher(p: str) -> None:
    print(ADD_MATCHER_FMT.format(p))


def remove_matcher(p: str) -> None:
    print(REMOVE_MATCHER_FMT.format(p))


def save_state( k, v: str) -> None:
    print(SAVE_STATE_FMT.format(k, v))


def get_input(i: str, options: Dict = {}) -> str:
    i = i.replace(" ", "_")
    i = i.upper()
    i = f'INPUT_{i}'

    val = os.getenv(i) or ''
    if options.get('required') and not val:
        raise ValueError('Input required and not supplied: missing')

    return val.strip()

def group(t: str) -> None:
    print(GROUPT_FMT.format(t))


def end_group() -> None:
    print(END_GROUP_FMT)


def set_env(k: str, v: str) -> None:
    os.environ[k] = v
    issue_command('set-env', {"name": k}, v)


def set_output(k, v: str) -> None:
    issue_command('set-output', {"name": k}, v)


def set_failed(message: str) -> None:
    error(message)


def debug(message: str) -> None:
    issue_command('debug', {}, message)


def error(message: str) -> None:
    issue('error', message)


def warning(message: str) -> None:
    issue('warning', message)


def info(message: str) -> None:
    print(message)


def start_group(name: str) -> None:
    issue('group', name)


def end_group() -> None:
    issue('endgroup')


def save_state(name: str, value, str) -> None:
    issue_command('save-state', {'name': name}, value)


def get_state(name: str) -> str:
    return os.getenv(f'STATE_{name}', '')


def escape(s: str) -> str:
    return s.replace('\r', '%0D').replace('\n', '%0A')

def data_escape(s: str) -> str:
    return s.replace('\r', '%0D').replace('\n', '%0A').replace(']', '%5D').replace(';', '%3B')
