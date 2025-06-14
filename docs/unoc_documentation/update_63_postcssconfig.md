📝 Dokumentation – update_63_postcssconfig.md
📁 Pfad: C:\noc_project\UltraNOC\docs\updates\update_63_postcssconfig.md

📄 Quelltext:

markdown
Kopieren
Bearbeiten
# ⚙️ Update 63 – PostCSS-Konfiguration

## Ziel
Einrichtung von PostCSS als Build-Tool für TailwindCSS im Vite-Frontend.

## Datei
📄 `C:\noc_project\UltraNOC\frontend\postcss.config.js`

## Inhalt

```js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
Erklärung
Plugin	Funktion
tailwindcss	Verarbeitet die TailwindCSS-Direktiven in CSS-Dateien
autoprefixer	Fügt automatisch Vendor-Präfixe für Browserkompatibilität hinzu

Hinweise
Diese Datei ist notwendig, damit TailwindCSS via Vite korrekt kompiliert wird.

Wird automatisch von Vite erkannt, wenn im Projektverzeichnis vorhanden.

Voraussetzung
tailwindcss, autoprefixer, postcss müssen in devDependencies installiert sein.

perl
Kopieren
Bearbeiten
