from repl_core.application import get_response, Application
from repl_core import run
from repl_core import print_formatted_text, HTML


app = Application(port=8000, route="/handshake", auto_connect=True)

# advance bar as option to decorator
# provides access to an instantiated bar object as argument in attached/view function 


"""
Declare a function that maps to a simple endpoint
"""
@app.viewer("/handshake",
            "hello {firstname:pierre|paul}",
            help_msg="Say hello to p*"
            )
def hello(firstname):
    print_formatted_text(f"Hello {firstname}")
    print(get_response().content)

"""
Declare a function that maps to a endpoint with parameters
"""
@app.viewer("/greetings/{firstname}/{lastname}",
            "hello_anyone {firstname:_string} {lastname:_string}",
            help_msg="Say hello to anyone"
            )
def hello_anyone(firstname="Jean", lastname="Dupond"):
    print_formatted_text(f"Hello who ? {firstname}")
    print_formatted_text(get_response().content)

"""
A useless function demonstrating file autosuggestion
"""
@app.viewer("/handshake",
            "hello_from_file {myfile:_path}",
            help_msg="Say hello from file"
            )
def hello_from_file(myfile="/path/to/my/file"):
    print(f"Hello who ? {myfile}")
    print(get_response().content)


"""
Declare a function that maps to a endpoint expecting a post data 
The function is only called to prepare the posted data
"""
@app.mutator("/put_stuff",
           "store {id:_number} {name:_string}",
            help_msg="Store stuff"
            )
def store(id=6005, name="Tin_can"):
    print (id, name)
    data_to_post = {"id" : id, "name": name}
    return data_to_post

"""
Declare a function that maps to a endpoint expecting a post data 
with the possibility to post treat the answer as a Requests:Response object
"""
@app.mutator("/put_stuff",
           "store_and_process {id:_number} {name:_string}",
            help_msg="Store stuff"
            )
def store_and_process(id=6005, name="Tin_can"):
    def process(response):
        print_formatted_text(HTML(f"Receiving <ansigreen>{response.content}</ansigreen>"))
    
    data_to_post = {"id" : id, "name": name}
    print_formatted_text(HTML(f"Sending <ansigreen>{data_to_post}</ansired>"))
    return data_to_post, process

run(app)