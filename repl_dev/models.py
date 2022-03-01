from pydantic import BaseModel, ValidationError, validator
from typing import Callable, Union, List
from xmlrpc.client import Boolean


class CommandModel(BaseModel):
    _target: Callable
    paramTypes: Union[List,None]
    runningParams : Boolean
    help: str

# SOME CUSTOM VALIDATION