/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.jsx",
  ],
  theme: {
    extend: {
      screens: {
        'lg': '1280px',
      },
      colors: {
        'line-green': '#06C755',
        'base-orange': '#FFA800',
      },
      fontFamily:{
        'hel': 'Helvetica',
      }
    },
  },
  plugins: [],
}

