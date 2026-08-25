# AGENTS.md

## Current Phase

The thesis is **finalized and submitted**. The defense was held on 2026-07-29. No further prose edits, recompilation, or content changes are expected. `main.pdf` is the final submission file. Slides in `slides/` are retained as historical artifacts.

## Slides (Archival)

The defense was held on 2026-07-29. The following versions are retained as historical artifacts:

- `thesis-slides-v1.pptx` — retained stable 65-slide defense deck
- `thesis-slides-v1.4.pptx` — author-reviewed intermediate state
- `thesis-slides-v2.pptx` — 70-slide pre-compression state
- `thesis-slides-v3.pptx` — final 69-slide deck with two-page contribution synthesis
- `slides/NOTE-V3.md` — final speaker notes
- `slides/README.md` — version index and directory structure

## Build

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
latexmk -c  # clean auxiliary files
```

Compiler: XeLaTeX only. Template files `ustthesis.cls` / `ustthesis.sty` must not be modified.

The current `main.tex` is self-contained and has no cross-document reference dependency. `latexmk` performs the required reruns for stable internal references.

## Structure

- `main.tex` — self-contained thesis (chapters 1–6, Appendix A: Full Publication List, then bibliography)
- `chapters/*.tex` — one file per chapter (00-abstract through 07-publications); `07-publications.tex` is loaded as Appendix A via `\appendix` before the bibliography. `00-acknowledgments.tex` is loaded via `\input{}` inside the `\acknowledgments` environment
- `appendices/*.tex` — retained migration sources; not loaded by the current thesis build
- `figures/{gve,mglvr,gmpgr}/` — figures for Ch3, Ch4, Ch5 respectively
- `references/references.bib` — single consolidated bibliography
- `STYLE.md` — prose style rules (archival reference)
- `TODO.md` — project completion status and known retained items

This project is finalized. `TODO.md` and `README.md` serve as archival records. Do not create additional thesis review or changelog files.

## LaTeX Conventions

- Floats: use `[t]` for figures and tables. A local `[!t]` is permitted only for a near-page-height object that must remain at the top and would otherwise create a sparse preceding page. Verify placement in the rendered PDF because the specifier alone does not ensure proximity or balanced page density.
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
| Ch3 | MM 2026 (accepted) | UVR framework, GVE model |
| Ch4 | AAAI 2027 (submitted) | MG-LVR benchmark, VEterfall |
| Ch5 | WebConf 2026 | MUIRML metric, HiPANNS |

Source papers live in `../Paper-LaTeX-Projects/` and PDFs in `../Paper-PDFs/`.
