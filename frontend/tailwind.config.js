/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(0 0% 0%)",
        main: "#f97316",
        mainAccent: "#fb923c",
        overlay: "rgba(0,0,0,0.8)",
        bg: "#dfe5f2",
        text: "#000",
        darkBg: "#1e293b",
        darkText: "#eeefe9",
        secondaryBlack: "#212121",
      },
      borderRadius: {
        base: "6px"
      },
      boxShadow: {
        base: "4px 4px 0px 0px rgba(0,0,0,1)",
      },
      translate: {
        boxShadowX: "4px",
        boxShadowY: "4px",
      },
      fontWeight: {
        base: "500",
        heading: "700",
      },
    },
  },
  plugins: [],
}
