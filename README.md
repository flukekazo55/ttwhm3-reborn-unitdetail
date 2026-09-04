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

/cathay
  -> CathayModule (lazy)
  -> Cathay NgRx feature state/effect
  -> assets/data/cathay.json only

/dwarfs
  -> DwarfsModule (lazy)
  -> Dwarfs NgRx feature state/effect
  -> assets/data/dwarfs.json only
```

Shared presentation components (`Lord`, `Skill Build`, `Unit Card`, faction renderer) live in `GuideSharedModule`. They contain no faction data and can be reused by future modules.

## Main structure

```text
src/app/
├── modules/
│   ├── khorne/
│   │   ├── khorne.module.ts
│   │   └── khorne.component.*
│   ├── kislev/
│   │   ├── kislev.module.ts
│   │   └── kislev.component.*
│   ├── cathay/
│   │   ├── cathay.module.ts
│   │   └── cathay.component.*
│   └── dwarfs/
│       ├── dwarfs.module.ts
│       └── dwarfs.component.*
├── services/
│   ├── khorne/khorne.service.ts
│   ├── kislev/kislev.service.ts
│   ├── cathay/cathay.service.ts
│   └── dwarfs/dwarfs.service.ts
└── shared/
    ├── models/guide.model.ts
    ├── modules/guide-shared/
    ├── stores/khorne/
    ├── stores/kislev/
    ├── stores/cathay/
    ├── stores/dwarfs/
    └── utils/guide-mapper.ts

src/assets/data/
├── khorne.json
├── kislev.json
├── cathay.json
└── dwarfs.json
```

## Routes

- `/khorne` — loads only Khorne feature + Khorne JSON
- `/kislev` — loads only Kislev feature + Kislev JSON
- `/cathay` — loads only Cathay feature + Cathay JSON
- `/dwarfs` — loads only Dwarfs feature + Dwarfs JSON
- `/` shows the faction picker (Home)

## Run

```bash
npm install
npm start
```

## Chibi artwork

Cathay, Dwarfs and Valkia use flat-vector chibi SVGs generated from a single
parameterised script — each figure is assembled from shared parts (head, beard,
helmet, torso, weapon, shield, mount, ...) so adding a unit only needs one row
in `SPECS`.

```bash
python tools/gen-chibi.py
```

Writes `src/assets/units/<faction>/chibi/<unit-id>.svg` and
`src/assets/lords/<faction>/chibi/<lord-id>-lord.svg`. Khorne and Kislev keep
their existing hand-made PNGs; `imageUrl` / `portraitUrl` in the JSON just point
at whichever file exists.

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

SPA fallback is configured for lazy routes such as `/khorne`, `/kislev`, `/cathay`, and `/dwarfs`.
See `VERCEL_DEPLOY.md` for details.
