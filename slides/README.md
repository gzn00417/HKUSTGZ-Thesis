# Defense Slides

The root of `slides/` currently keeps four presentation milestones.

| Version | Deck | Speaker notes | Role |
|---|---|---|---|
| V1 | `thesis-slides-v1.pptx` | `NOTE-V1.md` | retained stable 65-slide defense deck |
| V1.4 | `thesis-slides-v1.4.pptx` | `NOTE-V1.4.md` | retained author-reviewed intermediate version |
| V2 | `thesis-slides-v2.pptx` | `NOTE-V2.md` | retained 70-slide pre-compression version |
| V3 | `thesis-slides-v3.pptx` | `NOTE-V3.md` | current 69-slide working version |

V3 contains 60 main slides and 9 appendix slides. The three study-level
related-work pages remain labeled R1, R2, and R3. V3 compresses the former
three-page conclusion synthesis into two pages: the research logic and the
technical novelty/contributions.

## Files

- `SLIDES-GUIDE.md`: authoritative revision and QA guide.
- `HISTORY.md`: consolidated version lineage, durable feedback, change record,
  formula checks, timing, and QA history.
- `figures/`: reusable source figures.
- `.cleanup-review/`: Git-ignored local recovery material. It is not part of the
  active slide workspace.

## Editing policy

1. Read `SLIDES-GUIDE.md` and the relevant section of `HISTORY.md`.
2. Use V3 as the current working source unless the user specifies otherwise.
3. Always create a non-overwriting revision.
4. Keep temporary build scripts, renders, and inspection files outside
   `slides/`.
5. After content or layout changes, render and inspect every slide and verify the
   PPTX package.

Historical PPTX files, build scripts, and individual changelogs were consolidated
out of the active directory. Their durable information remains in `HISTORY.md`,
and local recovery copies remain available under `.cleanup-review/`.
