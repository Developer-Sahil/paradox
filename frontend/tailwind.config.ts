import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Cool-toned palette dominated by deep navy, teal, and soft cyan accents
        primary: {
          DEFAULT: '#0A192F', // Deep Navy
          light: '#172A45', // Slightly lighter navy for backgrounds
          dark: '#05101F', // Even deeper navy for extreme darks
        },
        accent: {
          DEFAULT: '#00C4CC', // Teal
          light: '#6DD5ED', // Soft Cyan
          dark: '#008C9E', // Darker Teal
        },
        text: {
          DEFAULT: '#E0E0E0', // Light grey for readability on dark backgrounds
          secondary: '#B0B0B0', // Slightly darker grey for secondary text
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Example: Using Inter as a bold yet minimal sans-serif font
        mono: ['Fira Code', 'monospace'], // Example: Fira Code for monospaced text
      },
      // Box shadow for soft glow effects (glassmorphism)
      boxShadow: {
        'soft-glow': '0 0 15px rgba(0, 196, 204, 0.4), 0 0 30px rgba(0, 196, 204, 0.2)',
        'glass-light': '0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)',
        'glass-dark': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
      },
      // Backgrounds for glassmorphism
      backdropBlur: {
        xs: '2px',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
};

export default config;
