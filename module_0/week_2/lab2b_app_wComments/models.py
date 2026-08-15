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
# Think of BaseModel as a blueprint for defining the shape of data. 
# BaseModel gives your class special abilities, like validation and JSON conversion.
# Field lets you attach rules to individual fields. For example, Field(min_length=1)
from pydantic import BaseModel, Field

# Define the expected structure of an incoming API request.
# Class = A blueprint (template) used to create objects with a fixed structure.
# Define a new class named TextRequest based on Pydantic's BaseModel.
class TextRequest(BaseModel): # Inherit all the validation features and JSON handling from Pydantic's BaseModel.
    # "text: str" - # Type hint: the text field is expected to contain a string.
    # Field() - define additional validation rules
    # (...) - the particular API field is required, in our case "text" is our API field and it can't be ignored
    # min_length=1 prevents empty text & max_length=10000 limits the input size.
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
