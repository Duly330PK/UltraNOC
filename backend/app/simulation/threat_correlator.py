from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional

# Definiert einfache Angriffsmuster als Sequenz von Ereignistypen.
# In einem echten System wäre dies eine komplexe, externe Konfiguration.
ATTACK_PATTERNS = {
    "brute_force_ssh": {
        "name": "Potenzieller Brute-Force SSH-Angriff",
        "sequence": ["Failed SSH login", "Failed SSH login", "Failed SSH login", "Successful SSH login"],
        "time_window_seconds": 300, # Angriff muss innerhalb von 5 Minuten erfolgen
    }
    # Hier könnten weitere Muster definiert werden, z.B. für Port-Scans etc.
}

class ThreatCorrelator:
    '''
    Diese Klasse analysiert einen Strom von Sicherheitsereignissen und versucht,
    bekannte Angriffsmuster zu erkennen.
    '''
    def __init__(self):
        # Ein Buffer, der die letzten relevanten Sicherheitsereignisse speichert.
        self.event_buffer: List[Dict] = []
        # Ein Set, um bereits gemeldete Incidents zu speichern und Duplikate zu vermeiden.
        self.incidents_created = set()

    def add_event(self, event: Dict) -> Optional[Dict]:
        '''Fügt ein neues Event hinzu und prüft sofort auf bekannte Muster.'''
        self.event_buffer.append(event)

        # Bereinige den Buffer von alten Events, um die Performance zu gewährleisten.
        now = datetime.fromisoformat(event["timestamp"])
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)

        self.event_buffer = [
            e for e in self.event_buffer 
            if now - datetime.fromisoformat(e["timestamp"]).replace(tzinfo=timezone.utc) < timedelta(seconds=600)
        ]
        return self.check_for_patterns()

    def check_for_patterns(self) -> Optional[Dict]:
        '''Prüft den Event-Buffer auf vordefinierte Angriffsmuster.'''
        # Gruppiere Events nach dem Zielgerät, um Angriffe auf ein spezifisches Ziel zu erkennen.
        events_on_target = {}
        for event in self.event_buffer:
            target = event.get('target_node_id')
            if target:
                events_on_target.setdefault(target, []).append(event)

        for target, events in events_on_target.items():
            event_types = [e['type'] for e in events]
            for pattern_key, pattern in ATTACK_PATTERNS.items():
                # Einfache Sequenzprüfung: Prüft, ob die Mustersequenz in den Ereignissen enthalten ist.
                pattern_str = ",".join(pattern["sequence"])
                events_str = ",".join(event_types)

                if pattern_str in events_str:
                    # Erzeuge eine eindeutige ID für diesen Incident, um ihn nicht mehrfach zu melden.
                    incident_id = f"inc-{pattern_key}-{target}"
                    if incident_id not in self.incidents_created:
                        print(f"!!! NEUER VORFALL ENTDECKT: {pattern['name']} auf {target} !!!")
                        self.incidents_created.add(incident_id)

                        # Gib die relevanten Informationen für die Incident-Erstellung zurück.
                        relevant_events = [e for e in events if e['type'] in pattern['sequence']]
                        return {"name": pattern['name'], "target": target, "events": relevant_events}
        return None