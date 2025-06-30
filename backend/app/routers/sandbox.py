import yaml
import os
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

PLUGIN_DIR = "app/data/device_plugins"

@router.get("/device-templates", response_model=List[dict])
def get_device_templates():
    """
    Liest alle Geräte-Plugin-Dateien (.yml) aus dem Plugin-Verzeichnis,
    parst sie und gibt sie als Liste an das Frontend zurück.
    """
    templates = []
    if not os.path.exists(PLUGIN_DIR):
        raise HTTPException(status_code=404, detail="Plugin-Verzeichnis nicht gefunden.")
        
    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith(".yml"):
            try:
                with open(os.path.join(PLUGIN_DIR, filename), 'r', encoding='utf-8') as f:
                    template = yaml.safe_load(f)
                    templates.append(template)
            except Exception as e:
                print(f"Fehler beim Laden des Plugins {filename}: {e}")
    return templates