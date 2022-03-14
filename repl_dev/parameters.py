from numbers import Number
from pydantic import BaseModel
from typing import Callable, Union, List, Optional, Literal


ParamTypes = Literal["string", "number", "path", "keyword"]
ParamValues = Union[int, float, str]

class Parameter(BaseModel):
    name : str
    types : Optional[ Union[ ParamTypes, List[ ParamTypes ] ] ]
    values : Optional[ List[ ParamValues ] ] 
    
    def parse_fields(self, fields:List[str]):        
        self.parse_types(fields)
        self.parse_default_values(fields)
        
    def parse_types(self, v:List[str]):
        v_types = []
        try:
            _ = iter(v)
        except TypeError as e:
            v = [v]
        for x in v:
            t = None
            if x.startswith('_'):
                if not x[1:] in ["string", "number", "path"]:
                    raise ValueError(f"{x[1:]} is not a valid type")
                t =  x[1:]
            else: # plain value assumed being keyword
                t = "keyword"
            v_types.append(t)
            
        #self.types = v_types if len(v_types) > 1 else v_types[0]
        self.types = v_types


    def parse_default_values(self, v):
        v_values = []
        try:
            _ = iter(v)
        except TypeError as e:
            v = [v]
        
        v_values = [ None if x.startswith('_') else x for x in  v ]
            
        self.values =  v_values if v_values else None

def parameter_parser(input_field)->Optional[Parameter]:
    if not ( input_field[0] == '{' and   input_field[-1] == '}'):
        raise ValueError(f"malformed paramater input value {input_field}")
    
    _ = input_field[1:-1]
    p_name, p_fields = _.split(':')    
    p_field = p_fields.split('|')
    pO = Parameter(name=p_name)
    pO.parse_fields(p_field)
    return pO