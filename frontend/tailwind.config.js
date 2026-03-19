/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "#050816",
        surface: "#0a1021",
        "surface-container": "#0f172d",
        "surface-container-low": "#0b1326",
        "surface-container-high": "#15203d",
        "surface-container-highest": "#1d2b52",
        "surface-variant": "#1d2745",
        "on-surface": "#f2f7ff",
        "on-surface-variant": "#93a6cc",
        "on-background": "#eaf2ff",
        outline: "#5d719d",
        "outline-variant": "#223054",
        primary: "#6cf2ff",
        "primary-container": "#00d7ff",
        "on-primary": "#03141d",
        secondary: "#8dffb6",
        "secondary-container": "#35ff9c",
        "on-secondary-container": "#032114",
        tertiary: "#b897ff",
        "tertiary-container": "#9a7cff",
        error: "#ff7a9f",
        "error-container": "#3d1021",
      },
      fontFamily: {
        headline: ["Space Grotesk", "Sora", "sans-serif"],
        body: ["Sora", "Segoe UI Variable", "sans-serif"],
        label: ["JetBrains Mono", "Consolas", "monospace"],
      },
      borderRadius: {
        DEFAULT: "0.35rem",
        lg: "0.75rem",
        xl: "1rem",
        full: "999px",
      },
      boxShadow: {
        "kinetic-pulse": "0 0 18px rgba(53, 255, 156, 0.32)",
        "primary-glow": "0 0 24px rgba(108, 242, 255, 0.22)",
        "error-glow": "0 0 22px rgba(255, 122, 159, 0.28)",
        hud: "0 22px 60px rgba(0, 0, 0, 0.38), inset 0 1px 0 rgba(255, 255, 255, 0.04)",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "kinetic-pulse": "kineticPulse 2s ease-in-out infinite alternate",
        drift: "drift 9s ease-in-out infinite",
        scan: "scan 8s linear infinite",
      },
      keyframes: {
        kineticPulse: {
          "0%": { boxShadow: "0 0 12px rgba(53, 255, 156, 0.2)" },
          "100%": { boxShadow: "0 0 26px rgba(53, 255, 156, 0.55)" },
        },
        drift: {
          "0%, 100%": { transform: "translate3d(0, 0, 0)" },
          "50%": { transform: "translate3d(0, -8px, 0)" },
        },
        scan: {
          "0%": { transform: "translateY(-140%)" },
          "100%": { transform: "translateY(220%)" },
        },
      },
    },
  },
  plugins: [],
};
