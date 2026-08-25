# HKUST(GZ) Thesis: Towards Scalable and Generalizable Video Retrieval

> **作者**: 郭茁宁 (Zhuoning Guo)  
> **导师**: Prof. Xiaowen Chu, Prof. Renjing Xu  
> **答辩日期**: 2026年7月29日

## 当前阶段

**论文已定稿提交，答辩已于 2026年7月29日完成。开发与写作全部结束。** `main.pdf` 为最终提交文件。`slides/` 保留全部答辩幻灯片历史版本，`appendices/` 保留迁移来源不参与构建。编译中间文件与 `supplementary` 空壳已清理，目录保持精简。

## 论文概述

本论文将视频检索视为一个沿 retrieval pipeline 的 scaling 问题，从三个递进阶段展开：**Semantic Scaling** (Ch3, GVE 通用视频嵌入) → **Observational Scaling** (Ch4, MG-LVR + VEterfall 时空采样) → **Search Scaling** (Ch5, GMP-GR + HiPANNS 并行图检索)。核心洞察：scalable video retrieval requires structure-aware scaling。

## 项目结构

```
HKUSTGZ-Thesis/
├── main.tex                         # 自包含的最终定稿论文
├── chapters/                        # 论文正文（含原附录核心材料）
├── appendices/                      # 保留的迁移来源，不参与当前构建
├── figures/{gve,mglvr,gmpgr}/       # 论文图片
├── references/references.bib        # 参考文献
├── AGENTS.md / STYLE.md / TODO.md   # 项目文档
└── slides/                          # 答辩幻灯片（归档）
    ├── thesis-slides-v*.pptx        # 全部历史版本（V0.1–V3）
    ├── NOTE-V3.md                   # 最终讲稿
    ├── figures/                     # 幻灯片使用的 PNG
    └── README.md                    # 版本索引
```

## 编译

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

`main.pdf` 是完整、自包含的正式提交文件，当前为 A4、135 页。原附录 A--C 的实质内容已整合至第 3--5 章，历史迁移源保留在 `appendices/`，但不参与当前构建。

2026-08-18 的终稿检查覆盖全部 135 页、编译日志、引用占位符、链接注释和页面边界。未发现引用失败、缺页、异常空白、内容裁切、重叠、乱码或其他影响提交的严重格式问题。少量编译排版提示经视觉复核后确认不影响成品。

## 论文与会议论文

| 章节 | 会议 | 核心贡献 |
|-----|------|---------|
| Ch3 | MM 2026（已接收） | UVR 框架、GVE 模型 |
| Ch4 | AAAI 2027（已投稿） | MG-LVR 基准、VEterfall |
| Ch5 | WebConf 2026 | MUIRML 度量、HiPANNS |

## 相关文件

| 文件 | 说明 |
|-----|------|
| [AGENTS.md](AGENTS.md) | AI 助手指令与项目结构 |
| [STYLE.md](STYLE.md) | 写作风格指南（归档参考） |
| [TODO.md](TODO.md) | 项目完成状态与已知保留项 |
| [slides/README.md](slides/README.md) | 幻灯片版本索引 |
