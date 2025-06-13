module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nocblue: '#0b5ed7',
        nocgray: '#1f1f1f'
      },
      borderRadius: {
        '2xl': '1rem'
      }
    },
  },
  plugins: [],
}
