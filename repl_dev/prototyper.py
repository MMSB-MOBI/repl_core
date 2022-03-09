import re
from optparse import Option
from pydantic import BaseModel, ValidationError, validator
from typing import Callable, Union, List, Optional, Literal, Any
from xmlrpc.client import Boolean
ParamTypes = Literal["string", "number", "file", "keyword"]

class Parameter(BaseModel):
    name : str
    types : Optional[ Union[ ParamTypes, List[ ParamTypes ] ] ]
    values : Optional[ Union[ str, List[ str ] ] ]
    
    def parse_fields(self, input_string):
        self.parse_types(input_string)
        self.parse_default_values(input_string)
        
    def parse_types(self, v):
        v_types = []
        try:
            _ = iter(v)
        except TypeError as e:
            v = [v]
        for x in v:
            t = None
            if x.startswith('_'):
                if not x[1:] in ["string", "number", "file"]:
                    raise ValueError(f"{x[1:]} is not a valid type")
                t =  x[1:]
            else: # plain value assumed being keyword
                t = "keyword"
            v_types.append(t)
            
        self.types = v_types if len(v_types) > 1 else v_types[0]
        
    def parse_default_values(self, v):
        v_values = []
        try:
            _ = iter(v)
        except TypeError as e:
            v = [v]
        
        v_values = [ None if x.startswith('_') else x for x in  v ]
            
        self.values =  v_values if len(v_values) > 1 else v_values[0]
           
def parameter_parser(input_field)->Optional[Parameter]:
    if not ( input_field[0] == '{' and   input_field[-1] == '}'):
        raise ValueError(f"malformed paramater input value {input_field}")
    
    _ = input_field[1:-1]
    p_name, p_fields = _.split(':')    
    p_field = p_fields.split('|')
    pO = Parameter(name=p_name)
    pO.parse_fields(p_field)
    return pO

class Prototype(BaseModel):
    input_str: str
    command : str
    parameters:Optional[List[Parameter]]

    def add(self, p:Parameter):
        if not self.parameters:
            self.parameters = []
        self.parameters.append(p)
        

def base_input_parser(istr):
    _ = re.search("^([\S]+)(.*)$", istr)
    if not _ :
        raise ValueError(f"No command found in {istr}")
    if len(_.group())==2:
        return (_[1], None)
    p = re.findall("(\{[\w_:|]+\})", _[2])

    return (_[1], p)
        
def parse(input_string):
    cmd, maybe_args = base_input_parser(input_string)
    
    fn_proto = Prototype(command=cmd, input_str=input_string)
    
    if not maybe_args:
        print(f"No parameter found in input string {input_string}")
        return fn_proto
    
    for arg in maybe_args:
        fn_proto.add(parameter_parser(arg))
        
    return fn_proto


class PrototypeCollector():
    def __init__(self):
        self._prototypes = {}

    def add(self, input_string)->Prototype:
        new_proto = parse(input_string)
        if new_proto.command in self._prototypes:
            raise KeyError(f"prototype command {new_proto.command} alredy exists")
        self._prototypes[new_proto.command] = new_proto
        return new_proto
    
    def isa(self, cmd):
        return str(cmd) in self._prototypes

    @property
    def commands(self):
        return [ k for k in self._prototypes ]
    
    def get_cmd_param_names(self, cmd_symbol)->Optional[List[str]]:
        if not cmd_symbol in  self._prototypes:
            raise KeyError(f"no prototype found for command named {cmd_symbol}")
        proto:Prototype = self._prototypes[cmd_symbol]
        if not proto.parameters:
            return None
        
        return [ p.name for p in proto.parameters ]