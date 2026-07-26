# Defense Slides

This directory keeps five early historical decks, three key presentation
milestones, and one small set of reusable support files.

## Early historical versions

- `thesis-slides-v0.1.pptx`
- `thesis-slides-v0.2.pptx`
- `thesis-slides-v0.3.pptx`
- `thesis-slides-v0.4.pptx`
- `thesis-slides-v0.5.pptx`

These files preserve the early design and content evolution. They are not the
recommended starting point for new edits. `v0.5` is especially useful as the
last 79-slide evidence-calibrated baseline before the later v0.6x/v0.7x
restructuring.

## Presentation milestones

| File | Historical source | Role |
|---|---|---|
| `thesis-slides-v0.6.pptx` | original `v0.66` | stable 79-slide classical baseline |
| `thesis-slides-v0.7.pptx` | original `v0.69` | stable 69-slide compressed baseline |
| `thesis-slides-v0.8.pptx` | current `v0.8` | recommended 69-slide defense baseline |

The intermediate v0.6x/v0.7x iterations remain recoverable in the system Trash.
The useful revisions from `v0.75` are already inherited by `v0.8`, so those
files are not kept as additional visible milestones.

## Files to read before editing

1. `SLIDES-GUIDE.md` — authoritative design, content, QA, and iteration guide.
2. `TODO-v0.6.md` — original user feedback retained as source evidence.
3. The relevant thesis chapter introduction and conclusion.

## Code and reproducibility

- `build.mjs` is the current safe entry point. It creates a byte-identical new
  version from v0.8, refuses overwrite, validates the PPTX signature, and verifies
  the copied file by SHA-256.
- `build.py` is retained as the historical v0.4 design-system reference.
- `v0.5-build/` reproducibly rebuilds v0.5 from v0.4. It is historical code and
  must not be used as the implementation base for v0.8 edits.
- `v0.5-final-changelog.md` preserves the detailed v0.5 evidence and QA record.

`build.mjs` deliberately does not claim to reconstruct the editorial history
from v0.7 to v0.8. The reviewed v0.8 PPTX and its recorded SHA-256 are the
canonical current artifact.

## Minimal workflow

1. Start from `thesis-slides-v0.8.pptx`.
2. Create a new filename with `build.mjs`; existing files cannot be overwritten.
3. Edit only the new version.
4. Render every slide and inspect both montages and risky pages at full size.
5. Run structural, overflow, figure-identity, and package-integrity checks.
6. Record only durable decisions in `SLIDES-GUIDE.md`; do not create a new
   plan/review/QA file for every minor iteration.

Figures used by the deck are in `figures/`.

## Recovery

Unselected intermediate decks, superseded newer build folders, render outputs,
and detailed iteration records were moved, not permanently deleted, to:

`/Users/guozhuoning/.Trash/HKUSTGZ-Thesis-slides-cleanup-20260727`
