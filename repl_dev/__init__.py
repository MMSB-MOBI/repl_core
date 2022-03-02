from prompt_toolkit import PromptSession, print_formatted_text, HTML
from prompt_toolkit.key_binding import KeyBindings
import re

from .dec_lib import Application
from .helpers import customAutoSuggest

INV_PROMPT = ">>>"

def getPrompt():
    return INV_PROMPT

def run(app:Application):

    def digest(_input):
        if re.match('^[\s]*$', _input) :
            #print("Empty string")
            return
        _ = _input.split()
        #print("input::", _)
        
        cmd = _.pop(0)
        if cmd == 'help':
            _help(_[0] if _ else None)
            return True
        if not app.isa(cmd):
            print_formatted_text(HTML(f"<ansired><b>{cmd}</b> is not a valid command</ansired>\nType <u>help</u> for a list of available commands"))
            return False

        _ = app.launch(cmd, *_)

    def _help(cmd):
        if cmd is None:
            msg = ', '.join([ f"<u>{c}</u>" for c in app.available_commands ])
            msg = f"Available command: {msg}"
            print_formatted_text(HTML(msg))
        elif not app.isa(cmd):
            print_formatted_text(HTML(f"<ansired><b>{cmd}</b> is not a valid command</ansired>\nType <u>help</u> for a list of available commands"))
        else:
            cmd_help, cmd_use = app.help(cmd)
            
            print_formatted_text(HTML(f"<u>{cmd}</u>:\n{cmd_help}"))
            if cmd_use:
                print_formatted_text(HTML(f"usage: <i>{cmd_use}</i>"))




    kb = KeyBindings()
    @kb.add('c-c')
    def exit_(event):
        """
        Pressing Ctrl-Q will exit the user interface.
        """
    #_exit()
        app.launch('exit')

    session = PromptSession()
    
    while True:
        answer = session.prompt(getPrompt(), 
                                completer=app.completer, 
                                auto_suggest=app.auto_suggest,
        key_bindings=kb )
        digest(answer)
        #print('You said: %s' % answer)
    exit(1)