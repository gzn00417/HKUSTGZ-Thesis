# TODO: 答辩准备

> **最后更新**: 2026-07-28
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

- **当前推荐版本**: V0.9（69 张，其中正文 57 张、附录 12 张）
- **早期历史版本**: v0.1–v0.5 保留在 `slides/`，用于追溯早期设计与内容演进
- **保留里程碑**:
  - v0.6 = 原 v0.66（79 张稳定基线）
  - v0.7 = 原 v0.69（69 张压缩基线）
  - v0.8 = V0.81 审阅前的 69 张基线
  - V0.9 = 合并 V0.81–V0.87 审阅过程后的正式 69 张答辩版本
- **版本规则**: 后续从 V0.9 另起 V0.91 或更高版本，不覆盖任何已有 PPTX
- **权威维护文档**: `slides/SLIDES-GUIDE.md`
- **原始用户意见**: `slides/TODO-v0.6.md`
- **答辩日期**: 2026/7/29

## 当前完成状态

- [x] 三个公开里程碑已按 v0.6、v0.7、v0.8 统一命名
- [x] v0.6、v0.7 从原 v0.66、v0.69 文件直接恢复，未重新导出
- [x] V0.9 已完成全量文字、逻辑和证据边界精修，并成为当前正式版本
- [x] v0.1–v0.5 作为早期历史版本保留，不纳入当前三个关键里程碑
- [x] v0.1–v0.5 的关键设计、内容校准和技术经验已精炼写入长期指南
- [x] v0.4 设计系统、v0.5 可复现构建链和 v0.5 完整 changelog 已保守保留
- [x] 当前 `build.mjs` 校验 V0.9 规范哈希并非覆盖派生新版本
- [x] V0.81–V0.87 的关键修改、论文来源和保留风险已合并进 `v0.9-build/`
- [x] Study 1、Study 2、Study 3 与 Conclusion 的长期内容逻辑已记录
- [x] 用户的审美偏好、排版红线、跨页联动原则和 QA 流程已合并记录
- [x] 大体积 starter、候选 PPT、渲染、布局和 inspect 输出不再作为长期依赖
- [x] `slides/` 仅保留 V0.1–V0.8 与 V0.9 里程碑、必要编辑记录和 figures

## 后续准备

- [ ] 完整试讲并记录实际节奏、可跳过页和超时点
- [ ] 在内容稳定后补全主讲 notes 的转场与读图提示
- [ ] 按 validity、causality、generalizability、benchmark construction 和 production evidence 重构 Q&A bank
- [ ] 如获得实现代码，确认 SCL 的 distance/sign convention
- [ ] 如需新增实验，仅在获得真实结果和可追溯原始材料后加入
- [ ] 答辩前重新确认 publication、acceptance、deployment 和日期表述

## 提交前待确认

- [ ] 封面元数据：`\defencedate{2026}{7}{29}`、`\depthead`、委员会成员（`\member`）最终确认（`main.tex`）
- [ ] IEEEtran 参考文献格式是否符合委员会期望
- [ ] `chapterabstract` 环境（自定义 quote + small）渲染效果确认
