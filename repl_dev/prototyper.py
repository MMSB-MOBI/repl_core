from ast import keyword
from optparse import Option
import re, sys
from typing import List, Optional, Union
from pydantic import BaseModel
from .parameters import Parameter, parameter_parser, ParamValues, ParamTypes



class Prototype(BaseModel):
    input_str: str
    command : str
    parameters:Optional[List[Parameter]]
    comments: Optional[str]

    def add(self, p:Parameter):
        if not self.parameters:
            self.parameters = []
        self.parameters.append(p)

    def set_defaults(self, defaults_values_tup):
        if self.parameters is None:
            if defaults_values_tup:
                raise TypeError(f"Prototype {self.command} parameters array is None but default values are found: {defaults_values_tup}") 
            return 
        print(f"Prototype {self.command} parameters array:{self.parameters}\tdefault values {defaults_values_tup}",\
            file=sys.stderr)
        if defaults_values_tup is None:
            return
        assert len(defaults_values_tup) == len(self.parameters)

        for p, _ in zip(self.parameters, defaults_values_tup):
            print(f"Parameter obj value::{p}",file=sys.stderr)
            if not "keyword" in p.types:
                p.values = [_]
    def __len__(self):
        return len(self.parameters)

def base_input_parser(istr):
    _ = re.search("^([\S]+)(.*)$", istr)
    if not _ :
        raise ValueError(f"No command found in {istr}")
    if len(_.group()) == 2:
        return (_[1], None)
    p = re.findall("(\{[\w_:|]+\})", _[2])

    return (_[1], p)

# Prototype factory
def parse(input_string, comments=None, callable=None):
    cmd, maybe_args = base_input_parser(input_string)
    
    fn_proto = Prototype(command=cmd, input_str=input_string, comments=comments)
    
    if not maybe_args:
        print(f"No parameter found in input string {input_string}", file=sys.stderr)
        return fn_proto
    
    for arg in maybe_args:
        fn_proto.add(parameter_parser(arg))
        
    return fn_proto

class PrototypeCollector():
    def __init__(self):
        self._prototypes = {}

    def __getitem__(self, cmd):
        if not cmd in self._prototypes:
            raise KeyError(f"prototype command {cmd} does not exist")

        return  self._prototypes[cmd]

    def add(self, input_string, default_values, comments=None)->Prototype:
        new_proto = parse(input_string, comments=comments)
        if new_proto.command in self._prototypes:
            raise KeyError(f"prototype command {new_proto.command} alredy exists")
        
        new_proto.set_defaults(default_values)
        print("added Prototype Object {new_proto}",file=sys.stderr)

        self._prototypes[new_proto.command] = new_proto
        return new_proto
    
    def get_match_cmd(self, maybe_cmd:str):
        print(f"Completing on input >{maybe_cmd}<", file=sys.stderr)      
        if not maybe_cmd:
            return []
        return  [ _ for _ in self._prototypes if _.startswith(maybe_cmd) ]
    
    def get_cmd_default_values_at(self, cmd, narg)->Optional[ List[ParamValues] ]:
        if cmd not in self._prototypes:
            return None
        proto:Prototype = self._prototypes[cmd]
        if narg >= len(proto):
            return None
        p:Parameter = proto.parameters[narg]
        return p.values

    def get_cmd_param_types_at(self, cmd, narg)->Optional[ List[ParamTypes] ]:
        if cmd not in self._prototypes:
            return None
        proto:Prototype = self._prototypes[cmd]
        if narg >= len(proto):
            return None
        p:Parameter = proto.parameters[narg]
        return p.types

    def isa(self, cmd):
        return str(cmd) in self._prototypes

    @property
    def commands(self):
        return [ k for k in self._prototypes ]
    
    def get_cmd_all_param_names(self, cmd_symbol)->Optional[List[str]]:
        if not cmd_symbol in  self._prototypes:
            raise KeyError(f"no prototype found for command named {cmd_symbol}")
        proto:Prototype = self._prototypes[cmd_symbol]
        if not proto.parameters:
            return None
        
        return [ p.name for p in proto.parameters ]

    def get_cmd_all_param_types(self, cmd_symbol)->Optional[List[List[ParamTypes]]]:
        if not cmd_symbol in  self._prototypes:
            raise KeyError(f"no prototype found for command named {cmd_symbol}")
        proto:Prototype = self._prototypes[cmd_symbol]
        if not proto.parameters:
            return None
        print(f"##{proto.parameters}", file=sys.stderr)
        return [ p.types for p in proto.parameters ]
        
    def get_cmd_all_param_values(self, cmd_symbol)->Optional[List[List[ParamValues]]]:
        if not cmd_symbol in  self._prototypes:
            raise KeyError(f"no prototype found for command named {cmd_symbol}")
        proto:Prototype = self._prototypes[cmd_symbol]
        if not proto.parameters:
            return None
        print(f"##{proto.parameters}", file=sys.stderr)
        return [ p.values for p in proto.parameters ]

     # to do 
      #  if not cmd_symbol in  self._prototypes:
      #      raise KeyError(f"no prototype found for command named {cmd_symbol}")
      #  proto:Prototype = self._prototypes[cmd_symbol]
      #  if not proto.parameters:
      #      return None
        
      #  return [ p.name for p in proto.parameters ]