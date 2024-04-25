/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/pages/Home.jsx",
    "./src/components/MainMenu.jsx",
    "./src/components/Header.jsx",
    "./src/components/Footer.jsx",
    "./src/components/StockItems.jsx",
    "./src/pages/Stock.jsx",
  ],
  theme: {
    extend: {
      screens: {
        'lg': '1280px',
      }
    },
  },
  plugins: [],
}

