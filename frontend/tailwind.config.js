/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "#0b0f1a",
        card: "#0f172a",
        panel: "#111827",
        stroke: "rgba(255,255,255,0.06)",
        glow: "rgba(99,102,241,0.25)"
      },
      boxShadow: {
        soft: "0 8px 30px rgba(99,102,241,0.12)"
      }
    },
  },
  plugins: [],
}
