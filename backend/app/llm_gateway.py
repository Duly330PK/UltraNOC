import httpx
import os
from typing import List, Dict

LLM_API_URL = os.getenv("LLM_API_URL", "http://host.docker.internal:11434/api/generate")

async def generate_text_with_history(prompt: str, history: List[Dict[str, str]] = None) -> str:
    # Erstellt einen formatierten Prompt, der den Chat-Verlauf berücksichtigt,
    # um dem LLM Kontext zu geben.
    full_prompt = ""
    if history:
        for entry in history:
            # Formatierung für ChatML-basierte Modelle wie Mistral Instruct
            full_prompt += f"<|im_start|>{entry['role']}\n{entry['content']}<|im_end|>\n"
    full_prompt += f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

    # Das zu verwendende Modell sollte idealerweise konfigurierbar sein.
    # Für die Demo verwenden wir 'mistral:instruct' als Annahme.
    payload = {"model": "mistral:instruct", "prompt": full_prompt, "stream": False}

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(LLM_API_URL, json=payload)
            response.raise_for_status()
            return response.json().get("response", "LLM-Antwort konnte nicht verarbeitet werden.").strip()
        except httpx.RequestError:
            return f"Fehler: LLM Gateway nicht erreichbar. Läuft Ollama/LM Studio unter {LLM_API_URL} und ist das Modell 'mistral:instruct' geladen?"
        except Exception as e:
            return f"Ein unerwarteter Fehler ist aufgetreten: {e}"

async def generate_incident_summary(events: List[Dict]) -> str:
    event_summary = "\n".join([f"- {e['timestamp']}: {e['description']}" for e in events])
    prompt = f'''
    Du bist ein Cybersecurity-Analyst. Fasse die folgende Kette von Ereignissen zu einem professionellen Incident-Bericht zusammen.
    Erkenne das Muster, gib dem Vorfall einen aussagekräftigen Namen und beschreibe kurz den potenziellen Angriffsvektor.

    Ereignis-Kette:
    {event_summary}

    Zusammenfassung des Vorfalls:
    '''
    return await generate_text_with_history(prompt)