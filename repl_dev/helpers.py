from inspect import signature
import inspect
from xmlrpc.client import Boolean
from prompt_toolkit import print_formatted_text, HTML
from .interactive_prompt import customCompleter, customAutoSuggest

from .models import CommandModel
from .prototyper import PrototypeCollector, Prototype
from typing import Union
import re, sys
from pathlib import Path


## AUTO SUGGEST AND VALIDATE ?

class CommandManager():
    def __init__(self):
        self.prototyper  = PrototypeCollector()
        self._completer  = customCompleter(self.prototyper)
        self._suggester  = customAutoSuggest(self.prototyper)
        
    def assert_callable(self, f:callable):
        if not f.__name__ in self.available_commands:
            raise KeyError(f"{f.__name__} is not known")
        p_names = self.prototyper.get_cmd_all_param_names(f.__name__)
        c_params = list(signature(f).parameters)
        if not c_params and not p_names:
            return True
        if len(p_names) != len(c_params):
            raise TypeError(f"{f.__name__} signature ({c_params})does not match function definition{p_names}")
        for a,b in zip(p_names, c_params):
            if a != b:
                raise TypeError(f"{f.__name__} signature ({c_params}) parameters names dont match function definition{p_names}")
        
        return True

    def help(self, cmd_name):
        _:Prototype = self.prototyper[cmd_name]
        return _.input_str, _.comments
    
    @property
    def available_commands(self):
        return self.prototyper.commands

    def add(self, proto_string , target, comments=None):
        callable_arg_specs = inspect.getfullargspec(target)
        print(f"Adding {proto_string} prototype callee is :\n {callable_arg_specs}",file=sys.stderr)
        
        proto_obj:Prototype = self.prototyper.add(proto_string, callable_arg_specs.defaults\
                                                , comments)

    def signatureCheck(self,fn, fn_symbol, *args, **kwargs):
        print(f"Checking signature of {fn_symbol} {fn.__name__}", file=sys.stderr)
        fn_sig_types = self.prototyper.get_cmd_all_param_types(fn_symbol)
        fn_sig_values = self.prototyper.get_cmd_all_param_values(fn_symbol)
        fn_sig_arg_names = self.prototyper.get_cmd_all_param_names(fn_symbol)
        print(f"=> {fn_sig_types}", file=sys.stderr)
        print(f"=> {fn_sig_values}", file=sys.stderr)

        # NO optional count for now
        if fn_sig_types is None:
            if len(args) > 0:
                raise SignatureEmptyError(fn_symbol, args, fn_sig_arg_names)
            return True

        if len(args) != len(fn_sig_types):
            raise SignatureLengthError(fn_symbol, args, fn_sig_arg_names)

        for i, (sig_type, sig_value) in enumerate( zip(fn_sig_types, fn_sig_values) ):
            callee_value = args[i]
            for t in sig_type:
                print(f"??{t}", file=sys.stderr)
                if t == "keyword" and callee_value in sig_value:
                    continue 
                if t == "number" and  str(callee_value).isnumeric() :
                    continue 
                if t == "path" and  Path(callee_value).exists() :
                    continue 
                if t == "string":
                    continue
                raise SignatureArgumentTypeError(i, fn_symbol, args, fn_sig_types)
        return True
       
    @property
    def suggester(self):
        return self._suggester
    
    @property
    def completer(self):
        return self._completer


class SignatureBaseError(Exception):
    def __init__(self, cmd, current, expected):
        self.cmd = cmd
        self.call = current
        self.expected = expected
        super().__init__()
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> not a valid argument {self.call}</ansired> <ansigreen><i>{self.expected}</i></ansigreen>"

class SignatureLengthError(SignatureBaseError):
    def __init__(self, *args):
        super().__init__(*args)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> unepxected number or arguments {self.call}</ansired> <ansigreen><i>{self.expected}</i></ansigreen>"

class SignatureEmptyError(SignatureBaseError):
    def __init__(self, *args):
        super().__init__(*args)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> Not emty arguments {self.call}</ansired> <ansigreen>{self.expected}</ansigreen>"
        

class SignatureArgumentTypeError(SignatureBaseError):
    def __init__(self, param_num,*args):
        self.p_num = param_num
        super().__init__(*args)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> not a valid type at pos {self.p_num}: {self.call}</ansired> <ansigreen><i>{self.expected}</i></ansigreen>"

class SignatureCallError(SignatureBaseError):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)#self.message)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> is not a valid command call </ansired> <ansigreen><i>{self.availbleCmd}</i></ansigreen>"

class SignatureWrongSubCommandError(SignatureBaseError):
    def __init__(self, cmd, signature, *subCmd):
        super().__init__(cmd, signature)#self.message)
        self.badSubCmd = subCmd
    def __str__(self):
        return f"<ansired>{self.cmd} was called with wrong subcommand <u>{self.badSubCmd}</u> instead of <i>{self.subCmd}</i></ansired>"

class SignatureEmptySubCommandError(SignatureBaseError):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)#self.message)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> empty argument list instead of <i>{self.subCmd}</i></ansired>"

import glob 
from os.path import commonprefix
def pathSuggest(string):
    _ = glob.glob(f"{string}*")
    return re.sub(rf'^{string}', '',commonprefix(_) )