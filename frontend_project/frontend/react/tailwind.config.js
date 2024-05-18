/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.jsx",
    "node_modules/preline/dist/*.jsx",
  ],
  theme: {
    extend: {
      screens: {
        'lg': '1280px',
      },
      colors: {
        'line-green': '#06C755',
        'base-orange': '#FFA800',
        'base-orange-hover': '#FF7B00',
      },
      fontFamily:{
        'hel': 'Helvetica',
      }
    },
  },
  plugins: [
    require('preline/plugin'),
  ],
}

