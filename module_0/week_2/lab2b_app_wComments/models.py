"""
Request and response models for the AI Workbench API.
Pydantic enforces type safety at the API boundary.
"""

# Import Optional type hint for values that may be None.
# typing is from Python's standard library like os, sys, time etc.
# The typing module provides tools that let us describe the kinds of data our code expects,
# such as Optional, List, Dict, and many others.
# Optional tells readers (and tools) that a value may be present, or it may be None.
from typing import Optional

# Import Pydantic tools for defining and validating API request/response models.
# Pydantic is a library that checks whether incoming data matches the structure and rules we define.
# Pydantic gets installed automatically when we install FastAPI, since this is one of the dependecy.
from pydantic import BaseModel, Field
# Think of BaseModel as a blueprint for defining the shape of data. 
# BaseModel gives your class special abilities, like validation and JSON conversion.
# Field lets you attach rules to individual fields. For example, Field(min_length=1)



class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)


class TextResponse(BaseModel):
    task: str
    result: str
    model: str
    tokens_used: Optional[int] = None


class HealthResponse(BaseModel):
    status: str
    provider: str
    model: str
