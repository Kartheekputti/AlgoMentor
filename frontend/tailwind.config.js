/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef6ff',
          100: '#d9ebff',
          200: '#bcd9ff',
          300: '#8ec1ff',
          400: '#5da3ff',
          500: '#3e86ff',
          600: '#2469db',
          700: '#1d52ae',
          800: '#1c448e',
          900: '#1b3b73',
        },
      },
    },
  },
  plugins: [],
}
