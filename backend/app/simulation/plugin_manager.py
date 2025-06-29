import yaml
import os
from typing import Dict, List

class PluginManager:
    def __init__(self, plugin_dir: str = "app/data/device_plugins"):
        self.plugin_dir = plugin_dir
        self.device_templates: Dict[str, Dict] = {}
        self.load_plugins()

    def load_plugins(self):
        print("Lade Geräte-Plugins...")
        if not os.path.exists(self.plugin_dir):
            print(f"WARNUNG: Plugin-Verzeichnis nicht gefunden: {self.plugin_dir}")
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                filepath = os.path.join(self.plugin_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        plugin_data = yaml.safe_load(f)
                        if 'id' in plugin_data:
                            self.device_templates[plugin_data['id']] = plugin_data
                            print(f"  -> Plugin '{plugin_data['id']}' geladen.")
                        else:
                            print(f"WARNUNG: Plugin {filename} hat keine 'id'.")
                except Exception as e:
                    print(f"FEHLER beim Laden von Plugin {filename}: {e}")

    def get_template(self, template_id: str) -> Dict:
        return self.device_templates.get(template_id)

    def get_all_templates(self) -> List[Dict]:
        return list(self.device_templates.values())