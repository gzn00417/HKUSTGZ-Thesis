# TODO: 论文待解决问题与潜在风险

> **最后更新**: 2026-06-22
> **编译状态**: 成功 (157页, 9.9MB)

---

## 当前状态

- **编译**: 成功（`latexmk -xelatex main.tex` 无未定义引用/引用）
- **PDF**: [main.pdf](main.pdf) (157页)
- **致命错误**: 无
- **模板文件**: `ustthesis.cls` / `ustthesis.sty` 与 `../Template-of-HKUST-GZ-Thesis` 一致
- **图表状态**: 正文浮动体使用页顶放置；Chapter 3 表格使用 `tabular*`/`tabularx` 按页宽排版

---

## 待处理问题（按优先级）

### 高优先级

| 问题 | 文件 | 说明 / 建议方案 |
|-----|------|----------------|
| 委员会信息未填写 | `main.tex` | `\member{Prof. XXX, Committee Member}` 被注释，需填写实际委员会成员 |
| 缺少中文摘要 | `chapters/00-abstract.tex` / 模板 | HKUST(GZ) 博士论文通常要求中英文摘要；当前仅含英文摘要，需确认研究生院要求并补充 |
| 封面元数据确认 | `main.tex` | 答辩日期 `2026/7/29`、系主任 `Prof. Xiaowen Chu`、导师姓名等需最终确认 |
| 模板官方认可 | - | 建议联系研究生院确认当前 `ustthesis` 模板版本是否被正式接受 |

### 中优先级

| 问题 | 文件 | 说明 / 影响 |
|-----|------|------------|
| 第三章内容校对 | `chapters/03-universal-video-retrieval.tex` | 发现多处笔误/语法：`parital information` → `partial information`（Definition 3.1）、`an strategy` → `a strategy`（Methodology 与 Ablation 小节）、`a MLLM-based` → `an MLLM-based`（Figure 3.4 caption） |
| 第五章公式检查 | `chapters/05-scale-efficient-retrieval.tex` | Self Covariant Loss 公式分母使用 `VAR(·)·VAR(·)`，通常协方差公式分母为标准差乘积；需确认是否为有意设计 |
| 章节末尾多余换页 | `chapters/03-universal-video-retrieval.tex`, `04-spatiotemporal-scaling.tex`, `05-scale-efficient-retrieval.tex` | 各章末尾残留 `\newpage`（来自原投稿模板），可能造成不必要的空白页，建议移除 |
| 未引用参考文献 | `references/references.bib` | `babenko2016efficient`、`lang2021architecture`、`wang2017irgan` 三篇未被正文引用，建议删除 |
| 参考文献字段补全 | `references/references.bib` | 109 条中：41 条 inproceedings/article 缺 `pages`；38 条 inproceedings 缺 `publisher`/`organization`；107 条缺 `DOI`；建议从出版源补全 |
| 出版物状态更新 | `chapters/07-publications.tex` | 第 1、2 篇标注为 Submitted to MM'26 / ECCV 2026，第 3 篇为 WWW'26 已发表；需根据实际审稿状态更新 |
| 致谢内容 | `chapters/00-acknowledgments.tex` | 当前为通用模板式内容，建议根据个人经历补充具体合作者、项目基金等信息 |

### 低优先级（可忽略）

- **字体小型大写警告**: Times New Roman 无 `sc`/`scit` 字形，模板中的小型大写命令会回退；可接受。
- **Overfull/Underfull hbox**: 主要来自表格列宽、目录编号和长串 URL；已通过 `\emergencystretch=2em` 缓解。
- **PDF 版本兼容警告**: 插入的 PDF 图为 1.7 版，输出设置为 1.5；不影响显示，可考虑升级输出 PDF 版本。
- **未使用图片资源**: `figures/gve/uvrb_radar_tasks.pdf` 等未在正文中引用，不影响编译。
- **引用命令混用**: 第二章使用 `\citep`，第三~五章使用 `\cite`，风格可统一但非必要。

---

## 已修复问题

| 问题 | 状态 | 备注 |
|-----|------|------|
| `tabularx` 包缺失导致编译失败 | 已修复 | 在 `main.tex` 中添加 `\usepackage{tabularx}`；此前第三章表格因环境未定义而中断，导致 127 个引用 + 252 个引用未定义 |
| 编译状态更新 | 已验证 | 清理后完整编译成功，157 页，无未定义引用/引用 |
| 参考文献重复 key | 已修复 | `li2026qwen3` / `qwen3vlembedding` 已统一为 `qwen3vlembedding` |
| `qwen3vlembedding` 缺失 arXiv ID | 已修复 | 已补充为 `arXiv:2601.04720` |
| 参考文献冗余条目 | 已修复 | 5 个未引用 key 已删除 |
| 三个未使用的影子 bib 文件 | 已修复 | `gve.bib` 等已删除，仅保留 `references.bib` |
| microtype 与 XeTeX 兼容性 | 已修复 | 已注释 |
| 致谢摘要格式 | 已修复 | 已修复 |
| 日期格式错误 | 已修复 | 已修复 |
| Unicode 箭头符号（正文） | 已修复 | 已添加 `\arrow` 命令 |
| Caption 全局覆盖 | 已修复 | 已移除 `\captionsetup`，保持模板默认字体 |
| Caption 上下间距 | 已修复 | 在 `main.tex` 局部镜像模板逻辑，补充 caption 下方 10pt |
| 第三章 Table 3.1--3.3 重叠/过宽 | 已修复 | 已参考 MM2026 原稿列分组，用 `tabular*`/`tabularx` 按页宽排版 |
| 条目标题可疑空格 | 已修复 | `InternVideo2.5` / `Qwen2.5-VL` 已修正 |
| BibTeX 作者格式错误 | 已修复 | `xu2025carebench` / `wang2023internvid` 作者分隔符从逗号改为 `and` |

---

## 编译命令

```bash
# 进入论文目录
cd HKUSTGZ-Thesis

# 完整编译（推荐）
latexmk -xelatex -f main.tex

# 清理辅助文件
latexmk -C
```

---

## 文件结构

```
HKUSTGZ-Thesis/
├── main.tex                 # 主编译文件
├── main.pdf                 # 编译输出
├── chapters/                # 论文章节
├── appendices/              # 附录
├── figures/                 # 图片资源
├── references/              # 参考文献
├── ustthesis.cls            # 论文模板类文件
├── ustthesis.sty            # 模板样式文件
├── README.md                # 项目说明
└── TODO.md                  # 本文件
```

---

## 论文章节与内容映射

| 章节 | 文件 | 内容概要 |
|-----|------|---------|
| 摘要 | `chapters/00-abstract.tex` | 英文摘要；需确认是否补充中文摘要 |
| 致谢 | `chapters/00-acknowledgments.tex` | 通用致谢，建议个性化 |
| 第 1 章 | `chapters/01-introduction.tex` | 研究背景、语义/观察/搜索三维度、论文组织 |
| 第 2 章 | `chapters/02-related-work.tex` | 视频检索、多任务检索、长视频采样、ANN/图检索、工业系统 |
| 第 3 章 | `chapters/03-universal-video-retrieval.tex` | UVRB、V-SynFlow、Modality Pyramid、GVE |
| 第 4 章 | `chapters/04-spatiotemporal-scaling.tex` | MG-LVR、时空缩放规律、VEterfall |
| 第 5 章 | `chapters/05-scale-efficient-retrieval.tex` | GMP-GR、MUIRML、HiPANNS、百度在线部署 |
| 第 6 章 | `chapters/06-conclusion.tex` | 贡献总结与未来方向 |
| 第 7 章 | `chapters/07-publications.tex` | 三篇相关论文列表 |
| 附录 A | `appendices/A-universal-video-retrieval.tex` | GVE 实验细节、prompt、训练参数 |
| 附录 B | `appendices/B-spatiotemporal-scaling.tex` | MG-LVR 错误分析、补充表格、prompt |
| 附录 C | `appendices/C-scale-efficient-retrieval.tex` | HiPANNS 伪代码、实现细节、额外实验 |

---

## 更新日志

| 日期 | 更新内容 |
|-----|---------|
| 2026-06-22 | 修复 BibTeX 作者格式错误：`xu2025carebench` / `wang2023internvid` 作者分隔符改为 `and` |
| 2026-06-22 | 发现并修复 `tabularx` 包缺失导致的编译错误；验证完整编译成功（157页） |
| 2026-06-22 | 重新梳理 TODO.md，按论文内容分类高/中/低优先级问题 |
| 2026-06-22 | 统计参考文献字段缺失情况：41 缺 pages，38 缺 publisher/organization，107 缺 DOI；发现 3 条未引用条目 |
| 2026-06-22 | 修复条目标题可疑空格：`InternVideo2.5` / `Qwen2.5-VL` |
| 2026-06-22 | 统一 `booktitle` 会议名称格式：CVPR/ICCV/ECCV/ICML/ICLR/KDD/SIGIR/WWW 等 |
| 2026-06-22 | 更新第三章 Table 3.1--3.3 为页宽 `tabular*` 排版，解决表格重叠/挤压 |
| 2026-06-22 | 确认 caption 字体与模板一致，保留模板 caption 样式 |
| 2026-06-21 | 统一参考文献格式：保护缩写、规范 arXiv 字段、统一期刊名大小写 |
| 2026-06-21 | 添加参考文献待补全/确认事项到 TODO |
| 2025-06-21 | 清理模板示例文件和编译辅助文件 |
| 2025-06-21 | 简化 TODO.md，保留关键信息 |
| 2025-06-14 | 修复编译问题，生成 PDF |
