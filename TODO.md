# TODO: 答辩准备

> **最后更新**: 2026-07-29
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

- **稳定基线版本**: V1（65 张，其中正文 56 张、附录 9 张）
- **保留版本**: V1、V1.4、V2 和 V3
- **当前工作版本**: V3（69 张，含 60 张正文和 9 张附录）
- **版本规则**: 后续从 V3 另起新版本，不覆盖任何已有 PPTX
- **权威维护文档**: `slides/SLIDES-GUIDE.md`
- **讲稿文件**: `slides/NOTE-V1.md`、`slides/NOTE-V1.4.md`、`slides/NOTE-V2.md`、`slides/NOTE-V3.md`
- **集中历史记录**: `slides/HISTORY.md`
- **答辩日期**: 2026/7/29

## 当前完成状态

- [x] V1 已基于作者最终保存的 V0.93 完成正文、附录和纯英文讲稿整理，并成为当前正式版本
- [x] V1 共 65 张，正文 56 张、附录 9 张；正文讲稿约 3,449 个口语词，保守估计 44–49 分钟
- [x] V1 的 65 页 PPT 备注已与 `NOTE-V1.md` 逐页核对一致
- [x] V1 已完成全量渲染、关键页全尺寸复核、边界检查、重新打开与文件完整性检查
- [x] V3 将原结论部分的 3 页压缩为 2 页，并完成全套英文讲义精简与方法白话化
- [x] V3 共 69 张，正文 60 张、附录 9 张；69 页备注已与 `NOTE-V3.md` 逐页核对一致
- [x] V3 已完成全量渲染、逐页视觉复核、边界检查、模板一致性和文件完整性检查
- [x] 早期版本、build、changelog 和用户意见已合并浓缩到 `slides/HISTORY.md`
- [x] 活跃目录仅保留 V1、V1.4、V2、V3 及其对应讲义
- [x] Study 1、Study 2、Study 3 与 Conclusion 的长期内容逻辑已记录
- [x] 用户的审美偏好、排版红线、跨页联动原则和 QA 流程已合并记录
- [x] 大体积 starter、候选 PPT、渲染、布局和 inspect 输出不再作为长期依赖
- [x] `slides/` 保留 V1、V1.4、V2、V3、必要维护记录和 figures

## 后续准备

- [ ] 完整试讲并记录实际节奏、可跳过页和超时点
- [ ] 根据完整试讲结果微调停顿、重音和可省略的口头细节
- [ ] 按 validity、causality、generalizability、benchmark construction 和 production evidence 重构 Q&A bank
- [ ] 如获得实现代码，确认 SCL 的 distance/sign convention
- [ ] 如需新增实验，仅在获得真实结果和可追溯原始材料后加入
- [ ] 答辩前重新确认 publication、acceptance、deployment 和日期表述

## 提交前待确认

- [ ] 封面元数据：`\defencedate{2026}{7}{29}`、`\depthead`、委员会成员（`\member`）最终确认（`main.tex`）
- [ ] IEEEtran 参考文献格式是否符合委员会期望
- [ ] `chapterabstract` 环境（自定义 quote + small）渲染效果确认
