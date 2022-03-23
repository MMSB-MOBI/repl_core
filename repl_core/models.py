from ast import arg
from pydantic import BaseModel, ValidationError, validator
from typing import Callable, Union, List, Optional, Literal
from xmlrpc.client import Boolean
from .errors import UpdateTupleLengthError, UpdateTupleTypeError
import sys

class CommandModel(BaseModel):
    target: Callable
    prototype_string:str
    help: str = None



#class UpdatePacket()

def validate_update_packet(f_name, *args):
    if len(args) != 3:
        raise UpdateTupleLengthError(f_name, *args)

    print(args)
    if not isinstance(args[0], int):
        raise UpdateTupleTypeError(0, f_name, *args)

    if not isinstance(args[1], int):
        raise UpdateTupleTypeError(1, f_name, *args)

    if not ( type(args[2]) == type(True) or type(args[2]) == type(False) ):
        raise UpdateTupleTypeError(2, f_name, *args)
    
   # raise UpdateTupleTypeError(1, f_name, *args)

    return args