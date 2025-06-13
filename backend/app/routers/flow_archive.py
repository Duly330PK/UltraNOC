from fastapi import APIRouter
from typing import List
import os
import json

router = APIRouter()

ARCHIVE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/flow_archive.json"))

@router.get("/flows")
def get_flows():
    if not os.path.exists(ARCHIVE_PATH):
        return []
    with open(ARCHIVE_PATH, "r") as f:
        return json.load(f)
