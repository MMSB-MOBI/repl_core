from requests import get
from prompt_toolkit import print_formatted_text, HTML
from . import helpers

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
DEFAULT_PROCESSES = {
    'exit'    :  {
        "_target"    : _exit,
        "paramTypes" : None,
        "help" : f"Close the interface\nUsage: exit"
    }
}


class Application():
    def __init__(self, host="localhost", port=1234):
        self.host = host
        self.port   = port
        self.viewer_map = {}
        self.help_registry = {}
        self.command_registry = helpers.CommandModelManager()
    
    def isa(self, cmd):
        return cmd in self.available_commands

    """
    viewer decorator provides view only on ressources
    GET
    POST?
    We must validate kwargs
    """
    def viewer(self, ressource_path, signature = None, help=None, paramType=None, help=None):
        def inner_decorator(f):
            if f.__name__ in self.viewer_map:
                raise KeyError(f"{f.__name__} is already registred")
            self.command_registry.add(f.__name__, _target=f, signature=signature, paramType=paramType, help=help)
            self.help_registry[f.__name__] = help
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
                        

    def viewer_execute(self, v_cmd_symbol):
        print(f"FIRE!! {v_cmd_symbol}")
        self.viewer_map[v_cmd_symbol]()

    @property
    def available_commands(self):
        return self.command_registry.available_commands

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
