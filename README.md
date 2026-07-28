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
    ├── thesis-slides-v0.1~v0.5.pptx # 保留的早期历史版本
    ├── thesis-slides-v0.6.pptx      # 原 v0.66，79 页稳定基线
    ├── thesis-slides-v0.7.pptx      # 原 v0.69，69 页压缩基线
    ├── thesis-slides-v0.8.pptx      # 审阅前的 69 页里程碑
    ├── thesis-slides-v0.9.pptx      # 当前正式的 69 页答辩版本
    ├── build.mjs                    # 从 V0.9 非覆盖派生新版本
    ├── v0.9-build/                  # V0.9 合并记录、审阅证据与最终精修脚本
    ├── build.py                     # 保留的 v0.4 历史设计系统
    ├── v0.5-build/                  # 从 v0.4 重建 v0.5 的历史构建链
    ├── v0.5-final-changelog.md      # v0.5 完整修改与 QA 记录
    ├── SLIDES-GUIDE.md              # 内容、审美、QA 与迭代权威指南
    ├── TODO-v0.6.md                 # 保留的原始用户修改意见
    ├── figures/                     # 幻灯片使用的 PNG
    └── README.md                    # 精简版本索引与维护入口
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
| [slides/README.md](slides/README.md) | 幻灯片版本索引与维护入口 |
| [slides/SLIDES-GUIDE.md](slides/SLIDES-GUIDE.md) | 幻灯片内容、审美、QA 与长期迭代规则 |
