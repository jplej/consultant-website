/** @type {import('tailwindcss').Config} */
const plugin = require("tailwindcss/plugin");

// Gruvbox light (airline theme) -- https://github.com/morhetz/gruvbox
//   light0 #fbf1c7  light1 #ebdbb2  light2 #d5c4a1  light3 #bdae93  light4 #a89984
//   dark0  #282828  dark1  #3c3836  dark2  #504945  dark3  #665c54  dark4  #7c6f64
//   faded: red #9d0006  green #79740e  yellow #b57614  blue #076678  purple #8f3f71  aqua #427b58  orange #af3a03
// Solarized light (Ethan Schoonover) -- https://ethanschoonover.com/solarized
//   base03 #002b36  base02 #073642  base01 #586e75  base00 #657b83
//   base0  #839496  base1  #93a1a1  base2  #eee8d5  base3  #fdf6e3
//   yellow #b58900  orange #cb4b16  red    #dc322f  magenta #d33682
//   violet #6c71c4  blue   #268bd2  cyan   #2aa198  green   #859900
// Tonal palette -- raw Solarized hues, never referenced from templates directly.
const tones = {
  base01: '#586e75', base1: '#93a1a1', base2: '#eee8d5', base3: '#fdf6e3', base03: '#002b36',
  blue:   '#268bd2', cyan:   '#2aa198', green:  '#859900', yellow: '#b58900',
  orange: '#cb4b16', red:    '#dc322f', magenta:'#d33682', violet: '#6c71c4',
};

// Semantic roles -- this is what templates use. Remap freely.
// Theme-switching tokens use CSS custom properties (defined in input.css).
// withOpacityValue lets Tailwind inject the alpha for utility classes (bg-ink/50)
// while theme() calls in the typography plugin get a plain rgb() fallback.
function withOpacityValue(variable) {
  return ({ opacityValue }) => {
    if (opacityValue !== undefined) {
      return `rgb(var(${variable}) / ${opacityValue})`;
    }
    return `rgb(var(${variable}))`;
  };
}

const palette = {
  // surfaces & text (switch with dark mode)
  ink:     withOpacityValue('--color-ink'),
  paper:   withOpacityValue('--color-paper'),
  rule:    withOpacityValue('--color-rule'),
  muted:   withOpacityValue('--color-muted'),
  codeBg:  withOpacityValue('--color-codeBg'),
  preBg:   withOpacityValue('--color-preBg'),
  preFg:   withOpacityValue('--color-preFg'),

  // interactive roles (same in both modes)
  action:  tones.blue,     // links, primary CTAs
  accent:  tones.yellow,   // active nav segment, statusline highlight
  brand:   tones.orange,   // logo tint, identity mark

  // status roles
  success: tones.green,
  warning: tones.yellow,
  danger:  tones.red,
  info:    tones.cyan,
};

const fonts = {
  serif: ['"Source Serif 4"', 'Charter', 'Georgia', 'serif'],
  sans:  ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
  mono:  ['"JetBrains Mono"', 'ui-monospace', 'Menlo', 'monospace'],
};

const base = {
  fontSize:   '19px',
  lineHeight: '1.7',
  measure:    '38rem',
};

module.exports = {
  darkMode: 'class',
  content: [
    "./templates/**/*.html",
    "./content/**/*.{md,myst}",
    "./*.py",
  ],
  theme: {
    extend: {
      colors:     palette,
      fontFamily: fonts,
      maxWidth:   { prose: base.measure },
      typography: ({ theme }) => ({
        DEFAULT: {
          css: {
            fontSize:   'inherit',
            lineHeight: 'inherit',
            '--tw-prose-body':     theme('colors.ink'),
            '--tw-prose-headings': theme('colors.ink'),
            '--tw-prose-links':    theme('colors.action'),
            '--tw-prose-bold':     theme('colors.ink'),
            '--tw-prose-quotes':   theme('colors.ink'),
            '--tw-prose-bullets':  theme('colors.muted'),
            '--tw-prose-hr':       theme('colors.rule'),
            'a': {
              color: theme('colors.action'),
              textDecoration: 'underline',
              textDecorationColor: theme('colors.rule'),
              textUnderlineOffset: '4px',
              textDecorationThickness: '1px',
              fontWeight: '400',
              transition: 'color .15s, text-decoration-color .15s',
            },
            'a:hover': {
              textDecorationColor: theme('colors.action'),
            },
            'h1': { fontWeight: '700', letterSpacing: '-0.015em', fontSize: '2rem', lineHeight: '1.15', color: theme('colors.ink') },
            'h2': { fontWeight: '600', letterSpacing: '-0.01em', color: theme('colors.ink') },
            'h3, h4': { fontWeight: '600', color: theme('colors.ink') },
            'strong': { color: theme('colors.ink') },
            'em': { fontStyle: 'italic' },
            'p, li': { lineHeight: '1.7' },
            'blockquote': {
              fontStyle: 'italic',
              borderLeftColor: theme('colors.rule'),
              color: theme('colors.muted'),
              fontWeight: '400',
            },
            'code': {
              fontWeight: '400',
              fontSize: '0.9em',
              color: theme('colors.ink'),
              backgroundColor: theme('colors.codeBg'),
              padding: '0.1em 0.35em',
              borderRadius: '3px',
            },
            'code::before': { content: '""' },
            'code::after':  { content: '""' },
            'pre': {
              backgroundColor: theme('colors.preBg'),
              color:           theme('colors.preFg'),
              fontSize:   '0.85em',
              lineHeight: '1.6',
            },
            'hr': { borderColor: theme('colors.rule') },
            '.admonition': {
              backgroundColor: theme('colors.rule'),
              borderLeft: `3px solid ${theme('colors.muted')}`,
              padding: '1em 1.25em',
              margin: '2em 0',
              borderRadius: '3px',
              fontSize: '0.95em',
            },
            '.admonition > :last-child': { marginBottom: '0' },
            '.admonition > :first-child:not(.admonition-title)': { marginTop: '0' },
            '.admonition-title': {
              fontFamily:     fonts.sans.join(','),
              fontSize:       '12px',
              fontWeight:     '500',
              letterSpacing:  '0.18em',
              textTransform:  'uppercase',
              color:          theme('colors.muted'),
              marginTop:      '0',
              marginBottom:   '0.75em',
            },
          },
        },
      }),
    },
  },
  plugins: [
    require("@tailwindcss/typography"),
    plugin(function({ addBase, addComponents, theme }) {
      addBase({
        'html': {
          backgroundColor: 'rgb(var(--color-paper))',
          color:           'rgb(var(--color-ink))',
          fontFamily:      fonts.serif.join(','),
          fontSize:        base.fontSize,
          lineHeight:      base.lineHeight,
          WebkitFontSmoothing: 'antialiased',
        },
      });
      addComponents({
        '.text-display': {
          fontFamily:    fonts.serif.join(','),
          fontSize:      '1.75rem',
          lineHeight:    '1.15',
          fontWeight:    '700',
          letterSpacing: '-0.015em',
          color:         theme('colors.ink'),
        },
        '.text-meta': {
          fontFamily:     fonts.sans.join(','),
          fontSize:       '12px',
          fontWeight:     '500',
          letterSpacing:  '0.18em',
          textTransform:  'uppercase',
          color:          theme('colors.muted'),
        },
      });
    }),
  ],
};
