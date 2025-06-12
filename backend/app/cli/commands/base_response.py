from pydantic import BaseModel
from typing import Optional

class CLIResponse(BaseModel):
    output: str
    error: bool = False
    warning: Optional[str] = None
