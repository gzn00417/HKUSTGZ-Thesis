# HKUST(GZ) Thesis: Towards Scalable and Generalizable Video Retrieval

> **作者**: 郭茁宁 (Zhuoning Guo)  
> **导师**: Prof. Xiaowen Chu, Prof. Renjing Xu  
> **答辩日期**: 2026年7月29日

## 当前阶段

**论文正文已提交并冻结**，不再修改 chapters 1-7 和 appendices。所有工作集中在 `slides/` 答辩幻灯片。

## 论文概述

本论文将视频检索视为一个沿 retrieval pipeline 的 scaling 问题，从三个递进阶段展开：**Semantic Scaling** (Ch3, GVE 通用视频嵌入) → **Observational Scaling** (Ch4, MG-LVR + VEterfall 时空采样) → **Search Scaling** (Ch5, GMP-GR + HiPANNS 并行图检索)。核心洞察：scalable video retrieval requires structure-aware scaling。

## 项目结构

```
HKUSTGZ-Thesis/
├── main.tex / supplementary.tex     # 论文编译文件（已冻结）
├── chapters/ + appendices/          # 章节内容（已冻结）
├── figures/{gve,mglvr,gmpgr}/       # 论文图片
├── references/references.bib        # 参考文献
├── AGENTS.md / STYLE.md / TODO.md   # 项目文档
└── slides/                          # 答辩幻灯片（当前活跃）
    ├── thesis-slides-v0.1~v0.5.pptx # v0.5 为当前最新审阅版
    ├── build.py                     # 设计系统参考库
    ├── v0.5-build/                  # v0.5 重建入口与内部阶段
    ├── v0.5-final-changelog.md      # v0.5 合并修改与 QA 记录
    ├── figures/                     # 42 张 PNG
    └── README.md                    # 幻灯片维护规则
```

## 编译

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error supplementary.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex   # 交叉引用
```

## 论文与会议论文

| 章节 | 会议 | 核心贡献 |
|-----|------|---------|
| Ch3 | MM 2026 | UVR 框架、GVE 模型 |
| Ch4 | ECCV 2026 | MG-LVR 基准、VEterfall |
| Ch5 | WebConf 2026 | MUIRML 度量、HiPANNS |

## 相关文件

| 文件 | 说明 |
|-----|------|
| [AGENTS.md](AGENTS.md) | AI 助手指令，当前阶段与维护规则 |
| [STYLE.md](STYLE.md) | 写作风格指南（参考，已冻结） |
| [TODO.md](TODO.md) | 答辩准备清单 |
| [slides/README.md](slides/README.md) | 幻灯片维护规则与设计策略 |
