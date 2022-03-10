from typing import Callable, Optional, Tuple
from xmlrpc.client import Boolean
from requests import get
from prompt_toolkit import print_formatted_text, HTML
from .helpers import CommandManager, SignatureBaseError
import sys

from inspect import signature as fn_signature

response = None

from inspect import signature

"""
signature = {
    "load" : {"fast", "slow"}
}

>>context : load slow path [VALUE PARAMETER]
"""


def get_response():
    global response
    return response


def my_decorator(arg):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            print('before function')
            response = f(*args, **kwargs)
            print('after function')
            return response
        print('decorating', f, 'with argument', arg)
        return wrapped
    return inner_decorator

def _exit():
    s = """<skyblue>      .                            .                      .
  .                  .             -)------+====+       .
                           -)----====    ,'   ,'   .                 .
              .                  `.  `.,;___,'                .
                                   `, |____l_
                     _,....------c==]""______ |,,,,,,.....____ _
    .      .        "-:_____________  |____l_|]'''''''''''       .     .
                                  ,'"",'.   `.
         .                 -)-----====   `.   `.         See you space cowboy     
                     .            -)-------+====+       .            .
             .                               .</skyblue>"""
    print_formatted_text(HTML(s))
    #print_formatted_text(HTML(f"\n\n<skyblue></skyblue>"))
    exit(0)

def _connection_test(host, port, route)->Boolean:
    url=f"{host}:{port}{route}"
    try :
        ans = get(f"http://{url}")
        assert ans.status_code == 200
    except Exception as e:
        print_formatted_text(HTML(f"<ansired>Unable to establish connnection at {url}</ansired>"))
        return False
    print_formatted_text(HTML(f"<ansigreen>Successfull connection at {url}</ansigreen>"))
    return True

DEFAULT_COMMANDS = {
    'exit'    :  {
        "target"    : _exit,
        "prototype" : "exit",
        "help_msg" : "Close the interface",
    },
    'connect' : {
        "target"    : _connection_test,
        "help_msg" : "Connect to the service",
        "prototype" : "connect {host:_string} {port:_number} {my_route:_string}"
    }
}

 # NExt step is to add default value for autosuggest !! 
 #"prototype" : "connect {host:_string=120.0.0.1} {port:_number=1234} {my_route:_string=/handshake}"


class Application():
    def __init__(self, host="localhost", port=1234, route="/", auto_connect=False):
        self.host = host
        self.port  = port
        self.handshake_route  = route
        self.viewer_map = {}
        self.default_map = {}
        self.command_registry = CommandManager()
        self.help_is_ready = False
        self.is_connected = False

        for basic_cmd, data_cmd in DEFAULT_COMMANDS.items():
            print(f"Adding to default command registry {basic_cmd}",file=sys.stderr)
            self.command_registry.add(data_cmd["prototype"], data_cmd["target"], data_cmd["help_msg"])
    
            self.default_map[basic_cmd] = data_cmd["target"]

        if auto_connect:
            self.is_connected = self.launch('connect', self.host, self.port, self.handshake_route)
    
    def help(self, cmd)->Tuple[str,str]:
        proto_input_string, proto_comments = self.command_registry.help(cmd)
        print(f"HH {proto_input_string} // {proto_comments}", file=sys.stderr)
        return proto_input_string, proto_comments

    def isa(self, cmd):
        return cmd in self.available_commands

    """
    viewer decorator provides view only on ressources
    GET
    POST?
    We must validate kwargs
    """
    def viewer(self, ressource_path:str, prototype:str, help_msg:str):
        def inner_decorator(f):
            # Register prototype
            self.command_registry.add(prototype, f, comments=help_msg)
            # Check decorated function matches prototype
            self.command_registry.assert_callable(f)

            # Not Needed TO CHEK THOUGH
            #if f.__name__ in self.viewer_map:
            #    raise KeyError(f"{f.__name__} is already registred")
            #self.command_registry.add(f.__name__, f)

                                      
            #self.help_registry[f.__name__] = help_msg
        
            # Checking arguments validity
            
            #sprint(f"viewer registred inspecti signature{fn_signature(f)}", file=sys.stderr)

            def wrapped(*args, **kwargs): 
                global response ## expression parser
                url = f"http://{self.host}:{self.port}{ressource_path}"
                response = get(url)
                print(f"wrapped{url}", file=sys.stderr)             
                ans = f(*args, **kwargs)
                print('after function')
                return ans
            print('decorating', f, 'with argument', ressource_path, file=sys.stderr)
        #return wrapped
            self.viewer_map[f.__name__] = wrapped
     
        return inner_decorator
        
    #def viewer_execute(self, v_cmd_symbol, *args, **kwargs):
    #    print(f"FIRE!! {v_cmd_symbol}", file=sys.stderr)
        # Get signature decorator
    #    to_launch = self.command_registry.signatureCheck(self.viewer_map[v_cmd_symbol])
    #    to_launch(*args, **kwargs)

    @property
    def available_commands(self):
        return self.command_registry.available_commands
    
    def get_f_by_symbol(self, sym)->Optional[Callable]:
        if sym in self.viewer_map:
            return self.viewer_map[sym]
        if sym in self.default_map:
            return self.default_map[sym]
        print(f"no callable named!! {sym}", file=sys.stderr)
        return None

    def launch(self, cmd_name, *args, **kwargs):# ONLY VIEWER FOR NOW

        print(f"launch!! {cmd_name}", file=sys.stderr)

        try :
        #    if cmd_name in self.viewer_map:
            fn = self.get_f_by_symbol(cmd_name)
            self.command_registry.signatureCheck(fn, cmd_name, *args, **kwargs)
            _ = fn(*args, **kwargs)
        except SignatureBaseError as e:
            print(str(e), file=sys.stderr)
            print_formatted_text(HTML(str(e)))
            return None
        return _
    
    @property
    def auto_suggest(self):
        return self.command_registry.get_customAutoSuggest()

    @property
    def completer(self):
        return self.command_registry.completer
"""
viewer decorator provides mutations on ressources
GET
POST
"""
def mutator(arg):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            print('before function')
            response = f(*args, **kwargs)
            print('after function')
            return response
        print('decorating', f, 'with argument', arg)
        return wrapped
    return inner_decorator
