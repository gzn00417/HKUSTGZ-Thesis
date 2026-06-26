# HKUST(GZ) Thesis: Towards Scalable and Generalizable Video Retrieval

> **作者**: 郭茁宁 (Zhuoning Guo)  
> **学位**: PhD (哲学博士)  
> **专业**: Doctor of Philosophy in Artificial Intelligence  
> **院系**: Thrust of Artificial Intelligence  
> **导师**: Prof. Xiaowen Chu, Prof. Renjing Xu  
> **答辩日期**: 2026年7月29日

---

## 当前状态

- 编译状态：待验证（需本地编译环境）
- 输出文件：[main.pdf](main.pdf)（上次编译: 157页）
- 最近审查：2026-06-26 全面复查，确认 Ch2 清理完毕，发现 Ch4/Ch5/Ch6 及附录仍有 15 项待修复问题（详见 [TODO.md](TODO.md)）
- 最近修复：2026-06-25 全文审查，修复拼写/语法、数据错误、LaTeX 标签适配、投稿模板残留等 23 项问题
- 写作规范：已建立 [STYLE.md](STYLE.md)（写作风格指南）和 [AGENTS.md](AGENTS.md)（AI 助手指令），供后续编辑参考
- 模板文件：`ustthesis.cls` / `ustthesis.sty` 保持与 `../Template-of-HKUST-GZ-Thesis` 一致
- 格式更新：第三章 Table 3.1--3.3 已按 `\linewidth` 页宽排版；caption 字体保持模板默认大小

## 快速开始

### 1. 编译论文

```bash
# 进入论文目录
cd HKUSTGZ-Thesis

# 使用 latexmk 自动编译（推荐）
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex

# 或手动编译
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex

# 清理辅助文件
latexmk -c
```

### 2. 查看输出

编译完成后查看 `main.pdf`。

### 3. 修改内容

- 章节内容：编辑 `chapters/*.tex`
- 参考文献：编辑 `references/references.bib`
- 图片资源：添加到 `figures/` 对应子目录

---

## 论文概述

本论文研究视频检索的可扩展性和泛化性问题，从三个相互关联的维度展开：

| 研究维度 | 核心问题 | 对应章节 |
|---------|---------|---------|
| **语义尺度** | 如何学习支持多样化查询的通用检索表示 | Chapter 3 |
| **观测尺度** | 视频采样密度如何影响检索质量 | Chapter 4 |
| **搜索尺度** | 如何在大规模候选集合中高效执行检索 | Chapter 5 |

---

## 项目结构

```
HKUSTGZ-Thesis/
├── main.tex                 # 主编译文件
├── main.pdf                 # 编译输出
├── chapters/                # 论文章节
│   ├── 00-abstract.tex      # 摘要
│   ├── 00-acknowledgments.tex # 致谢
│   ├── 01-introduction.tex  # 引言
│   ├── 02-related-work.tex  # 相关工作
│   ├── 03-universal-video-retrieval.tex  # 第三章
│   ├── 04-spatiotemporal-scaling.tex     # 第四章
│   ├── 05-scale-efficient-retrieval.tex  # 第五章
│   ├── 06-conclusion.tex    # 结论
│   └── 07-publications.tex  # 发表论文
├── appendices/              # 附录
├── figures/                 # 图片资源
│   ├── gve/                 # 第三章图片
│   ├── mglvr/               # 第四章图片
│   └── gmpgr/               # 第五章图片
├── references/              # 参考文献
│   └── references.bib       # 整合的参考文献
├── ustthesis.cls            # 论文模板类文件
├── ustthesis.sty            # 模板样式文件
├── STYLE.md                 # 写作风格指南（编辑 .tex 前必读）
├── AGENTS.md                # AI 助手指令
├── README.md                # 本文件
└── TODO.md                  # 待解决问题清单
```

---

## 论文与会议论文对应关系

| 章节 | 会议论文 | 核心贡献 |
|-----|---------|---------|
| Ch.3 | MM2026 | UVR能力框架、GVE通用视频嵌入模型 |
| Ch.4 | ECCV2026 | MG-LVR基准、VEterfall时空采样方法 |
| Ch.5 | WebConf2026 | MUIRML度量学习、HiPANNS并行图检索 |

会议论文项目位于上级目录的 `Paper-LaTeX-Projects/` 文件夹。

---

## 编译环境

### 要求

- LaTeX发行版：TeX Live 2020+ 或 MacTeX
- 编译器：XeLaTeX 或 LuaLaTeX
- 必要宏包：见 `main.tex` 中的 `\usepackage` 列表

### 文件依赖

```
main.tex
  ├── ustthesis.cls (模板类)
  ├── ustthesis.sty (模板样式)
  ├── chapters/*.tex (章节内容)
  ├── appendices/*.tex (附录)
  └── references/references.bib (参考文献)
```

图片路径配置：
```latex
\graphicspath{{figures/gve/}{figures/mglvr/}{figures/gmpgr/}}
```

---

## 格式约定

- 不修改模板文件 `ustthesis.cls` 和 `ustthesis.sty`。
- Caption 使用模板默认字体大小；当前仅在 `main.tex` 局部补充 caption 下方 10pt 间距。
- 正文浮动体优先使用 `[t]` 放置；附录可按需要使用 `[htbp]` / `[ht]`。
- 宽表优先使用 `tabularx` 或 `tabular*{\linewidth}` 按页宽排版；如需整体缩小仅用 `\footnotesize` / `\scriptsize`。
- 不使用 `resizebox`、`adjustbox`、`wraptable` 缩放表格。

---

## 相关文件

| 文件 | 说明 |
|-----|------|
| [STYLE.md](STYLE.md) | 写作风格指南，编辑任何 `.tex` 文件前必读 |
| [AGENTS.md](AGENTS.md) | AI 助手指令，包含构建命令、项目结构和 LaTeX 约定 |
| [TODO.md](TODO.md) | 待解决问题与潜在风险清单 |
| [../Paper-LaTeX-Projects/](../Paper-LaTeX-Projects/) | 会议论文项目 |
| [../Paper-PDFs/](../Paper-PDFs/) | 会议论文PDF版本 |
| [../Template-of-HKUST-GZ-Thesis/](../Template-of-HKUST-GZ-Thesis/) | 原始论文模板 |

---

## 模板信息

- 模板来源：HKUST(GZ) Thesis Template
- 原作者：[@fan](https://github.com/luckyfan-cs)
- 请遵守学校论文格式要求使用本模板

---

## 常见问题

### 编译失败

1. 检查 LaTeX 发行版是否完整安装
2. 检查字体是否缺失
3. 清理辅助文件后重新编译：`latexmk -c && latexmk -xelatex main.tex`

### 图片找不到

1. 确认图片文件存在于 `figures/` 对应子目录
2. 检查 `\graphicspath` 配置是否正确

### 参考文献未显示

1. 确保运行了 `bibtex main`
2. 检查 `references.bib` 中是否有对应条目
3. 重新编译两次以更新引用

---

## 更新日志

- 2026-06-26: 全面复查，确认 Ch2 清理完毕；更新所有文档文件（README/AGENTS/TODO/STYLE），新增 STYLE.md 和 AGENTS.md 到项目结构
- 2026-06-25: Ch2 内容扩展（5 类 video retrieval domain）、De-AI 润色、em dash/分号替换；创建 STYLE.md 和 AGENTS.md
- 2026-06-25: 全文综合审查（逻辑/格式/内容/排版/代码/伪代码），新增 10+ 项问题到 TODO.md
- 2026-06-25: 全文审查修复 23 项问题（拼写/语法、数据错误、LaTeX 标签、投稿模板残留等）
- 2026-06-22: 同步当前编译状态、模板一致性与表格/caption格式说明
- 2025-06-14: 重新编写README，简化为快速上手指南
