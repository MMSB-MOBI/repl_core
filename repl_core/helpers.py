from inspect import signature
import inspect
from xmlrpc.client import Boolean
from prompt_toolkit import print_formatted_text, HTML
from .interactive_prompt import customCompleter, customAutoSuggest

from .models import CommandModel
from .prototyper import PrototypeCollector, Prototype
from typing import Union, Optional, List
import re, sys
from pathlib import Path
from .errors import SignatureDefinitionError, SignatureLengthError, \
    SignatureArgumentNameError, SignatureEmptyError, SignatureArgumentTypeError, \
    SignatureRessourceError

## AUTO SUGGEST AND VALIDATE ?

class CommandManager():
    def __init__(self):
        self.prototyper  = PrototypeCollector()
        self._completer  = customCompleter(self.prototyper)
        self._suggester  = customAutoSuggest(self.prototyper)
        
    def assert_callable(self, f:callable, url_path:str):
        if not f.__name__ in self.available_commands:
            raise KeyError(f"{f.__name__} is not known")
        p_names = self.prototyper.get_cmd_all_param_names(f.__name__)
        c_params = list(signature(f).parameters)
        print(f"Asserting callable {f.__name__}", file=sys.stderr)
        if not c_params and not p_names:
            return True
        if len(p_names) != len(c_params):
            raise SignatureLengthError(f.__name__, c_params, p_names)
        for i, (a,b) in enumerate(zip(p_names, c_params)):
            if a != b:
               raise SignatureArgumentNameError(i, f.__name__, c_params, p_names)

        for url_elem in re.findall("\{([^\}]+)\}", url_path):            
            if not url_elem in p_names:
                raise SignatureRessourceError(url_elem, f.__name__, c_params, p_names)

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

    def signature_check_and_arg_coherce(self,fn, fn_symbol, *args, **kwargs)->Optional[List[Union[str,float,int]]]:
        print(f"Checking signature of {fn_symbol} {fn.__name__}", file=sys.stderr)
        fn_sig_types = self.prototyper.get_cmd_all_param_types(fn_symbol)
        fn_sig_values = self.prototyper.get_cmd_all_param_values(fn_symbol)
        fn_sig_arg_names = self.prototyper.get_cmd_all_param_names(fn_symbol)
        print(f"=> {fn_sig_types}", file=sys.stderr)
        print(f"=> {fn_sig_values}", file=sys.stderr)
        coherced_args = []
        # NO optional count for now
        if fn_sig_types is None:
            if len(args) > 0:
                raise SignatureEmptyError(fn_symbol, args, fn_sig_arg_names)
            return []

        if len(args) != len(fn_sig_types):
            raise SignatureLengthError(fn_symbol, args, fn_sig_arg_names)

        for i, (sig_type, sig_value) in enumerate( zip(fn_sig_types, fn_sig_values) ):
            callee_value = args[i]
            coherced     = False
            for t in sig_type:
                print(f"??{t}", file=sys.stderr)
                if t == "keyword" and callee_value in sig_value:
                    if not coherced:
                        coherced_args.append(callee_value)
                        coherced = True
                    continue 
                if t == "number" and  str(callee_value).isnumeric() :
                    if not coherced:
                        coherced_args.append(
                            float(callee_value) if '.' in str(callee_value) else int(callee_value)
                        )
                        coherced = True
                    continue 
                if t == "path" and  Path(callee_value).exists() :
                    if not coherced:
                        coherced_args.append(callee_value)
                        coherced = True
                    continue                         
                if t == "string":
                    if not coherced:
                        coherced_args.append(callee_value)
                        coherced = True
                    continue
                raise SignatureArgumentTypeError(i, fn_symbol, args, fn_sig_types)

        return coherced_args
    def type_coherce_args(self, fn_symbol, *iargs):
        fn_sig_types = self.prototyper.get_cmd_all_param_types(fn_symbol)

    @property
    def suggester(self):
        return self._suggester
    
    @property
    def completer(self):
        return self._completer



import glob 
from os.path import commonprefix
def pathSuggest(string):
    _ = glob.glob(f"{string}*")
    return re.sub(rf'^{string}', '',commonprefix(_) )