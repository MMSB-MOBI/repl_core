
from prompt_toolkit import print_formatted_text, HTML

#from ..helpers import signatureCheck, signatureCheck
#from .mutators import load, delete, build
#from .viewers import clist
from .connect import Connector, getPrompt

from pydantic import BaseModel, ValidationError, validator
from typing import Callable, Union, List
from xmlrpc.client import Boolean

import sys

"""
class ExecutorBaseError(Exception):
    def __init__(self, symbol):
        self.typings = cmd
        self.availbleCmd = set(signatures.keys())
        if cmd in availbleCmd:
            self.subCmd = signatures[cmd] if type(signatures[cmd]) == set else set(signatures[cmd].keys())
        super().__init__()
        
class ExecutorParameterNumberError(SignatureBaseError):
    def __init__(self, cmd):
        super().__init__(cmd)#self.message)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> is not a valid command call </ansired> <ansigreen><i>{self.availbleCmd}</i><ansigreen>"

class ExecutorParameterNumberError(SignatureBaseError):
    def __init__(self, cmd):
        super().__init__(cmd)#self.message)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> is not a valid command call </ansired> <ansigreen><i>{self.availbleCmd}</i><ansigreen>"
"""


class CommandModel(BaseModel):
    _target: Callable
    paramTypes: Union[List,None]
    runningParams : Boolean
    help: str
"""
    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v
"""

class Executor():
    def __init__(self, command_pool = None):
        
        if not command_pool:
            print("WARNING NO COMMAND POOL")
            self.executor = { }
        
        else :
            self.executor = { key : CommandModel(desc) for key, desc in command_pool.items() }
        
        if not connect in self.executor:
            self._connector = Connector()
            print("Adding base connect", file=sys.stderr)
            self.executor["connect"] = self._connector.get_specs

        print(self.executor)


    @property
    def availbleCmd(self):
        for k in self.executor:
            yield k
        
    def isa(self, cmd):
        return cmd in self.executor
    
    def help(self, cmd):
        return self.executor[cmd]["help"]

    def process(self, cmd, *args):
        if not self.isa(cmd):
            raise ValueError(f"{cmd} is not a valid command {self.executor.keys()}")
        fn = self.executor[cmd]["_target"]
        try:
            self.checkTypes(cmd, *args)
            fn(*args)
        except Exception as e:
            print_formatted_text(HTML(e))
            return False
        return True

    def checkTypes(self, symbol, *args):
        _ = self.executor[symbol]
        typeArgs = _["paramTypes"]
        if typeArgs is None:
            return True
        
        if len(args) < len(typeArgs) or\
            (len(args) > len(typeArgs) and _["runningParams"]) :
            raise TypeError(f"<ansired>{symbol} excepts {len(typeArgs)} argument(s)</ansired>")
""" GIVING UP ON PARAM TYPE CHECKING...
        for i, carg in enumerate(args):
            ctype=type(carg)
            j = i if i < len(typeArgs) else len(typeArgs) - 1
            _type = typeArgs[j]
            
            if ctype != _type:
                _type = str(_type).replace('<', '').replace('>', '').replace("'", "")
                raise TypeError(f"<ansired>{symbol} argument {carg} wrongs types should be {_type}</ansired>")
                #print(f"<ansired>{symbol} argument {carg} has wrong {ctype}</ansired>")
                #raise TypeError(f"<ansired>{symbol} argument {carg} has wrong {ctype}</ansired>")
"""
def _exit():
    print_formatted_text(HTML(f"\n\n<skyblue>See you space cowboy</skyblue>"))
    exit(0)






