# TODO: 答辩准备

> **最后更新**: 2026-07-18
> **当前阶段**: 论文正文已提交并冻结。所有工作集中在 `slides/` 答辩幻灯片。

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

## 待确认

- 封面元数据：答辩日期、系主任、导师姓名等最终确认（`main.tex`）
