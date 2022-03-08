from inspect import signature
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from .models import CommandModel
from typing import Union
import re, sys

class CommandManager():
    def __init__(self):
        self._command_map = {}
        self._signatures = {
            'help' : set()
        }
    def __iter__(self):
        for t in self._command_map.items():
            yield t
   
    def __getitem__(self, cmd)->CommandModel:
        if cmd in self._command_map:
            return self._command_map[cmd]
        raise KeyError(f"no command {cmd}")
        
    @property
    def completer(self):
        return  NestedCompleter.from_nested_dict(self._signatures)
    
    @property
    def available_commands(self):
        return self._signatures.keys()

    def add(self, symbol, signature=None, **kwargs):
        print(f"Adding {kwargs} signature",file=sys.stderr)
        self._command_map[symbol] = CommandModel(**kwargs)
        self._signatures[symbol]  = signature
        self._signatures["help"].add(symbol)
        # Should be made recursive if needed

    def signatureCheck(self,fn, fn_symbol, *args, **kwargs):
        
        print(f"Checking signature of {fn_symbol}", file=sys.stderr)
        cmd = fn_symbol
        err_egg = (cmd, self._signatures)
        #cur_sig = self.completer
   
        if not cmd in self.available_commands:
            raise SignatureCallError(*err_egg)
        if self._signatures[cmd] is None:
            return fn(*args, **kwargs)
        availArg = set([ subCmd for subCmd in self._signatures[cmd] ])
    
        _ = set(args) - set(availArg)
        if not args:
            raise SignatureEmptySubCommandError(*err_egg)        
        if _:
            raise SignatureWrongSubCommandError(*err_egg, *_)        
        return fn(*args, **kwargs)
       
    def get_customAutoSuggest(self):
        return customAutoSuggest(self)

class customAutoSuggest(AutoSuggest):
    def __init__(self, bound_command_manager):
        super().__init__()
        self.command_manager = bound_command_manager

    def update(self, cmd):
        self.currentCommand = cmd

    def get_suggestion(self, buffer, document):
        """ Given the current first word on prompt
            tries to find matching arguments
        """
        print("###", document.text, file = sys.stderr )
        if re.match('^[\S]*$', document.text):
            return Suggestion("")
        
        
        curr_prompt_elem = re.findall('([\S]+)', document.text)
       # print(f"# {len(curr_prompt_elem)} my i suggest ?\n")
        try: 
            data:Union[CommandModel, None] = self.command_manager[ curr_prompt_elem[0] ] ## MM
            if len(curr_prompt_elem) == 1: # return basic suggestion
                _ = " ".join( data.usage.split()[1:] )
                return Suggestion(f" {_}")
            # We are in arguments, here we check if a path is desirable
            curr_arg_type_num = len(curr_prompt_elem) - 2
            if data.paramTypes:
                if data.paramTypes[curr_arg_type_num] == "path":
                    return Suggestion( pathSuggest(curr_prompt_elem[-1]) )
            
        except KeyError as e:
            print(f"{curr_prompt_elem[0]} not a valid key\n", file=sys.stderr) 
            #return Suggestion("!!!")
        return Suggestion("")

class SignatureBaseError(Exception):
    def __init__(self, cmd, signatures):
        self.cmd = cmd
        self.availbleCmd = set(signatures.keys())
        if cmd in self.availbleCmd:
            self.subCmd = signatures[cmd] if type(signatures[cmd]) == set else set(signatures[cmd].keys())
        super().__init__()
        
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