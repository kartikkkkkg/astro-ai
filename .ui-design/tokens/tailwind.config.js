// Design System Tailwind Extension
// Import and spread in your tailwind.config.ts

/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#E0FCF9",
          100: "#B3F9F3",
          200: "#80F6ED",
          300: "#4DF3E7",
          400: "#26F0E1",
          500: "#0BF7ED",
          600: "#09C6BB",
          700: "#07958A",
          800: "#05645A",
          900: "#04332A",
          950: "#021915",
        },
        secondary: {
          50: "#FFE0E8",
          100: "#FFB3D1",
          200: "#FF80BA",
          300: "#FF4DA3",
          400: "#FF268C",
          500: "#FF006E",
          600: "#CC0058",
          700: "#990042",
          800: "#66002D",
          900: "#330017",
          950: "#1A000B",
        },
        neutral: {
          50: "#F9FAFB",
          100: "#F3F4F6",
          200: "#E5E7EB",
          300: "#D1D5DB",
          400: "#9CA3AF",
          500: "#6B7280",
          600: "#4B5563",
          700: "#374151",
          800: "#1F2937",
          900: "#111827",
          950: "#030712",
        },
        semantic: {
          success: "#22C55E",
          warning: "#F59E0B",
          error: "#EF4444",
          info: "#3B82F6",
        },
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        mono: ["ui-monospace", "Fira Code", "monospace"],
      },
      borderRadius: {
        sm: "0.125rem",
        base: "0.25rem",
        md: "0.375rem",
        lg: "0.5rem",
        xl: "0.75rem",
        "2xl": "1rem",
        full: "9999px",
      },
      boxShadow: {
        sm: "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        base: "0 1px 3px 0 rgb(0 0 0 / 0.1)",
        md: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
        lg: "0 10px 15px -3px rgb(0 0 0 / 0.1)",
        xl: "0 20px 25px -5px rgb(0 0 0 / 0.1)",
      },
      animation: {
        duration: {
          fast: "150ms",
          normal: "300ms",
          slow: "500ms",
        },
        easing: {
          ease: "cubic-bezier(0.4, 0, 0.2, 1)",
          easeIn: "cubic-bezier(0.4, 0, 1, 1)",
          easeOut: "cubic-bezier(0, 0, 0.2, 1)",
        },
      },
    },
  },
};