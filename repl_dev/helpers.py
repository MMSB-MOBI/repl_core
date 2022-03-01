from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from models import CommandModel

import re
""" WHAT IS A SIGNATURE :
SMTG TAHT COMPLIES TO THAT ?
  'exit'    :  {
        "_target"    : _exit,
        "paramTypes" : None,
        "help" : f"Close the interface\nUsage: exit"
    }

    AKA 
    class CommandModel(BaseModel):
    _target: Callable
    paramTypes: Union[List,None]
    runningParams : Boolean
    help: str
    SO IT HAS TO BE BUILDT IN THE @app.viewer context
"""

class CommandModelManager():
    def __init__(self):
        self._command_map = {}

    @property
    def completer(self):
        return  NestedCompleter.from_nested_dict(self._command_map)
    @property
    def available_commands(self):
        return self.completer.keys()

    def add(self, symbol, **kwargs):
        print(f"Adding {kwargs} signature")
        self._command_map[symbol] = CommandModel(kwargs)
        # Should be made recursive if needed
        
#@decorator TO CONFIRM IN CONTEXT 
    def signatureCheck(self, fn):
    
        def wrapped(*args, kwargs):
            cur_sig = self.completer
            cmd = fn.__name__
            if not cmd in cur_sig:
                raise SignatureCallError(cmd)
            if cur_sig[cmd] is None:
                return fn(*args, **kwargs)
            availArg = set([ subCmd for subCmd in cur_sig[cmd] ])
        
            _ = set(args) - set(availArg)
            if not args:
                raise SignatureEmptySubCommandError(cmd, cur_sig)        
            if _:
                raise SignatureWrongSubCommandError(cmd, *_)        
            return fn(*args, **kwargs)
        return wrapped
    def get_customAutoSuggest(self):
        return customAutoSuggest(self)

class customAutoSuggest(AutoSuggest):
    def __init__(self, bound_signature_manager):
        super().__init__()
        self.signature_manager = bound_signature_manager
    def update(self, cmd):
        self.currentCommand = cmd

    def get_suggestion(self, buffer, document):
        if len(str(document.text) == 0):
            return Suggestion("")
        # Scan bound_signature_manager for longest match
        for cmd in signature_manager.a
        if str(document.text).startswith('connect'):
            _ = re.findall('([\S]+)', document.text)
            if len(_) == 1:
                return Suggestion(" 127.0.0.1 1234")
            if len(_) == 2:
                return Suggestion(" 1234")
            
        #if str(document.text).startswith('list'):
        #    return Suggestion(" all|vector|culled|tree")
        if str(document.text).startswith('load'):
            _ = re.findall('([\S]+)', document.text)
            if len(_) > 1:
                return Suggestion( pathSuggest(_[-1]) )

        return Suggestion("")

class SignatureBaseError(Exception):
    def __init__(self, cmd, cur_sig):
        self.cmd = cmd
        self.availbleCmd = set(cur_sig.keys())
        if cmd in self.availbleCmd:
            self.subCmd = cur_sig[cmd] if type(cur_sig[cmd]) == set else set(cur_sig[cmd].keys())
        super().__init__()
        
class SignatureCallError(SignatureBaseError):
    def __init__(self, cmd):
        super().__init__(cmd)#self.message)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> is not a valid command call </ansired> <ansigreen><i>{self.availbleCmd}</i><ansigreen>"

class SignatureWrongSubCommandError(SignatureBaseError):
    def __init__(self, cmd, *subCmd):
        super().__init__(cmd)#self.message)
        self.badSubCmd = subCmd
    def __str__(self):
        return f"<ansired>{self.cmd} was called with wrong subcommand <u>{self.badSubCmd}</u> instead of <i>{self.subCmd}</i></ansired>"

class SignatureEmptySubCommandError(SignatureBaseError):
    def __init__(self, cmd):
        super().__init__(cmd)#self.message)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> empty argument list instead of <i>{self.subCmd}</i></ansired>"


import glob 
from os.path import commonprefix
def pathSuggest(string):
    _ = glob.glob(f"{string}*")
    return re.sub(rf'^{string}', '',commonprefix(_) )