# backend/app/routers/device_templates.py

from fastapi import APIRouter
from app.simulation.plugin_manager import PluginManager

router = APIRouter()
plugin_manager = PluginManager()

@router.get("/device-templates")
def get_device_templates():
    return plugin_manager.get_all_templates()
s