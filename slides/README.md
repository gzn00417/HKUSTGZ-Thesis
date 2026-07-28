# Defense Slides

This directory contains the formal thesis-defense deck, milestone PPTX history,
reusable figures, and compact maintenance records.

## Current version

| File | Slides | SHA-256 | Role |
|---|---:|---|---|
| `thesis-slides-v0.9.pptx` | 69 | `467fc283fed0cca02fa4490f48fb17b6340165919141fbc094edfac96b8b4e86` | current formal defense deck |

V0.9 contains 57 main slides and 12 appendix slides. It is byte-identical to
the reviewed V0.87 deck and supersedes the V0.81–V0.87 working chain.

## Retained PPTX milestones

| Version | Role |
|---|---|
| `v0.1`–`v0.5` | early design and content evolution |
| `v0.6` | original v0.66, 79-slide stable baseline |
| `v0.7` | original v0.69, 69-slide compressed baseline |
| `v0.8` | pre-review 69-slide baseline |
| `v0.9` | reviewed formal 69-slide defense deck |

V0.81–V0.87 were working iterations rather than formal milestones. Their key
reasoning, hashes, affected sections, evidence boundaries, and QA results are
consolidated in `v0.9-build/CHANGELOG.md`. Their PPTX files and repetitive build
folders were moved to the system Trash during V0.9 promotion.

## Files to read before editing

1. `SLIDES-GUIDE.md`, the authoritative content, visual, QA, and record guide.
2. `v0.9-build/CHANGELOG.md`, the consolidated V0.8-to-V0.9 change record.
3. `v0.9-build/REVIEW.md`, the consolidated review evidence.
4. `TODO-v0.6.md`, retained evidence for earlier detailed feedback.
5. The relevant thesis chapter introduction, method passages, and conclusion.

The exact Artifact Tool editor for the final V0.86-to-V0.87 pass is retained as
`v0.9-build/edit-final-pass.mjs`. It is a historical trace, not the default
starting point for future revisions.

## Create the next branch

```bash
SLIDES_OUTPUT=slides/thesis-slides-v0.91.pptx node slides/build.mjs
```

`build.mjs` validates the canonical V0.9 hash, creates an exact
non-overwriting copy, and verifies the output hash.

## Retained historical build assets

- `build.py`: historical V0.4 design-system source.
- `v0.5-build/`: reproducible V0.5 build chain.
- `v0.5-final-changelog.md`: consolidated V0.5 modification and QA record.
- `figures/`: reusable slide figures.

## Record and cleanup policy

- Keep formal PPTX milestones, not every working iteration.
- For a major review cycle, keep one consolidated changelog, one consolidated
  review record, and only the editor that materially helps trace the final pass.
- Never overwrite a formal PPTX.
- Never permanently delete a PPTX from the project. When pruning is requested,
  notify the user and move it to the system Trash.
- Do not retain render folders, starter decks, edited candidates, layout JSON,
  extracted media, inspection output, or dependency workspaces.
