# AGENTS.md

## Current Phase

Thesis body (chapters 1–7, appendices) is **frozen** — no further content edits. All ongoing work is in `slides/`.

## Slides

- `slides/` — defense slides, retained milestones, one safe branching script,
  reusable figures, and the consolidated maintenance guide
- **Early history**: preserve `thesis-slides-v0.1.pptx` through
  `thesis-slides-v0.5.pptx` in `slides/`. They are historical references, not
  the starting point for new edits. v0.5 is the last 79-slide evidence-calibrated
  baseline before the later restructuring.
- **Historical milestones**:
  - `thesis-slides-v0.6.pptx` = original v0.66, 79-slide stable baseline
  - `thesis-slides-v0.7.pptx` = original v0.69, 69-slide compressed baseline
  - `thesis-slides-v0.8.pptx` = pre-review 69-slide baseline
- **Current stable version**:
  - `thesis-slides-v0.9.pptx` = current formal 69-slide defense deck
  - V0.81 through V0.87 were working iterations. Their key modification
    process is consolidated in `slides/v0.9-build/`.
- **Version management**: always create a new version; never overwrite existing pptx. The current version is not final until explicitly stated.
- **Never delete pptx files** directly. If deletion is requested, only move to trash after notifying.
- Start future work from V0.9 and use `slides/build.mjs` only to create a
  non-overwriting branch such as V0.91.
- Use `slides/v0.9-build/CHANGELOG.md` and `slides/v0.9-build/REVIEW.md` to
  trace the V0.8-to-V0.9 review. The retained final-pass editor is
  `slides/v0.9-build/edit-final-pass.mjs`.
- `slides/build.py`, `slides/v0.5-build/`, and
  `slides/v0.5-final-changelog.md` are retained historical v0.4/v0.5
  reproducibility assets. Do not use them as the implementation base for V0.9.
- Read `slides/SLIDES-GUIDE.md` before every slide revision. It is the
  authoritative source for thesis alignment, cross-page reasoning, aesthetics,
  known failure cases, QA, and record policy.
- Retain `slides/TODO-v0.6.md` as source evidence for the user's detailed
  feedback.
- Retain `slides/v0.9-build/REVIEW.md` as the consolidated V0.81 review
  evidence. The duplicate raw review file was moved to Trash during V0.9
  promotion.
- After slide-content or layout changes, render and inspect every slide. Automated
  overflow checks do not replace full-size visual review.
- See `slides/README.md` for the concise file index and recovery information.

## Build

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error supplementary.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex   # second pass for cross-refs
latexmk -c  # clean auxiliary files
```

Compiler: XeLaTeX only. Template files `ustthesis.cls` / `ustthesis.sty` must not be modified.

**Build order**: main must be compiled first (generates `main.aux`), then supplementary (reads `main.aux` for `\ref{}` to chapter labels), then main again (reads `supplementary.aux` for `\ref{}` to appendix labels). Both documents use `xr-hyper` for cross-document references.

## Structure

- `main.tex` — main thesis (chapters 1–6, publications, bibliography; no appendices)
- `supplementary.tex` — supplementary material (appendices A–C + own bibliography)
- `chapters/*.tex` — one file per chapter (00-abstract through 07-publications); `00-acknowledgments-zh.tex` is a Chinese reference draft (not \input{} by main.tex)
- `appendices/*.tex` — appendix chapters (loaded by `supplementary.tex`, not `main.tex`)
- `figures/{gve,mglvr,gmpgr}/` — figures for Ch3, Ch4, Ch5 respectively
- `references/references.bib` — single consolidated bibliography
- `STYLE.md` — prose style rules (must read before editing any `.tex`)
- `TODO.md` — slides preparation checklist

## LaTeX Conventions

- Floats: prefer `[t]` placement in main text; `[htbp]`/`[ht]` only in appendices.
- Wide tables: use `tabularx` or `tabular*{\linewidth}`. Never use `resizebox`, `adjustbox`, or `wraptable`.
- Font scaling: if a table must be smaller, use `\footnotesize` or `\scriptsize` only.
- Captions: use template default font size. Do not use `\captionof` inside a `figure` environment (use `\caption` instead).
- `\graphicspath` is set to `{{figures/gve/}{figures/mglvr/}{figures/gmpgr/}}`.

## Chapter Edit Restrictions

Chapters 3, 4, 5 are derived from published/submitted conference papers. **Do not modify their content** except for:
- Formatting fixes (LaTeX commands, float placement, table layout)
- Factual errors (wrong numbers, incorrect references)
- Grammar errors (spelling, article usage, subject-verb agreement)

Do not rephrase, restructure, or rewrite sentences in these chapters for style alone.

## Writing Style

Read `STYLE.md` before editing prose. Key rules:
- No em dashes (`---`). Use commas, parentheses, or clause restructuring.
- No semicolons (`;`). Split into separate sentences.
- Minimize `\textbf{}`. Only for list labels, thesis-defined core concepts, and first-use abbreviations.
- Minimal edits: do not rewrite correct sentences. Preserve word-choice diversity.
- No contractions. Standard academic English.

## Chapter-to-Conference Mapping

| Chapter | Conference | Key Artifacts |
|---------|-----------|---------------|
| Ch3 | MM 2026 | UVR framework, GVE model |
| Ch4 | ECCV 2026 | MG-LVR benchmark, VEterfall |
| Ch5 | WebConf 2026 | MUIRML metric, HiPANNS |

Source papers live in `../Paper-LaTeX-Projects/` and PDFs in `../Paper-PDFs/`.
