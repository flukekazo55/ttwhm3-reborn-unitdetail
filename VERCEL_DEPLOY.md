# Deploy to Vercel

This Angular 18 application is configured as a client-side SPA.

## Included configuration

- `vercel.json`
- `.vercelignore`
- `.nvmrc`
- `npm run vercel-build`

## Vercel build settings

- Framework: Angular
- Node.js: 20.x
- Build command: `npm run vercel-build`
- Output directory: `dist/warhammer3-faction-guide/browser`

## SPA routes

The Vercel rewrite falls back to `/index.html`, so direct navigation or refresh works for lazy-loaded Angular routes such as:

- `/khorne`
- `/kislev`

Static files and JSON assets are checked before the rewrite, so Angular chunks, CSS, images, and faction data continue to load normally.

## GitHub deployment

1. Push the project to GitHub.
2. In Vercel, create a project and import the repository.
3. Keep the repository root as the Root Directory.
4. Vercel reads `vercel.json`.
5. Deploy.

No environment variables are required for the current static guide.

## Vercel CLI

```bash
npm install
npx vercel
```

Production deployment:

```bash
npx vercel --prod
```
