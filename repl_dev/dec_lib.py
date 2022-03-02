from requests import get
from prompt_toolkit import print_formatted_text, HTML
from .helpers import CommandManager 

response = None

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


"""
signatures = {
    'clist': { 
        'vector',
        'tree',
        'culled',
        'all'
    },
    'connect' : None,    
    'build'   : None,
    'load'    : None,
    'exit'    : None,
    'delete'  : None,
    'help'    : {'clist', 'connect',  'load', 'exit', 'delete', 'build'}

}

completer = NestedCompleter.from_nested_dict(signatures)
"""
def _exit():
    print_formatted_text(HTML(f"\n\n<skyblue>See you space cowboy</skyblue>"))
    exit(0)



DEFAULT_COMMANDS = {
    'exit'    :  {
        "target"    : _exit,
        "paramTypes" : None,
        "help" : f"Close the interface\nUsage: exit",
        "signature" : None,
        "usage" : "exit"
    }
}

class Application():
    def __init__(self, host="localhost", port=1234):
        self.host = host
        self.port   = port
        self.viewer_map = {}
        self.help_registry = {}
        self.usage_registry = {}
        self.command_registry = CommandManager()

        for basic_cmd, data_cmd in DEFAULT_COMMANDS.items():
            self.command_registry.add(basic_cmd, **data_cmd)
            self.help_registry[basic_cmd] = data_cmd["help"]
            self.usage_registry[basic_cmd] = data_cmd["usage"]

    def isa(self, cmd):
        return cmd in self.available_commands

    """
    viewer decorator provides view only on ressources
    GET
    POST?
    We must validate kwargs
    """
    def viewer(self, ressource_path, signature = None, help=None, paramTypes=None, usage = None):
        def inner_decorator(f):
            if f.__name__ in self.viewer_map:
                raise KeyError(f"{f.__name__} is already registred")
            self.command_registry.add(f.__name__, target=f, 
                                      signature=signature, 
                                      paramTypes=paramTypes, 
                                      help=help,
                                      usage=usage)
            self.help_registry[f.__name__] = help
            self.usage_registry[f.__name__] = usage
            def wrapped(*args, **kwargs): 
                global response ## expression parser
                url = f"http://{self.host}:{self.port}{ressource_path}"
                response = get(url)
                print(f"wrapped{url}")               
                ans = f(*args, **kwargs)
                print('after function')
                return ans
            print('decorating', f, 'with argument', ressource_path)
        #return wrapped
            self.viewer_map[f.__name__] = wrapped
     
        return inner_decorator
                        
    def viewer_execute(self, v_cmd_symbol, *args, **kwargs):
        print(f"FIRE!! {v_cmd_symbol}")
        self.viewer_map[v_cmd_symbol](*args, **kwargs)

    @property
    def available_commands(self):
        return self.command_registry.available_commands

    def launch(self, cmd_name, *args, **kwargs):# ONLY VIEWER FOR NOW
        self.viewer_map[cmd_name](*args, **kwargs)

    def help(self, cmd_name):
        return (self.help_registry[cmd_name], self.usage_registry[cmd_name])
    
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
