# Writing Style Guide

> **当前状态**: 论文已定稿提交，开发与写作全部结束。本文档作为归档参考保留。

This document defines the editing standards for this thesis. It must be read before editing any `.tex` file. The goal is submission-ready academic prose for top-tier CS venues (NeurIPS, ICLR, ICML, CVPR, ECCV, etc.), produced in a single editing pass.

## Chapter Edit Restrictions

Chapters 3, 4, 5 are derived from published/submitted conference papers. **Do not modify their content** except for:
- Formatting fixes (LaTeX commands, float placement, table layout)
- Factual errors (wrong numbers, incorrect references)
- Grammar errors (spelling, article usage, subject-verb agreement)

Do not rephrase, restructure, or rewrite sentences in these chapters for style alone.

The explicitly authorized appendix-integration pass is complete. Its retained structural rule is that supporting configurations, analyses, and figures remain adjacent to the experiment or claim they explain. New material must not be appended as an undifferentiated block at the end of a chapter. Each technical chapter ends with `Chapter Summary`, while the thesis-level conclusion remains in Chapter 6.

## Core Principles

1. **One-pass resolution**. Fix all grammar, style, and AI-trace issues in a single pass. Do not leave follow-up work.
2. **Minimal modification**. Every change must improve readability or rigor. No meaningless word swaps or sentence restructures for the sake of change.
3. **Content fidelity**. Never alter core arguments, experimental results, data, conclusions, or reasoning logic.
4. **Style consistency**. The final text must read as if written by one author in one voice, with no traces of different editing stages.

## Punctuation

- **No em dashes** (`---`). Replace with commas, parentheses, or clause restructuring.
- **No semicolons** (`;`). Split into separate sentences with periods.
- Colons (`:`) are acceptable for introducing explanations or lists.

## Formatting

- Keep table captions at the template default size. Use the body-text default for ordinary table contents. Use `\footnotesize` only for genuinely dense tables and `\scriptsize` only when a wide result table cannot otherwise fit.
- Use `[t]` for figures and tables. A local `[!t]` may be used for a near-page-height object when it remains top-aligned and prevents a sparse preceding page. The rendered PDF must also keep each float close to its first substantive discussion, avoid sparse float-only pages, and preserve a continuous reading order around landscape material. Avoid `\clearpage`. A local float barrier may be used only at a genuine semantic boundary and only when it does not create a visibly underfilled preceding page. Keep portrait orientation by default. Retain a landscape page only when it materially improves final-size legibility and does not fracture the surrounding prose.

- **Minimize `\textbf{}`**. Only use for:
  - List item labels (e.g., `\item \textbf{Coarse-grained retrieval}`)
  - Core thesis concepts defined in this work (e.g., semantic scale, observational scale, search scale)
  - First occurrence of key abbreviations (e.g., `\textbf{Approximate Nearest Neighbor Search (ANNS)}`)
- Do not bold well-established technical terms (e.g., dual-encoder architecture, two-tower architecture, spatiotemporal sampling).
- **Strictly prohibit** adding any emphasis formatting (`\textbf{}`, `\emph{}`, `\underline{}`) not present in the original.

## Editing Philosophy

- **Minimal changes**. Do not rewrite sentences that are already correct and natural.
- **Preserve word diversity**. When replacing overused words (e.g., "leverage"), do not replace every instance. Keep some original choices to maintain natural variation across the text.
- **No unnecessary rephrasing**. If a sentence is grammatically correct and reads naturally, leave it as is.
- **Structure preservation**. Maintain original paragraph structure. Do not convert paragraphs into lists, nor merge lists into paragraphs.

## Deep Polishing

- Correct all spelling, grammar, punctuation, and article usage errors.
- Optimize sentence structures to conform to top-conference writing conventions and enhance logical coherence.
- Eliminate awkwardness and ambiguity caused by non-native writing.
- Prefer "of" constructions over possessive noun forms (e.g., "the performance of METHOD" instead of "METHOD's performance").
- Prioritize universally understandable vocabulary. Reject flowery or obscure word choices.

## Redline Review

- Identify and correct statements that are self-contradictory.
- Check and unify terminology usage for core concepts across the text.
- Correct severe grammatical errors and Chinglish that obscure meaning.
- **Retain the original text** for all "optional" style issues. If it is not clearly wrong, do not change it.

## De-AI Guidelines

- Replace clearly AI-characteristic words selectively:
  - "leverage" → "use" / "adopt" / "based on" (but keep some "leverage" instances for variety)
  - "delve into" → "investigate" / "examine"
  - "tapestry" → "context" / "landscape"
- Remove filler transition phrases: "Importantly,", "It is worth noting that", "First and foremost". Connect sentences naturally through logical progression.
- Avoid overly regular and symmetrical sentence structures. Introduce natural linguistic variation.
- Retain the original text if it is already natural, authentic, and free of obvious AI characteristics.
- The goal is natural academic prose, not a complete vocabulary overhaul.

## Academic Register

- No contractions (use "it is", "does not", etc.).
- Standard academic written English throughout.
- Use universally understandable vocabulary. Reject flowery or obscure word choices.

## Overclaim Avoidance

- Avoid absolute or universal claims ("cannot", "no amount of", "fundamental", "must") where the evidence only supports an empirical tendency.
- Thesis-level claims should be scoped: use "within the scope of this thesis", "across the three stages studied", or similar qualifiers.
- Prefer empirical/operational formulations over definitional/philosophical ones. For example, "generalizability serves as an empirical criterion" rather than "generalizability is the validation".
- Do not use memorable slogans as thesis claims. Let the argument speak through its logic and evidence.
- When describing findings, use "consistent" rather than "fundamental", "is not eliminated" rather than "cannot be resolved", "alone is insufficient" rather than "no amount of X can compensate for".

## LaTeX Integrity

- Strictly preserve all LaTeX commands (`\cite{}`, `\ref{}`, `\eg`, `\ie`, etc.), mathematical formulas, and special characters (properly escape `%`, `_`, `&`).
- `\ie` and `\eg` should be followed by a comma when used mid-sentence: `\ie, retrieval` not `\ie retrieval`.
- Do not expand common domain abbreviations (e.g., LLM, CNN, Transformer) or arbitrarily change the names of defined core concepts.
- Retain existing formatting settings in the original text.

## Execution Protocol

Before finalizing any edit, verify:
1. All LaTeX commands, formulas, and special characters are correctly preserved.
2. No changes have been made to core arguments, data, or reasoning logic.
3. All modifications are necessary. No changes made just for the sake of change.
4. The final text has a natural tone that approximates the writing style of native-speaking human researchers.
5. No formatting or content not present in the original has been added.
