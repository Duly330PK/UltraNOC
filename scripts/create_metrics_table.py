# C:\noc_project\UltraNOC\scripts\create_metrics_table.py

from app.models.device_metrics import Base
from app.database import engine

# Erstellt die Tabelle device_metrics (falls nicht vorhanden)
Base.metadata.create_all(bind=engine)
