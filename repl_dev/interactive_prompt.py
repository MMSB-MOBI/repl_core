from dataclasses import field
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.completion import Completer, Completion
import re,sys

import glob 
from os.path import commonprefix
import os

def path_suggest(string):
    print([_ for _ in os.scandir()], file=sys.stderr)
    _ = glob.glob(f"{string}*")
    print(f"globee;globa |{string}*| => {_}", file=sys.stderr)
    return re.sub(rf'^{string}', '',commonprefix(_) )


def grep_last_arg_field(line):
    
    m = re.findall('([\s]+[\S]*)', line)
    if not m:
        return None, None, None

    seed = m[-1]
    offset = len(seed.replace(" ", ""))
    return seed, offset, len(m) - 1

class customCompleter(Completer):
    def __init__(self, bound_prototyper):
        super().__init__()    
        self.bound_prototyper = bound_prototyper
    def get_completions(self, document, complete_event):
        """ Given the current first word on prompt
            tries to find matching arguments
        """
        print(f"Calling complter on following line :: >{document.text}<",file=sys.stderr)
        curr_prompt_elem = re.findall('([\S]+)', document.text)
        # 1st filed aka command suggestion
        if re.match("^[\S]+$", document.text):   
            offset = -1 * len(curr_prompt_elem[0])    
            for maybe_asked_cmd in self.bound_prototyper.get_match_cmd(curr_prompt_elem[0]):
                yield Completion(maybe_asked_cmd, start_position=offset,
                                style='bg:ansiyellow fg:ansiblack')
        # Other fields aka keyword suggestion
        else:
            print("Other field suggestion ???", file = sys.stderr)
            curr_last_field, offset, n_arg = grep_last_arg_field(document.text)

            print(f"customCompleter::curr_last_field, offset, n_arg: ({curr_last_field}, {offset}, {n_arg})", file = sys.stderr)
            if curr_last_field:
                print(f"CLF>{curr_last_field}<", file=sys.stderr)
                _ = self.bound_prototyper.get_cmd_default_values_at(curr_prompt_elem[0], n_arg)
                print(f"##DFV {_} (from : {curr_prompt_elem[0]}, {n_arg})", file=sys.stderr)
                if _ is None:
                    print(f"[ERROR-get_completion]Follwing prompt bug : >{document.text}<", file=sys.stderr)
                    return
                if len(_) > 1:
                    print("Autocompleting w/ mutliple keywords", _, file=sys.stderr)
                    for keyword in _:
                        if keyword.startswith( curr_last_field.strip() ):
                            print(f"Yielding {keyword} w/ offset {offset}", file=sys.stderr)
                            yield Completion(keyword, start_position=(-1)*offset)
                            print("coucou", file=sys.stderr)

class customAutoSuggest(AutoSuggest):
    def __init__(self, bound_prototyper):
        super().__init__()    
        self.bound_prototyper = bound_prototyper
    def update(self, cmd):
        self.currentCommand = cmd

    def get_suggestion(self, buffer, document):
        """ Given the current first word on prompt
            tries to find matching arguments
        """
        curr_prompt_elem = re.findall('([\S]+)', document.text)
        curr_last_field, offset, n_arg = grep_last_arg_field(document.text)

        print(f"customAutoSuggest::curr_last_field, offset, n_arg: ({curr_last_field}, {offset}, {n_arg})", file = sys.stderr)
        if curr_last_field:
            def_value = self.bound_prototyper.get_cmd_default_values_at(curr_prompt_elem[0], n_arg)
            if def_value is None:
                print(f"[ERROR-get_suggestion]Follwing prompt bug : >{document.text}<", file=sys.stderr)
                return None
        
            if len(def_value) > 1:
                return None
            
            
            # Testing if file        
            types = self.bound_prototyper.get_cmd_param_types_at(curr_prompt_elem[0], n_arg)
            if types:
                if types[0] == "path" and offset > 0: # Started to type smtg in a file field
                    print(f"Autosuggesting file field w/ {curr_last_field}", file=sys.stderr)
                    return Suggestion(path_suggest(curr_last_field.strip()))
                print("Autosuggesting ",def_value, file=sys.stderr)
                if str(def_value[0]).startswith(curr_last_field.strip()):
                    return Suggestion(str(def_value[0])[offset:])
                return Suggestion("")
        
        return None
    """       
       # print(f"# {len(curr_prompt_elem)} my i suggest ?\n")
        try: 
            data:Union[CommandModel, None] = self.command_manager[ curr_prompt_elem[0] ] ## MM
            if len(curr_prompt_elem) == 1: # return basic suggestion
                _ = " ".join( data.usage.split()[1:] )
                return Suggestion(f" {_}")
            # We are in arguments, here we check if a path is desirable
            curr_arg_type_num = len(curr_prompt_elem) - 2
            if data.paramTypes:
                if data.paramTypes[curr_arg_type_num] == "path":
                    return Suggestion( pathSuggest(curr_prompt_elem[-1]) )
            
        except KeyError as e:
            print(f"{curr_prompt_elem[0]} not a valid key\n", file=sys.stderr) 
            #return Suggestion("!!!")
        return Suggestion("")
    """