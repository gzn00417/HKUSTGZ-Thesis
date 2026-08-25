# Project Status

> **状态**: 论文已定稿提交，答辩已完成。开发与写作全部结束。
> **答辩日期**: 2026年7月29日
> **最终提交文件**: `main.pdf`（A4，135 页）

## 已完成

- 论文正文（Ch1–6 + Appendix A: Publication List）已定稿并通过全量逐页复核
- 原附录 A–C 实质内容已整合至 Ch3–5，`main.pdf` 自包含可独立阅读
- 格式修正完成：A4 纸张、行距、超链接黑色、目录层级、附录引用等
- Publication List 已从 Chapter 7 改为 Appendix A
- 答辩幻灯片 V3 为最终版本，`slides/` 保留全部历史版本

## 已知保留项（无需修改）

- 编译日志有少量 overfull/underfull 提示，逐页检查无裁切或重叠
- Times New Roman 缺少部分 small-caps 字形，XeLaTeX 用可用字形替代，无乱码
- 少数高密度表格使用 `\footnotesize`，Ch4 超宽曲线用横向页面，均为可读性保留的局部例外
- `appendices/` 保留迁移来源，不参与构建，正式提交文件为 `main.pdf`
