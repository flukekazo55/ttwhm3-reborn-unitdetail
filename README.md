# Warhammer III Faction Guide — Angular 18

Angular 18.1 project refactored to **one lazy-loaded feature module per faction**, following the conventions from `flukekazo55/angular-v18-ai-skill`.

## Lazy-load architecture

```text
/khorne
  -> KhorneModule (lazy)
  -> Khorne NgRx feature state/effect
  -> assets/data/khorne.json only

/kislev
  -> KislevModule (lazy)
  -> Kislev NgRx feature state/effect
  -> assets/data/kislev.json only
```

Shared presentation components (`Lord`, `Skill Build`, `Unit Card`, faction renderer) live in `GuideSharedModule`. They contain no faction data and can be reused by future modules.

## Main structure

```text
src/app/
├── modules/
│   ├── khorne/
│   │   ├── khorne.module.ts
│   │   └── khorne.component.*
│   └── kislev/
│       ├── kislev.module.ts
│       └── kislev.component.*
├── services/
│   ├── khorne/khorne.service.ts
│   └── kislev/kislev.service.ts
└── shared/
    ├── models/guide.model.ts
    ├── modules/guide-shared/
    ├── stores/khorne/
    ├── stores/kislev/
    └── utils/guide-mapper.ts

src/assets/data/
├── khorne.json
└── kislev.json
```

## Routes

- `/khorne` — loads only Khorne feature + Khorne JSON
- `/kislev` — loads only Kislev feature + Kislev JSON
- `/` redirects to `/khorne`

## Run

```bash
npm install
npm start
```

## Why this is lighter

The root app no longer registers a combined `GuideModule`, combined NgRx state, or a `guide.json` containing every faction. Each faction's module, effects, store registration, and JSON request happen only after navigating to that faction route.


## Deploy to Vercel

Vercel deployment files are included in the repository root.

```bash
npm run vercel-build
```

Output:

```text
dist/warhammer3-faction-guide/browser
```

SPA fallback is configured for lazy routes such as `/khorne` and `/kislev`.
See `VERCEL_DEPLOY.md` for details.
