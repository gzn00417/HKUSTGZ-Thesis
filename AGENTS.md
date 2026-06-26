# AGENTS.md

## Build

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
latexmk -c  # clean auxiliary files
```

Compiler: XeLaTeX only. Template files `ustthesis.cls` / `ustthesis.sty` must not be modified.

## Structure

- `main.tex` — entry point, loads all chapters
- `chapters/*.tex` — one file per chapter (00-abstract through 07-publications)
- `appendices/*.tex` — appendix chapters
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
