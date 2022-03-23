class UpdateBaseError(Exception):
    def __init__(self, f_name, *curr_args):
        self.cmd = f_name
        self.call = curr_args       
        super().__init__()
    def __str__(self):
        return f"<ansired>Update Long Pool runtime Error<u>{self.cmd}</u> not a valid argument {self.call}</ansired>"
# TO TEST

class UpdateTupleLengthError(UpdateBaseError):
    def __init__(self, *args):
        super().__init__(*args)
    def __str__(self):
        #return f"<ansired><u>{self.cmd}</u> not a valid argument {self.call}</ansired> <ansigreen><i>{self.expected}</i></ansigreen>"
        return f"<ansired>Update Long Pool runtime Error, update function specified in {self.cmd} return the following non length 3 [{len(self.call)}] tuple: ({self.call})</ansired>"

class UpdateTupleTypeError(UpdateBaseError):
    def __init__(self, pos, fname, *args):
        super().__init__(fname, *args)       
        self.wrong_type = type(args[pos])
        self.wrong_pos = pos
    def __str__(self):
        #return f"<ansired><u>{self.cmd}</u> not a valid argument {self.call}</ansired> <ansigreen><i>{self.expected}</i></ansigreen>"
        return f"<ansired>Update Long Pool runtime Error, update function specified in {self.cmd} return an unexpected type({self.wrong_type}) at pos {self.wrong_pos} of {self.call}</ansired>"
