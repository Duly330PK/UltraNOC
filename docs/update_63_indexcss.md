📝 Dokumentation – update_63_indexcss.md
📁 Pfad: C:\noc_project\UltraNOC\docs\updates\update_63_indexcss.md

📄 Quelltext:

markdown
Kopieren
Bearbeiten
# 🎨 Update 63 – CSS-Einstiegspunkt für Tailwind

## Ziel
Aktivierung der TailwindCSS-Basisklassen durch `index.css`.

## Datei
📄 `C:\noc_project\UltraNOC\frontend\src\index.css`

## Inhalt

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Optional: Eigene globale Styles */
body {
  font-family: system-ui, sans-serif;
}
Erklärung
Direktive	Funktion
@tailwind base	Importiert grundlegende CSS-Resets
@tailwind components	Ermöglicht benutzerdefinierte Komponenten
@tailwind utilities	Aktiviert Utility-Klassen

Hinweise
Die Datei muss in main.jsx eingebunden sein, z. B. per import './index.css';

Tailwind analysiert die Datei automatisch via Vite/PostCSS.