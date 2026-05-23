const config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        void: {
          950: "#0a0a0f",
          900: "#0f0f1a",
          800: "#1a1a2e",
          700: "#2a2a4a",
        },
        chrono: {
          gold: "#c9a96e",
          copper: "#b87333",
          blue: "#4a8fcc",
          purple: "#7b4fcc",
          green: "#5a9e6f",
        },
      },
      fontFamily: {
        display: ["var(--font-cinzel)", "serif"],
        body: ["var(--font-inter)", "sans-serif"],
      },
      animation: {
        "pulse-glow": "pulseGlow 2s ease-in-out infinite",
        "slide-up": "slideUp 0.6s ease-out",
        "fade-in": "fadeIn 0.8s ease-out",
      },
      keyframes: {
        pulseGlow: {
          "0%, 100%": { boxShadow: "0 0 20px rgba(201, 169, 110, 0.3)" },
          "50%": { boxShadow: "0 0 40px rgba(201, 169, 110, 0.6)" },
        },
        slideUp: {
          from: { opacity: "0", transform: "translateY(20px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        fadeIn: {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
