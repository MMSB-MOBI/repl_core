from typing import Callable, Optional, Tuple, Literal, Any
from xmlrpc.client import Boolean
from requests import get, post, Response
from prompt_toolkit import print_formatted_text, HTML
from .errors import SignatureBaseError, SignatureArgumentNameError
from .helpers import CommandManager
import sys, re, inspect

response = None
"""
signature = {
    "load" : {"fast", "slow"}
}

>>context : load slow path [VALUE PARAMETER]
"""
"""
Coherce content of the return of a user mutator function into
(data_to_post, Response_processor)
"""
def unwrap_data_callable_2uple(d:Any):
    if type(d) == 'tuple' or type(d) == 'list':
        if len(d) == 2:
            if d[1] == 'callable':
                return d
    print("returning d, ans_proc", file=sys.stderr)
    return (d, answer_processor)
            
    
def answer_processor(answer:Response):
    try:
        #d = answer.json()
        content = answer.content
        if answer.status_code != 200:
            print_formatted_text(HTML(f"<ansired>A problem occured <i>{answer.status_code}</i>\n\t{content}</ansired>"))
        else :
            print_formatted_text(HTML(f"<ansigreen>Success<i>{content}</i></ansigreen>"))
    except Exception as e:
        print_formatted_text(HTML(f"<ansired>A problem occured <i>{content}</i></ansired>"))



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

def _connection_test(host="localhost", port=1234, route="/hello")->Boolean:
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
    

    def generate_url(self, f:Callable, url_ressource_specs:str, *args):
        callable_arg_specs = inspect.getfullargspec(f)
        for i_arg, arg_name in enumerate(callable_arg_specs.args):
            value = args[i_arg]          
            url_ressource_specs = url_ressource_specs.replace('{' + arg_name + '}', value)
        url = f"http://{self.host}:{self.port}{url_ressource_specs}"       
        return url
    """
    viewer decorator provides view only on ressources
    GET
    POST?
    """
    def viewer(self, ressource_path:str, prototype:str, help_msg:str):
        def inner_decorator(f):
            self.assert_register(f, prototype, help_msg, ressource_path)

            def wrapped(*args, **kwargs): 
                global response
                url = self.generate_url(f, ressource_path, *args)
                response = get(url)
                print(f"wrapped{url}", file=sys.stderr)             
                ans = f(*args, **kwargs)                
                return ans
            print('decorating', f, 'with argument', ressource_path, file=sys.stderr)
        #return wrapped
            self.viewer_map[f.__name__] = wrapped           
        return inner_decorator


    RequestType=Literal['POST', 'GET']

    """
    viewer decorator provides view only on ressources
    GET
    POST?
    """
    def mutator(self, ressource_path:str, prototype:str, help_msg:str, method='POST'):
        def inner_decorator(f):
            # Register prototype
            self.assert_register(f, prototype, help_msg, ressource_path)
            
            def wrapped(*args, **kwargs):
                # Check and cast *args
                
                datum_to_post, ans_processor =  unwrap_data_callable_2uple(
                                                    f(*args, **kwargs)
                                                )
                url = self.generate_url(f, ressource_path, *args)
                if method == "POST":
                    print(datum_to_post, file=sys.stderr)
                    ans:Response = post(url, json = datum_to_post)
                else: 
                    raise TypeError("method ??")
                return ans_processor(ans)
            self.viewer_map[f.__name__] = wrapped
     
        return inner_decorator

    def assert_register(self, f, prototype, help_msg, ressource_path):
        try:
            self.command_registry.add(prototype, f, comments=help_msg)
            # Check decorated function matches prototype
            self.command_registry.assert_callable(f, ressource_path)
        except SignatureBaseError as e:
            print_formatted_text( HTML(f"<ansired> STARTUP ERROR:\t{str(e)}</ansired>\n") )
            exit()
        
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
            fn = self.get_f_by_symbol(cmd_name)
            _args = self.command_registry.signature_check_and_arg_coherce(fn, cmd_name, *args, **kwargs)    
            _ = fn(*_args, **kwargs)
        except SignatureBaseError as e:
            print_formatted_text(HTML(str(e)))
            return None
        return _
    
    @property
    def auto_suggest(self):
        return self.command_registry.suggester

    @property
    def auto_complete(self):
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
