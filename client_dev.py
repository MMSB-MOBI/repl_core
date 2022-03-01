from inspect import signature
import repl_dev.dec_lib
from repl_dev.dec_lib import get_response, Application#viewer_map, viewer_execute


app = Application(port=8000)
@app.viewer("/handshake",
            signature = { "pierre", "paul" },
            help="hello pierre|paul"
            )
def hello():
    print("metier IN")
    print(get_response().content)
    print("metier OUT")

app.viewer_execute("hello")
app.viewer_execute("hello")
