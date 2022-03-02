from pydantic import BaseModel, ValidationError, validator
from typing import Callable, Union, List, Optional, Literal
from xmlrpc.client import Boolean

ParamTypes = Literal["string", "number", "path"]

class CommandModel(BaseModel):
    target: Callable
    paramTypes: Optional[List[ParamTypes]]
    runningParams : Optional[Boolean] = False
    help: str = None
    usage:Optional[str] = None
    """
    @validator('paramTypes')
    def param_types_allowed_values(cls, v):
        if not v is None:
            for _ in v:
                if not _ in str_param_types:
                    raise ValueError(
                        'if no None paramTypes must be a list of "string", "number" or "path"')
        return v
    """
    
# SOME CUSTOM VALIDATION