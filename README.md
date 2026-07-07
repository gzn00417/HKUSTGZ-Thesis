# HKUST(GZ) Thesis: Towards Scalable and Generalizable Video Retrieval

> **作者**: 郭茁宁 (Zhuoning Guo)  
> **学位**: PhD (哲学博士)  
> **专业**: Doctor of Philosophy in Artificial Intelligence  
> **院系**: Thrust of Artificial Intelligence  
> **导师**: Prof. Xiaowen Chu, Prof. Renjing Xu  
> **答辩日期**: 2026年7月29日

---

## 当前状态

- 编译状态：已验证 (TeX Live 2026, XeLaTeX)
- 输出文件：[main.pdf](main.pdf)（119页）+ [supplementary.pdf](supplementary.pdf)（51页），2026-07-01 编译
- 最近审查：2026-07-01 第十轮更新（Ch7 新增合作作者许可邮件截图）+ 完整编译验证
- 最近修复：2026-07-01 Ch7 新增 Co-author Permission 章节，插入 Prof. Hao Liu 邮件许可截图 `figures/endorse-liuhao.png`；完整清理编译验证通过
- 当前阶段：**论文正文已冻结**，不再修改 chapters 1-7 和 appendices。所有后续工作集中在 `slides/` 答辩幻灯片维护
- 写作规范：已建立 [STYLE.md](STYLE.md)（写作风格指南）和 [AGENTS.md](AGENTS.md)（AI 助手指令），供后续编辑参考
- 模板文件：`ustthesis.cls` / `ustthesis.sty` 保持与 `../Template-of-HKUST-GZ-Thesis` 一致
- 格式更新：第三章 Table 3.1--3.3 已按 `\linewidth` 页宽排版；caption 字体保持模板默认大小

## 快速开始

### 1. 编译论文

```bash
# 进入论文目录
cd HKUSTGZ-Thesis

# 使用 latexmk 编译（推荐，需按顺序）
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error supplementary.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex   # 第二轮同步交叉引用

# 或手动编译
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
xelatex supplementary.tex
bibtex supplementary
xelatex supplementary.tex
xelatex main.tex   # 同步 supplementary.aux

# 清理辅助文件
latexmk -c
```

### 2. 查看输出

编译完成后查看 `main.pdf`（主论文）和 `supplementary.pdf`（补充材料）。

### 3. 修改内容

- 章节内容：编辑 `chapters/*.tex`
- 参考文献：编辑 `references/references.bib`
- 图片资源：添加到 `figures/` 对应子目录

---

## 论文概述

本论文将视频检索视为一个沿 retrieval pipeline 的 scaling 问题，从三个递进的阶段展开：

| 研究阶段 | Scaling 挑战 | 核心问题 | 对应章节 |
|---------|-------------|---------|---------|
| **Semantic Scaling** | 表示学习 | 如何学习支持多样化查询的通用检索表示 | Chapter 3 |
| **Observational Scaling** | 视觉观测 | 视频采样密度如何影响不同粒度的检索质量 | Chapter 4 |
| **Search Scaling** | 大规模搜索 | 如何在大规模候选集合中高效执行检索 | Chapter 5 |

核心洞察：Scalable video retrieval requires structure-aware scaling across semantic capability, visual observation, and search execution. 在本文研究的三个阶段中，单独扩大模型容量、观测密度或度量精度均不足以产生更广泛的检索泛化能力。Generalizability 作为 empirical criterion 用于评估 scaling 是否以 structure-aware 的方式完成。

---

## 项目结构

```
HKUSTGZ-Thesis/
├── main.tex                 # 主论文编译文件（Ch1-6 + Publications + References）
├── main.pdf                 # 主论文输出（119页）
├── supplementary.tex        # 补充材料编译文件（Appendix A-C + References）
├── supplementary.pdf        # 补充材料输出（51页）
├── chapters/                # 论文章节
│   ├── 00-abstract.tex      # 摘要
│   ├── 00-acknowledgments.tex       # 致谢（英文，正式）
│   ├── 00-acknowledgments-zh.tex    # 致谢（中文参考稿，不参与编译）
│   ├── 01-introduction.tex  # 引言
│   ├── 02-related-work.tex  # 相关工作
│   ├── 03-universal-video-retrieval.tex  # 第三章
│   ├── 04-spatiotemporal-scaling.tex     # 第四章
│   ├── 05-scale-efficient-retrieval.tex  # 第五章
│   ├── 06-conclusion.tex    # 结论
│   └── 07-publications.tex  # 发表论文
├── appendices/              # 附录（由 supplementary.tex 加载）
├── figures/                 # 图片资源
│   ├── endorse-liuhao.png   # Ch7 合作作者许可邮件截图
│   ├── thesis-framework.pdf # Ch1 论文框架图
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
├── TODO.md                  # 待解决问题清单
└── slides/                  # 答辩幻灯片（v0.1-v0.3）
    ├── README.md            # 幻灯片维护规则与设计策略
    ├── build.py             # 参考实现（从 PNG 生成 deck）
    ├── thesis-slides-v0.1.pptx
    ├── thesis-slides-v0.2.pptx
    ├── thesis-slides-v0.3.pptx
    └── figures/             # build.py 引用的 17 张 PNG
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
  ├── references/references.bib (参考文献)
  └── supplementary.aux (交叉引用 appendix labels，通过 xr-hyper)

supplementary.tex
  ├── ustthesis.cls (模板类)
  ├── ustthesis.sty (模板样式)
  ├── appendices/*.tex (附录内容)
  ├── references/references.bib (参考文献)
  └── main.aux (交叉引用 chapter labels，通过 xr-hyper)
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
| [slides/README.md](slides/README.md) | 答辩幻灯片维护规则与设计策略 |
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

- 2026-07-07: 提交答辩幻灯片 `slides/`（v0.1-v0.3），含 build.py、17 张 PNG 和维护规则；论文正文冻结，后续仅维护 slides
- 2026-07-01: 第十轮更新：Ch7 新增 Co-author Permission 章节，插入 Prof. Hao Liu 邮件许可截图 `figures/endorse-liuhao.png`；完整清理编译验证 main.pdf 119页 + supplementary.pdf 51页，零错误零未解析引用
- 2026-06-30: 第九轮修复：Ch3 V-SynFlow 图补充 `[t]` 放置选项；Acknowledgments 2 处直引号改为 LaTeX 标准引号；Ch5 Related Works 2 处直引号改为 LaTeX 标准引号；完整清理编译验证 main.pdf 118页 + supplementary.pdf 51页，零错误零未解析引用
- 2026-06-29: 第八轮修复：删除 3 条未引用 bib 条目（`babenko2016efficient`/`lang2021architecture`/`wang2017irgan`）；修复 Ch5 中 10 处 `\ie` 缺逗号；完整编译验证 main.pdf 118页 + supplementary.pdf 51页，零错误零未解析引用；更新所有文档文件
- 2026-06-29: 提交前整理：修复6项确定性错误（Ch3 captionof/Ch4重复label/Ch5拼写语法/Appendix C伪代码∩→∪+双重fig前缀/Ch5注释残留），Ch2 taxonomy与Ch3对齐，Ch2 §2.3补充Ch5贡献预览（GMP-GR/MUIRML/HiPANNS），中文致谢加入.gitignore；main.pdf 118页 + supplementary.pdf 47页，0错误0未定义引用；清理中间文件
- 2026-06-29: 致谢完成：重写英文版致谢（个性化感谢三位导师/教授/工业界合作者/论文合作者/同学/家人），创建中文参考稿 `00-acknowledgments-zh.tex`；完整编译验证通过；清理LaTeX中间文件
- 2026-06-28: Introduction 框架图插入：在 `01-introduction.tex` 中插入 `figures/thesis-framework.pdf` 为 Figure 1.1，扩展第六段为详细方法描述并与框架图三列结构对齐；上下文一致性验证通过；main.pdf 从 116 页增至 117 页；编译验证无错误

- 2026-06-28: Future Directions 重写为四个前沿方向（Retrieval-Native Foundation Models / Agentic Visual Memory / Self-Evolving Data / Continuous Generative Representations），篇幅压缩 50%；修复封面 degree 重复、Ch6 em dash、吞吐量数据矛盾、defensive language（3处）、Ch2 overclaim、Ch6 分号（2处）；全文 style check 通过；编译验证 163 页无错误
- 2026-06-27: Overclaim 风险降低：移除 "naive scaling" slogan，替换为 scoped proposition；Conclusion 新增三种 generalization 段落；全文 claim 统一为 empirical/operational 表述；编译验证 167 页无错误
- 2026-06-27: Introduction 完整重写（7段 + Organization，34个引用）；Abstract/Conclusion 与 intro scaling 叙事对齐；全文跨章一致性验证；编译验证 167 页无错误
- 2026-06-26: 全面复查，确认 Ch2 清理完毕；更新所有文档文件（README/AGENTS/TODO/STYLE），新增 STYLE.md 和 AGENTS.md 到项目结构
- 2026-06-25: Ch2 内容扩展（5 类 video retrieval domain）、De-AI 润色、em dash/分号替换；创建 STYLE.md 和 AGENTS.md
- 2026-06-25: 全文综合审查（逻辑/格式/内容/排版/代码/伪代码），新增 10+ 项问题到 TODO.md
- 2026-06-25: 全文审查修复 23 项问题（拼写/语法、数据错误、LaTeX 标签、投稿模板残留等）
- 2026-06-22: 同步当前编译状态、模板一致性与表格/caption格式说明
- 2025-06-14: 重新编写README，简化为快速上手指南
