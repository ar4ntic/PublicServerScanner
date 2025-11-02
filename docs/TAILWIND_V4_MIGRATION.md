# Tailwind CSS v4 Migration Guide

This document explains the migration to Tailwind CSS v4 and the key differences from v3.

## What Changed

### ✅ Removed Files

- ❌ `tailwind.config.ts` - No longer needed
- ❌ `postcss.config.js` - No longer needed

### ✅ Updated Files

- ✏️ `app/globals.css` - Now uses `@import` and `@theme`
- ✏️ `package.json` - Updated to `tailwindcss@^4.0.0-alpha.25`

## New Tailwind v4 Syntax

### Old Way (v3)

**tailwind.config.ts:**
```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "hsl(221.2 83.2% 53.3%)",
      },
      borderRadius: {
        lg: "0.5rem",
      },
    },
  },
};

export default config;
```

**globals.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### New Way (v4)

**No config file needed!**

**globals.css:**
```css
@import "tailwindcss";

@theme {
  --color-primary: 221.2 83.2% 53.3%;
  --radius-lg: 0.5rem;
}
```

## Theme Configuration

### Colors

Tailwind v4 uses CSS custom properties for theming:

```css
@theme {
  /* Define colors using HSL values */
  --color-primary: 221.2 83.2% 53.3%;
  --color-secondary: 210 40% 96.1%;
  --color-accent: 210 40% 96.1%;

  /* Use in HSL format without hsl() wrapper */
  --color-border: 214.3 31.8% 91.4%;
}
```

**Usage in components:**
```tsx
<div className="bg-primary text-primary-foreground">
  Primary button
</div>
```

### Dark Mode

Dark mode is defined with a separate `@theme dark` block:

```css
@theme dark {
  --color-primary: 217.2 91.2% 59.8%;
  --color-background: 222.2 84% 4.9%;
  --color-foreground: 210 40% 98%;
}
```

### Border Radius

```css
@theme {
  --radius-lg: 0.5rem;
  --radius-md: calc(0.5rem - 2px);
  --radius-sm: calc(0.5rem - 4px);
}
```

**Usage:**
```tsx
<div className="rounded-lg">Rounded corners</div>
```

### Spacing

```css
@theme {
  --spacing-card: 1rem;
  --spacing-section: 2rem;
}
```

## Migration Steps

If you're migrating an existing project:

### 1. Update Package

```bash
npm install tailwindcss@^4.0.0-alpha.25
npm uninstall postcss autoprefixer  # No longer needed
```

### 2. Remove Config Files

```bash
rm tailwind.config.ts
rm postcss.config.js
```

### 3. Update globals.css

Replace:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

With:
```css
@import "tailwindcss";

@theme {
  /* Your custom theme */
}
```

### 4. Convert Theme Values

**Old (tailwind.config.ts):**
```typescript
theme: {
  extend: {
    colors: {
      primary: {
        DEFAULT: "hsl(221.2 83.2% 53.3%)",
        foreground: "hsl(210 40% 98%)",
      },
    },
  },
}
```

**New (globals.css):**
```css
@theme {
  --color-primary: 221.2 83.2% 53.3%;
  --color-primary-foreground: 210 40% 98%;
}
```

### 5. Test Your Build

```bash
npm run dev
# Check for any styling issues
```

## Benefits of v4

### 🚀 Performance
- Faster build times
- Smaller bundle size
- Native CSS instead of JavaScript config

### 🎨 Simpler Configuration
- No config file needed
- Direct CSS customization
- Easier to understand

### 🔧 Better CSS Integration
- Native CSS custom properties
- Works seamlessly with CSS preprocessors
- Better browser DevTools support

### 📦 Reduced Dependencies
- No PostCSS needed
- No autoprefixer needed
- Smaller node_modules

## Important Notes

### ⚠️ Alpha Version

Tailwind CSS v4 is currently in **alpha**:
- API may change before stable release
- Some plugins may not be compatible yet
- Not recommended for production until stable

### 🔄 Breaking Changes

When upgrading to stable v4:
1. Check the official migration guide
2. Update alpha version to stable
3. Test thoroughly
4. Review breaking changes

### 📚 Resources

- [Tailwind CSS v4 Alpha](https://tailwindcss.com/blog/tailwindcss-v4-alpha)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [GitHub Discussions](https://github.com/tailwindlabs/tailwindcss/discussions)

## Common Patterns

### Custom Utilities

**v3:**
```typescript
// tailwind.config.ts
plugins: [
  plugin(({ addUtilities }) => {
    addUtilities({
      '.my-custom': {
        /* styles */
      },
    })
  }),
]
```

**v4:**
```css
/* globals.css */
@utility my-custom {
  /* styles */
}
```

### Content Configuration

**v3:**
```typescript
content: ["./app/**/*.{ts,tsx}"]
```

**v4:**
Content is automatically detected! No configuration needed.

### Custom Screens

**v3:**
```typescript
theme: {
  screens: {
    'tablet': '640px',
  },
}
```

**v4:**
```css
@theme {
  --breakpoint-tablet: 640px;
}
```

## Troubleshooting

### Styles not applying?

1. Make sure `@import "tailwindcss"` is at the top of globals.css
2. Restart dev server
3. Clear `.next` cache: `rm -rf .next`

### Dark mode not working?

Ensure you have the `@theme dark` block and that your app supports dark mode class/media query.

### Custom colors not showing?

Check that color variables use the correct format:
```css
/* ✅ Correct */
--color-primary: 221.2 83.2% 53.3%;

/* ❌ Wrong */
--color-primary: hsl(221.2 83.2% 53.3%);
```

## Future-Proofing

When Tailwind v4 reaches stable:

```bash
# Update to stable version
npm install tailwindcss@4

# Check for breaking changes
npm run build

# Update any deprecated syntax
# Refer to official migration guide
```

---

**Note:** This project is using Tailwind CSS v4 alpha. Always refer to the official documentation for the latest updates and changes.
