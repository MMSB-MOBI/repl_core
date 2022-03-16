


class SignatureBaseError(Exception):
    def __init__(self, cmd, current, expected):
        self.cmd = cmd
        self.call = current
        self.expected = expected
        super().__init__()
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> not a valid argument {self.call}</ansired> <ansigreen><i>{self.expected}</i></ansigreen>"
# TO TEST

class SignatureDefinitionError(SignatureBaseError):
    def __init__(self, *args):
        super().__init__(*args)
    def __str__(self):
        #return f"<ansired><u>{self.cmd}</u> not a valid argument {self.call}</ansired> <ansigreen><i>{self.expected}</i></ansigreen>"
        return f"{self.cmd} signature ({self.call})does not match function definition{self.expected}"

# TO TEST
class SignatureLengthError(SignatureBaseError):
    def __init__(self, *args):
        super().__init__(*args)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> unexpected number or arguments {self.call}</ansired> <ansigreen><i>{self.expected}</i></ansigreen>"

# TO TEST
class SignatureArgumentTypeError(SignatureBaseError):
    def __init__(self, param_num, *args):
        self.p_num = param_num
        super().__init__(*args)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> not a valid type at pos {self.p_num}: {self.call}</ansired> <ansigreen><i>{self.expected}</i></ansigreen>"

# TO TEST
class SignatureArgumentNameError(SignatureBaseError):
    def __init__(self, param_num, *args):
        self.p_num = param_num
        super().__init__(*args)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> not a valid name at pos {self.p_num}: {self.call}</ansired> <ansigreen><i>{self.expected}</i></ansigreen>"


class SignatureRessourceError(SignatureBaseError):
    def __init__(self, url_elem, *args):
        self.url_elem = url_elem
        super().__init__(*args)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> specify url parameters <b>{self.url_elem}</b> is lacking in function definition</ansired>:<ansigreen><i>{self.expected}</i></ansigreen>"

class SignatureOverrideError(SignatureBaseError):
    def __init__(self, *args):
        super().__init__(*args)
    def __str__(self):
        return f"<ansired>Multiple definiton attempt at command named <u>{self.cmd}</u> </ansired>"

class SignatureEmptyError(SignatureBaseError):
    def __init__(self, *args):
        super().__init__(*args)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> Not emty arguments {self.call}</ansired> <ansigreen>{self.expected}</ansigreen>"
        

class SignatureArgumentTypeError(SignatureBaseError):
    def __init__(self, param_num,*args):
        self.p_num = param_num
        super().__init__(*args)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> not a valid type at pos {self.p_num}: {self.call}</ansired> <ansigreen><i>{self.expected}</i></ansigreen>"

class SignatureCallError(SignatureBaseError):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)#self.message)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> is not a valid command call </ansired> <ansigreen><i>{self.availbleCmd}</i></ansigreen>"

class SignatureWrongSubCommandError(SignatureBaseError):
    def __init__(self, cmd, signature, *subCmd):
        super().__init__(cmd, signature)#self.message)
        self.badSubCmd = subCmd
    def __str__(self):
        return f"<ansired>{self.cmd} was called with wrong subcommand <u>{self.badSubCmd}</u> instead of <i>{self.subCmd}</i></ansired>"

class SignatureEmptySubCommandError(SignatureBaseError):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)#self.message)
    def __str__(self):
        return f"<ansired><u>{self.cmd}</u> empty argument list instead of <i>{self.subCmd}</i></ansired>"
