# TODO: 答辩准备

> **最后更新**: 2026-07-25
> **当前阶段**: 论文格式修正完成，正文编译为 A4 正确格式。工作集中在 `slides/` 答辩幻灯片。

## 格式修正记录 (2026-07-25)

以下问题已修正并提交：

- [x] **纸张尺寸**: Letter → A4（原版虽指定 `[a4paper]` 但编译输出为 Letter，现已纠正）
- [x] **行距过大**: 移除 `\onehalfspacing`（与 cls 自带 `\openup 3\jot` 双倍行距叠加导致 ~27pt 行距），恢复 cls 默认 ~23.5pt 双倍行距
- [x] **超链接颜色**: 蓝色 → 黑色（`colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black`）
- [x] **页码位置**: 注释掉 `\PNumberAboveBottomMargin`，页码位于底部边距下方（模板默认位置）
- [x] **Bibliography 目录项**: 添加 `\addcontentsline{toc}{chapter}{Bibliography}`
- [x] **废弃命令**: `\sc` → `\scshape`
- [x] **附录引用**: 正文中所有 `Appendix~\ref{...}` 改为纯文字 "the supplementary material"，无超链接
- [x] **冗余格式覆盖**: 移除 `setspace`、自定义 `\parskip`/`\parindent`、`\@makecaption` 重定义、`\emergencystretch`（均与 cls 默认重复或冲突）
- [x] **main.pdf**: 119 页 Letter → 106 页 A4（页数减少因纸张变高 + 行距修正，内容未变）
- [x] **supplementary.pdf**: 51 页 A4，已按 main→supplementary→main 顺序重新编译

**编译规则**（见 `AGENTS.md`）：
1. `latexmk -xelatex main.tex`
2. `latexmk -xelatex supplementary.tex`
3. `latexmk -xelatex main.tex`
4. `latexmk -c` 清理中间文件

## 幻灯片维护

- **当前版本**: v0.5（当前最新审阅版，79 张）
- **版本规则**: v0.1–v0.4 保持不变。以后如需继续修改，按用户指示另起版本，不覆盖现有 PPTX
- **答辩日期**: 2026/7/29

## v0.4 内容审查项在 v0.5 中的处理状态

以下条目均已在 v0.5 的整体重构和证据边界校准中处理。物理页码已随 85→79 张的重排改变，最终措辞和页码以 `slides/v0.5-final-changelog.md` 为准。

- [x] 人工审计的样本量和准确率边界已改为与 thesis 及后续核查一致的保守表述
- [x] 服务部署范围已改为两个服务共五台服务器，不再暗示每个服务各五台
- [x] 自创二元框架和过强泛化已改写为 thesis-level 的三阶段 scaling 主线
- [x] `reveals nothing`、`scaling paradox`、`worthless/useless` 等过强措辞已校准
- [x] 发布状态、延迟/SLA、因果性、形式化保证和效率口径已统一到论文证据边界

## v0.5 后续准备

- [ ] 完整试讲并记录实际节奏、可跳过页和超时点
- [ ] 在内容稳定后补全主讲 notes 的转场与读图提示
- [ ] 按 validity、causality、generalizability、benchmark construction 和 production evidence 重构 Q&A bank
- [ ] 如获得实现代码，确认 SCL 的 distance/sign convention
- [ ] 仅在 v0.5 可见内容获确认后，再决定是否把构建逻辑并入长期 `slides/build.py`

## 提交前待确认

- [ ] 封面元数据：`\defencedate{2026}{7}{29}`、`\depthead`、委员会成员（`\member`）最终确认（`main.tex`）
- [ ] IEEEtran 参考文献格式是否符合委员会期望
- [ ] `chapterabstract` 环境（自定义 quote + small）渲染效果确认
