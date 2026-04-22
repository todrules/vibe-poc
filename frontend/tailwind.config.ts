import type { Config } from "tailwindcss";

// Tailwind scans the App Router, reusable components, and shared type-driven UI folders.
const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./types/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: "#f4f6f1",
        ink: "#101828",
        line: "#d0d5dd",
        panel: "#ffffff",
        accent: {
          DEFAULT: "#175cd3",
          foreground: "#ffffff",
          subtle: "#eff8ff",
        },
      },
      boxShadow: {
        panel: "0 18px 50px -24px rgba(16, 24, 40, 0.18)",
      },
      borderRadius: {
        xl: "1rem",
        "2xl": "1.5rem",
      },
      fontFamily: {
        sans: ["Manrope", "ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
};

export default config;