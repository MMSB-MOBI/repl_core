from prompt_toolkit import PromptSession, print_formatted_text, HTML
from prompt_toolkit.key_binding import KeyBindings
import re

from .dec_lib import Application
from .helpers import customAutoSuggest

INV_PROMPT = ">>>"

def getPrompt():
    return INV_PROMPT

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
    if not executor.isa(cmd):
        print_formatted_text(HTML(f"<ansired><b>{cmd}</b> is not a valid command</ansired>\nType <u>help</u> for a list of available commands"))
        return False

    _ = executor.process(cmd, *_)

def _help(cmd):
    if cmd is None:
        msg = ', '.join([ f"<u>{c}</u>" for c in executor.availbleCmd ])
        msg = f"Available command: {msg}"
        print_formatted_text(HTML(msg))
    elif not executor.isa(cmd):
        print_formatted_text(HTML(f"<ansired><b>{cmd}</b> is not a valid command</ansired>\nType <u>help</u> for a list of available commands"))
    else:
        msg = executor.help(cmd)
        #print("##", msg, "##")
        print_formatted_text(HTML(f"<u>{cmd}</u>:\n{msg}"))




def run(application_object):

    kb = KeyBindings()
    @kb.add('c-c')
    def exit_(event):
        """
        Pressing Ctrl-Q will exit the user interface.
        """
    #_exit()
        application_object.process('exit')

    session = PromptSession()
    
    while True:
        answer = session.prompt(getPrompt(), 
                                completer=application_object.completer, 
                                auto_suggest=customAutoSuggest(),
        key_bindings=kb )
        digest(answer)
        #print('You said: %s' % answer)
    exit(1)