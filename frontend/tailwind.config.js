/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        industrial: {
          900: "#0f172a",
          800: "#1e293b",
          700: "#334155",
          600: "#475569",
          500: "#64748b",
          accent: "#0284c7",
          success: "#16a34a",
          danger: "#dc2626",
          warning: "#d97706"
        }
      }
    },
  },
  plugins: [],
}
