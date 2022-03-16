from pydantic import BaseModel, ValidationError, validator
from typing import Callable, Union, List, Optional, Literal
from xmlrpc.client import Boolean

class CommandModel(BaseModel):
    target: Callable
    prototype_string:str
    help: str = None
