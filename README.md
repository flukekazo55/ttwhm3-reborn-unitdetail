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

## Skill plans

Cathay and Dwarfs skill plans are built from the real in-game skill trees,
scraped from totalwarhammerplanner.com with headless Chrome (the site is a JS
app, so a plain fetch returns an empty shell).

```bash
python tools/fetch-skills.py       <workdir>   # render + parse the trees
python tools/build-skill-plans.py  <workdir>   # order them into Lv 2-50
python tools/apply-skill-plans.py  <workdir>   # write into src/assets/data
```

What comes from the game: skill names, prerequisites, rank gates and effect
text. What is this guide's opinion: the *order*. The builder scores each node
against a per-lord keyword focus, then picks greedily, and asserts the result is
legal — a skill is never listed before its prerequisite or before its rank
unlocks.

Known limits:

- The table lists one skill per level. In game several skills take more than one
  point, so treat it as a priority order, not a literal point-by-point script.
- Malakai Makaisson and Valkia the Bloody have no page on the planner under any
  URL tried, so their plans are still hand-written and unverified.
- Khorne's and Kislev's original three/four lords keep their existing
  hand-written plans; nothing in this pipeline touches them.

## Faction shields

The home faction-select cards show a big faction shield as their main art — our
own flat-vector take on the Warhammer faction shield (riveted steel frame,
glossy field, faction rune), one per faction:

```bash
python tools/gen-shields.py     # -> src/assets/shields/<faction>.svg
```

## Faction emblems & the Dwarfs dark theme

Each faction card and faction hero shows a small heraldic **banner** — our own
flat-vector take (skull, Ursun bear, jade dragon, anvil on a hanging flag), not game art:

```bash
python tools/gen-emblems.py     # -> src/assets/emblems/<faction>.svg
```

Design tokens are CSS custom properties (`--c-*`) defined on `:root` in
`styles.scss`, with a dark override set under `.faction-dark`. The SCSS aliases
in `styles/variables.scss` forward to them, so component styles pick up the
theme automatically. Only the **Dwarfs** faction opts into the dark palette:
its component host carries `class: 'faction-dark'` and its card on the home page
gets `[class.faction-dark]`, so Dwarfs reads as an "under the mountain" faction
while the other three stay light.

## Chibi artwork

Every lord and unit across all four factions uses a flat-vector chibi SVG
generated from a single parameterised script, so the whole guide reads as one
art set. Each figure is assembled from shared parts — head, face, beard, helmet,
torso, arms, weapon, shield, mount, wings — and adding a unit only needs one row
in `SPECS`.

```bash
python tools/gen-chibi.py     # writes all 74 SVGs
```

Writes `src/assets/units/<faction>/chibi/<unit-id>.svg` and
`src/assets/lords/<faction>/chibi/<lord-id>-lord.svg`.

Templates: `humanoid`, `cavalry`, `beast`, `chariot`, `monster`, `artillery`,
`aircraft`, `airship`. Parts library: 20 helmets, 19 weapons, 3 beard shapes,
3 mount styles.

The original Khorne/Kislev PNGs are still on disk but no longer referenced by
any JSON — delete them with:

```bash
find src/assets -name '*.png' -delete
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

SPA fallback is configured for lazy routes such as `/khorne`, `/kislev`, `/cathay`, and `/dwarfs`.
See `VERCEL_DEPLOY.md` for details.
