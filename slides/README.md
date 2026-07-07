# Defense Slides

## Files

- `thesis-slides-v0.3.pptx` — current version
- `thesis-slides-v0.2.pptx` — previous version
- `thesis-slides-v0.1.pptx` — initial version
- `build.py` — reference implementation that generates the deck from PNGs
- `figures/` — PNGs used by the current deck

## How figures are used

`build.py` places PNGs onto slides via `pic(s, "name", ...)`. Each call maps to `figures/name.png`:

```
pic(s, "gve/model", ...)           → figures/gve/model.png
pic(s, "mglvr/d2s", ...)           → figures/mglvr/d2s.png
pic(s, "thesis-framework", ...)    → figures/thesis-framework.png
```

The 17 images currently in `figures/` are exactly those referenced by `build.py`. They are high-res rasterizations of the vector PDFs in the repository-level `figures/{gve,mglvr,gmpgr}/`.

## How to add a figure back

If you need a figure that was removed (not referenced by the current deck):

1. Go to the repository-level `figures/{gve,mglvr,gmpgr}/<name>.pdf`
2. Rasterize to PNG at 2x-4x the vector size (e.g. via PyMuPDF)
3. Save to `slides/figures/{gve,mglvr,gmpgr}/<name>.png`
4. Add a `pic(s, "subdir/name", ...)` call in `build.py`

## Design Strategy

- **Thesis-level argument**, not three paper talks
- **55–60 main slides** + **15–25 backup** for a 50–60 minute defense
- **Claim-driven titles**, fewer full tables, more visual evidence
- **Times New Roman only**, one font size per role, no auto-shrink
- **Palette**: NAVY/GOLD/GREEN/RED/MUTED; no hand-drawn diagrams
- **Self-contained slides**: claim + evidence + how-to-read + thesis connection on key pages

## Iteration History

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | Jul 3 | Initial build with basic structure |
| v0.2 | Jul 3 | Incremental revision: factual fixes, visual hierarchy, layout polish |
| v0.3 | Jul 7 | Aesthetic pass: chrome, takeaway grading, figure heroes, de-grid; content-faithfulness pass: wording fixes, figure callouts, narrative coherence |

## Key Design Decisions

- Figures organized by paper: `gve/` (Ch3), `mglvr/` (Ch4), `gmpgr/` (Ch5)
- `thesis-framework.png` at figures root (cross-chapter overview)
- Only PNGs referenced by `build.py` are kept
- All changes validated against `main.tex` / `THESIS_OUTLINE.md`

## Rules & Guidelines

### Version Management
- **永远另起新版本**（如 v0.4），直到用户明确说"v0.4 可以定稿"
- 不要修改现有版本文件，每次更新都创建新的 pptx 文件
- 旧版本保留作为参考和回滚点
- **绝对不要删除 pptx 文件**，即使用户要求也只能移到回收站，必须先通知用户

### Content Consistency
- 所有修改必须与 `main.tex` 和 `THESIS_OUTLINE.md` 保持一致
- 数值、引用、结论必须与论文正文完全匹配
- 图表标注（如 Fig. 1, Table 2）必须与论文中的标注一致
- 更新论文内容后，同步检查 slides 是否需要更新

### Figure Management
- Figures 按论文组织：`gve/` (Ch3), `mglvr/` (Ch4), `gmpgr/` (Ch5)
- `thesis-framework.png` 在 figures 根目录（跨章节概览）
- 只保留 `build.py` 引用的 PNG，删除前先确认无引用
- 需要新 figure 时，从仓库级 `figures/{gve,mglvr,gmpgr}/<name>.pdf` 光栅化

### Design Principles
- **Thesis-level argument**，不是三个 paper talks
- **55–60 main slides** + **15–25 backup** for 50–60 min defense
- **Claim-driven titles**，少用表格，多用视觉证据
- **Times New Roman only**，每个角色一个字号，不自动缩放
- **Palette**: NAVY/GOLD/GREEN/RED/MUTED，不用手绘图
- **Self-contained slides**: 关键页包含 claim + evidence + how-to-read + thesis connection

### Common Mistakes to Avoid
- ❌ 直接删除 pptx 文件
- ❌ 覆盖现有版本而不是创建新版本
- ❌ 假设某个 figure 不再需要而不检查 build.py
- ❌ 修改论文内容后忘记同步 slides
- ❌ 图表标注与论文不一致
- ❌ 在 slides 中使用论文中没有的术语或缩写
