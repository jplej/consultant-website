module.exports = {
  content: [
    './_drafts/**/*.html',
    './_includes/*.html',
    './_layouts/*.html',
    './_posts/**/*.md',
    './_posts/**/*.html',
    './_landing_blocs/**/*.md',
    './_landing_blocs/**/*.html',
    './_landing_blocs/*.html',
    './_service_blocs/**/*.md',
    './_service_blocs/**/*.html',
    './pages/**/*.md',
    './pages/**/*.html',
  ],
  safelist: [
    'bg-BgLight-primary',
    'bg-BgLight-secondary',
    'bg-BgDark-primary',
    'bg-BgDark-secondary',
    'bg-BgDark-border',
    'bg-accent-main',
    'bg-accent-highlight',
    'bg-accent-error',
    'bg-accent-warning',
    'bg-accent-success',
    'bg-accent-url',
    'text-textOnDark-primary',
    'text-textOnDark-secondary',
    'text-textOnLight-primary',
    'text-textOnLight-secondary',
    'text-accent-main',
    'text-accent-highlight',
    'text-accent-error',
    'text-accent-url',
    'text-accent-main',
    'text-accent-warning',
    'text-accent-success',
  ],
  theme: {
    extend: {
      colors: {
        // Background Colors for Dark UI Elements (Interactive)
        BgDark: {
          primary: '#3B4252',   // `nord1`
          secondary: '#434C5E',  // `nord2`
          border: '#4C566A',     // `nord3`
        },

        // Background Colors for Light Non-Interactive Elements
        BgLight: {
          primary: '#ECEFF4',  // `nord6`
          secondary: '#E5E9F0', // `nord5`
        },

        // Text Colors on Dark Backgrounds
        textOnDark: {
          primary: '#ECEFF4',  // `nord6`
          secondary: '#d8dee9', // `nord5`
        },

        // Text Colors on Light Backgrounds
        textOnLight: {
          primary: '#2E3440',  // `nord0`
          secondary: '#4C566A', // `nord3`
        },

        // Accent Colors for Highlights and Actions
        accent: {
          main: '#8FBCBB',   // `nord7`
          highlight: '#88C0D0',        // `nord8`
          error: '#BF616A',        // `nord11` (red)
          warning: '#EBCB8B',      // `nord13` (yellow)
          success: '#A3BE8C',      // `nord14` (green)
          url: '#b48ead' // `nord15' (purple)
        },
      },

      // Font Families
      fontFamily: {
        // Body text
        body: ['Roboto', 'Open Sans', 'sans-serif'],

        // Headings
        heading: ['Oswald', 'Playfair Display', 'Montserrat', 'Helvetica', 'serif'],

        // Buttons & Navigation
        button: ['Oswald', 'Arial', 'Lato', 'sans-serif'],

        // Code or Technical Text
        code: ['Roboto Mono', 'Inconsolata', 'Courier New', 'monospace'],
      },
    },
  },
  plugins: []
}
