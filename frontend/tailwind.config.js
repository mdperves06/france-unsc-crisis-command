/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        france: {
          blue: "#002395",
          white: "#FFFFFF",
          red: "#ED2939",
          navy: "#0a1128",
          dark: "#050914",
          gold: "#D4AF37",
          cyan: "#00d2ff"
        },
        un: {
          blue: "#4B92DB",
          light: "#E8F0FE",
          dark: "#0b1d3a"
        },
        diplomatic: {
          border: "#1E293B",
          card: "rgba(15, 23, 42, 0.75)",
          cardHover: "rgba(30, 41, 59, 0.85)",
          glow: "rgba(0, 210, 255, 0.15)"
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace']
      },
      boxShadow: {
        'glow-blue': '0 0 25px rgba(0, 35, 149, 0.35)',
        'glow-cyan': '0 0 20px rgba(0, 210, 255, 0.25)',
        'glow-gold': '0 0 20px rgba(212, 175, 55, 0.25)',
      }
    },
  },
  plugins: [],
}
