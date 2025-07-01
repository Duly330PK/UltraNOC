import yaml
import os
from typing import Dict, List, Any

class PluginManager:
    """
    Verwaltet das Laden von Geräte-Plugins aus YAML-Dateien.
    Jedes Plugin definiert die Metadaten und CLI-Befehle für einen Gerätetyp.
    """
    def __init__(self, plugin_dir: str = "app/data/device_plugins"):
        self.plugin_dir = plugin_dir
        self.device_templates: Dict[str, Dict] = {}
        self.load_plugins()

    def load_plugins(self):
        """Lädt alle .yml-Dateien aus dem Plugin-Verzeichnis."""
        print("--- Loading Device Plugins ---")
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            print(f"INFO: Plugin directory created: {self.plugin_dir}")
            return

        # DEBUG: List all files in the plugin directory
        try:
            files = os.listdir(self.plugin_dir)
            print(f"Found {len(files)} files in '{self.plugin_dir}': {files}")
        except Exception as e:
            print(f"ERROR: Could not list files in '{self.plugin_dir}': {e}")
            return

        for filename in files:
            if filename.endswith((".yml", ".yaml")):
                filepath = os.path.join(self.plugin_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        plugin_data = yaml.safe_load(f)
                        if plugin_data and 'id' in plugin_data:
                            self.device_templates[plugin_data['id']] = plugin_data
                            print(f"  -> SUCCESS: Plugin '{plugin_data['id']}' from '{filename}' loaded.")
                        else:
                            print(f"  -> WARNING: Plugin '{filename}' is missing an 'id' and will be ignored.")
                except Exception as e:
                    print(f"  -> ERROR: Failed to load plugin from '{filename}': {e}")
        print("--- Plugin loading finished ---")


    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Gibt die Daten für ein spezifisches Geräte-Template zurück."""
        return self.device_templates.get(template_id, {})

    def get_all_templates(self) -> List[Dict]:
        """Gibt eine Liste aller geladenen Geräte-Templates zurück."""
        return list(self.device_templates.values())