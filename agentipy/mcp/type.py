from typing import Any, Callable, Dict

from pydantic import BaseModel


class ActionType(BaseModel):
    """
    Defines the structure for an Action within Agentipy.
    """
    name: str
    description: str
    schema: Dict[str, ]
    handler: Callable

