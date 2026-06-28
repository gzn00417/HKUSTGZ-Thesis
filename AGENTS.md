# AGENTS.md

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
- `TODO.md` — known issues and risks (check before claiming something is "done")

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
