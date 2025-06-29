/** @type {import('tailwindcss').Config} */
export default {
  // NEU: Aktiviert den klassenbasierten Dark Mode
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Dark Mode Farben (bleiben wie bisher)
        'noc-dark': '#0d1117',
        'noc-light-dark': '#161b22',
        'noc-border': '#30363d',
        'noc-text': '#c9d1d9',
        'noc-text-secondary': '#8b949e',

        // Light Mode Farben (NEU)
        'lm-bg': '#ffffff',
        'lm-bg-secondary': '#f0f2f5',
        'lm-border': '#d0d7de',
        'lm-text': '#24292f',
        'lm-text-secondary': '#57606a',
        
        // Akzentfarben (können für beide Modi gleich sein)
        'noc-blue': '#58a6ff',
        'noc-green': '#3fb950',
        'noc-yellow': '#d29922',
        'noc-red': '#f85149',
        'noc-purple': '#a371f7',
      },
    },
  },
  plugins: [],
}