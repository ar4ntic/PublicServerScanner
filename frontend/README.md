# PublicScanner Frontend

Next.js 14 frontend application for PublicScanner.

## Tech Stack

- **Next.js 14** - App Router
- **TypeScript** - Type safety
- **Tailwind CSS v4** - Styling (using new @import syntax)
- **React Query** - Data fetching
- **Zod** - Schema validation
- **React Hook Form** - Form handling

## Tailwind CSS v4

This project uses Tailwind CSS v4 (alpha) with the new simplified configuration:

- ✅ No `tailwind.config.ts` needed
- ✅ No `postcss.config.js` needed
- ✅ Configuration via `@theme` in CSS
- ✅ Direct `@import "tailwindcss"` in globals.css

### Theme Configuration

All theme customization is done in `app/globals.css` using the `@theme` directive:

```css
@import "tailwindcss";

@theme {
  --color-primary: 221.2 83.2% 53.3%;
  --radius-lg: 0.5rem;
}

@theme dark {
  --color-primary: 217.2 91.2% 59.8%;
}
```

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run type-check
```

## Project Structure

```
frontend/
├── app/
│   ├── (auth)/          # Auth routes (grouped)
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/       # Protected routes
│   ├── globals.css      # Tailwind v4 config
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Home page
│   └── providers.tsx    # React Query provider
├── components/
│   ├── ui/             # Reusable UI components
│   └── layout/         # Layout components
├── lib/                # Utilities
├── hooks/              # Custom React hooks
└── utils/              # Helper functions
```

## Features

- ✅ Server-side rendering (SSR)
- ✅ App Router with layouts
- ✅ TypeScript strict mode
- ✅ ESLint + Prettier configured
- ✅ Dark mode support
- ✅ Responsive design
- ✅ Form validation with Zod
- ✅ API integration ready

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8080
```

## Notes

- Using Tailwind CSS v4 alpha - expect breaking changes
- When v4 is stable, update package version
- Custom theme values use CSS variables
- No JavaScript config needed for Tailwind
