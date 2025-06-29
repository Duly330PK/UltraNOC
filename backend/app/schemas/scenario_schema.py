from pydantic import BaseModel
from typing import List

class Scenario(BaseModel):
    name: str
    description: str
    steps: List[dict]