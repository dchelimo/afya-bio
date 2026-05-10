/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./index.html", "./*/index.html"],
  theme: {
    extend: {
      fontFamily: {
        sans:    ['DM Sans', 'system-ui', 'sans-serif'],
        serif:   ['DM Serif Display', 'Georgia', 'serif'],
        mono:    ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
}
