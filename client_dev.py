from inspect import signature
from repl_dev.application import get_response, Application#viewer_map, viewer_execute
from repl_dev import run

app = Application(port=8000, route="/handshake", auto_connect=True)

# callback for post-treatment of mutator decorator ?

# advance bar as option to decorator
# provides access to an instantiated bar object as argument in attached/view function 
@app.viewer("/handshake",
            "hello {firstname:pierre|paul}",
            help="Say hello to p*"
            )
def hello(firstname):
    print(f"Hello {firstname}")
    print(get_response().content)
    print("metier OUT")


## @app.mutator -> different decorator
"""
@app.viewer("/put_stuff",
            signature = None,
            help="load a file of interest",
            paramTypes=["path"],
            usage = 'load yourFile'
            )
def load():
    print("LOAD metier IN")
    print(get_response().content)
    print("Load metierout")
"""
"""
createCustomCompleter

"""

"""
@app.viewer_as_proto("/load_with_param",
            prototype = "load {foo_param:cull|raw} {source:_file} {bar_threshold:_number}",
            help      = "load data with god-like accuracy",
            )
def load():
    print("LOAD metier IN")
    print(get_response().content)
    print("Load metierout")
"""


#app.viewer_execute("hello")
#app.viewer_execute("hello")

run(app)