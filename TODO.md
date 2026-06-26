# TODO: 论文待解决问题与潜在风险

> **最后更新**: 2026-06-26
> **编译状态**: 待验证 (需本地编译环境)
> **审查范围**: 全文综合审查（逻辑、格式、内容、排版、代码、伪代码）

---

## 当前状态

- **编译**: 待验证（本地无 LaTeX 环境，需手动运行 `latexmk -xelatex main.tex`）
- **PDF**: [main.pdf](main.pdf) (上次编译: 157页)
- **致命错误**: 无
- **Ch2 状态**: 已清理完毕（无残留 em dash、分号、不必要 `\textbf{}`、AI 特征词）
- **Ch3/Ch4/Ch5 编辑限制**: 这三章源自已发表/投稿的会议论文，**禁止修改内容**，仅允许修复格式、事实性错误、语法错误（详见 `STYLE.md` 和 `AGENTS.md`）
- **模板文件**: `ustthesis.cls` / `ustthesis.sty` 与 `../Template-of-HKUST-GZ-Thesis` 一致
- **图表状态**: 正文浮动体使用页顶放置；Chapter 3 表格使用 `tabular*`/`tabularx` 按页宽排版
- **写作规范**: 已建立 `STYLE.md`（写作风格指南）和 `AGENTS.md`（AI 助手指令）

---

## 待处理问题（按优先级）

### 高优先级

| 问题 | 文件 | 说明 / 建议方案 |
|-----|------|----------------|
| 委员会信息未填写 | `main.tex` | `\member{Prof. XXX, Committee Member}` 被注释，需填写实际委员会成员 |
| 缺少中文摘要 | `chapters/00-abstract.tex` / 模板 | HKUST(GZ) 博士论文通常要求中英文摘要；当前仅含英文摘要，需确认研究生院要求并补充 |
| 封面元数据确认 | `main.tex` | 答辩日期 `2026/7/29`、系主任 `Prof. Xiaowen Chu`、导师姓名等需最终确认 |
| 模板官方认可 | - | 建议联系研究生院确认当前 `ustthesis` 模板版本是否被正式接受 |
| **Ch6 em dash** | `chapters/06-conclusion.tex` | L7、L15 各一处 em dash (`---`)，需替换为逗号、括号或从句 |
| **Ch4 "Importantly," 过渡词** | `chapters/04-spatiotemporal-scaling.tex` | L21 `Importantly, the benchmark allows...`，需移除过渡词并自然衔接 |
| **Ch5 吞吐量数据矛盾** | `chapters/05-scale-efficient-retrieval.tex` | Abstract/Conclusion 写 "one hundred million requests per second"（≈86亿/天），但 Ch5 L52/L491 写 "one hundred billion requests per day"（≈116万/秒），两者相差约 86 倍，需核实原始数据 |
| **Ch5 Related Works 位置不当** | `chapters/05-scale-efficient-retrieval.tex` | Related Works (L436-462) 放在 Experiments 和 Conclusion **之后**，应移至 Methodology 之前或至少 Experiments 之前 |
| **Ch5 Label 拼写错误** | `chapters/05-scale-efficient-retrieval.tex` + `appendices/C-scale-efficient-retrieval.tex` | `effciency` 缺字母 `i`，共 4 处：`gmpgr:fig:effciency_video`、`gmpgr:fig:effciency_explore`、`gmpgr:fig:effciency_mvideo`、`gmpgr:fig:fig:effciency_fresh`（最后一个还有双重 `fig:` 前缀）|
| **Ch3 `\captionof` 在 `figure` 环境内** | `chapters/03-universal-video-retrieval.tex` | L91、L98 在 `figure` 环境的 `minipage` 内使用 `\captionof{figure}`，应改为 `\caption`（当前会跳过 figure 计数器，导致编号异常）|
| **Ch4 重复 label** | `chapters/04-spatiotemporal-scaling.tex` | L263-264 连续两行 `\label{mglvr:sec:testtime}` 和 `\label{mglvr:sec:test_time}`，后者覆盖前者，导致引用指向错误 |

### 中优先级

| 问题 | 文件 | 说明 / 影响 |
|-----|------|------------|
| **Ch5 Self Covariant Loss 公式** | `chapters/05-scale-efficient-retrieval.tex` | 公式中 `VAR(x) = \sqrt{\sum(x-\bar{x})^2}` 实际计算的是未归一化的标准差（缺少 $\frac{1}{N_l}$ 因子），命名为 `VAR` 容易与方差混淆；需确认是否为有意设计 |
| **Ch5 $\mathcal{F}$ 符号重载** | `chapters/05-scale-efficient-retrieval.tex` | 公式(1)中 $\mathcal{F}$ 是检索函数，公式(7)中 $\mathcal{F}_t$ 是训练优化函数，同一章内符号含义不同 |
| **Ch3/Ch4/Ch5 Related Works 重复** | 各章 | 各章保留独立的 Related Works section，与 Ch2 (Background and Literature Review) 存在大量内容重叠（如 HNSW、CLIP-based/MLLM-based models、工业检索系统等） |
| **Ch3/Ch4/Ch5 Conclusion 重复** | 各章 | 各章保留独立的 Conclusion section，与 Ch6 (Conclusions and Future Works) 存在重复 |
| 未引用参考文献 | `references/references.bib` | `babenko2016efficient`、`lang2021architecture`、`wang2017irgan` 三篇未被正文引用，建议删除 |
| 参考文献字段补全 | `references/references.bib` | 109 条中：41 条 inproceedings/article 缺 `pages`；38 条 inproceedings 缺 `publisher`/`organization`；107 条缺 `DOI`；建议从出版源补全 |
| 出版物状态更新 | `chapters/07-publications.tex` | 第 1、2 篇标注为 Submitted to MM'26 / ECCV 2026，第 3 篇为 WWW'26 已发表；需根据实际审稿状态更新 |
| 致谢内容 | `chapters/00-acknowledgments.tex` | 当前为通用模板式内容，建议根据个人经历补充具体合作者、项目基金等信息 |
| **Ch5 注释残留代码** | `chapters/05-scale-efficient-retrieval.tex` | L68、L99、L109、L248、L264、L290-295、L443、L459 共 8 处论文投稿注释行未清理，建议删除或转为正式内容 |
| **Ch5 伪代码集合运算符错误** | `appendices/C-scale-efficient-retrieval.tex` | L48 `B_U = B_U ∩ B_i` 使用交集符号 ∩ 表示拼接，语义错误；应为 `B_U = B_U ∪ B_i` 或改为文字描述 |
| **Q-HiPANNS 返回值模糊** | `appendices/C-scale-efficient-retrieval.tex` | L58 `Return δ_{B_i}` 返回的是函数参数 `B_i` 而非累积结果，语义不清 |
| **Ch5 语法错误** | `chapters/05-scale-efficient-retrieval.tex` | L307 `supervised by single` → `supervised by a single`；L325 `consistently outperformed`（过去时）与上下文现在时不统一 |

### 低优先级（可忽略）

- **字体小型大写警告**: Times New Roman 无 `sc`/`scit` 字形，模板中的小型大写命令会回退；可接受。
- **Overfull/Underfull hbox**: 主要来自表格列宽、目录编号和长串 URL；已通过 `\emergencystretch=2em` 缓解。
- **PDF 版本兼容警告**: 插入的 PDF 图为 1.7 版，输出设置为 1.5；不影响显示，可考虑升级输出 PDF 版本。
- **未使用图片资源**: `figures/gve/uvrb_radar_tasks.pdf` 等未在正文中引用，不影响编译。
- **引用命令混用**: 第二章使用 `\citep`，第三~五章使用 `\cite`，风格可统一但非必要。
- **Ch5 `\ie` 缺少逗号**: L21、L37、L198、L202、L215、L331、L357、L370 共 8 处 `\ie` 后缺少逗号，应为 `\ie,`。
- **Ch5 Preliminaries 数据描述混淆**: L64 "one hundred billion requests... per day" 描述的是 Baidu 整体框架而非 GMP-GR 本身，与 L52 容易混淆读者。
- **Ch3 Table 3.1 表格分裂**: 用了两个独立 `tabularx` 环境，第二个表格列头不同，可能产生排版间隙。建议合并为单一表格或添加分隔说明。
- **Ch7 em dash (3处)**: `chapters/07-publications.tex` L7、L9、L11 使用 `---` 作为出版物条目分隔符，属于格式惯例，可保留但需确认一致性。
- **Appendix A 缩写词**: `appendices/A-universal-video-retrieval.tex` L399 示例文本中出现 `don't`，属于 prompt 示例内容，可保留。

---

## 已修复问题

### 2026-06-25/26 修复（Ch2 内容扩展与润色）

#### 内容扩展
| 修复内容 | 文件 |
|---------|------|
| 扩展 5 类 video retrieval domain 描述（新增 long-context retrieval） | `chapters/02` |
| 新增总结段落区分五类任务的不同挑战 | `chapters/02` |
| 统一后文引用为五类分类 | `chapters/02` |

#### 格式清理
| 修复内容 | 文件 |
|---------|------|
| 移除约 8 处不必要的 `\textbf{}` | `chapters/02` |
| 替换所有 6 处 em dash（改为逗号、括号或从句） | `chapters/02` |
| 替换 1 处分号（改为句号拆分两句） | `chapters/02` |

#### De-AI 润色
| 修复内容 | 文件 |
|---------|------|
| 3 处 `leverage` → `use`/`based on`/`used`（保留 1 处维持多样性） | `chapters/02` |
| 移除 1 处 `Importantly,` 过渡词 | `chapters/02` |

#### 文档建设
| 修复内容 | 文件 |
|---------|------|
| 创建写作风格指南 | `STYLE.md` |
| 创建 AI 助手指令 | `AGENTS.md` |
| 删除旧 `WRITING_PREFERENCES.md`，更新引用 | `AGENTS.md` |

### 2026-06-25 修复（全文审查）

#### 拼写/语法错误
| 问题 | 文件 | 修复内容 |
|-----|------|----------|
| `parital` | `chapters/03` | → `partial` |
| `an strategy` | `chapters/03` | → `a strategy` |
| `a MLLM-based` | `chapters/03` | → `an MLLM-based` |
| `cost-effectively` | `chapters/05` | → `cost-effective` |
| `nuance user preference` | `chapters/05` | → `nuanced user preferences` |
| `to weighted aggregate` | `chapters/05` | → `to aggregate with weighted` |
| `defeats all baseline methods` | `chapters/05` | → `consistently outperforms all baseline methods` |
| `i.e,` | `appendices/A` | → `i.e.,` |
| `splited` | `appendices/C` | → `split` |

#### 明显数据/代码错误
| 问题 | 文件 | 修复内容 |
|-----|------|----------|
| Table 格式不一致 | `chapters/05` | `1.19\%` → `+1.19\%`（与同行 `+1.13\%` 统一） |
| 伪代码变量名错误 | `appendices/C` | `$N'_U = B_i - \epsilon$` → `$N'_U = N_{B_i} - \epsilon$` |
| 视频分类结果矛盾 | `appendices/A` | 原文称 LanguageBind 0.553 最高，但表中无此模型；修正为与表格一致的 GVE-7B/InternVideo2-6B 0.526 |

#### LaTeX 代码/标签适配
| 问题 | 文件 | 修复内容 |
|-----|------|----------|
| 图片路径硬编码 | `chapters/03` | `figures/gve/uvr.pdf` → `uvr.pdf`，label `gve:fig:uvr` → `fig:uvr` |
| 缺少 section labels | `chapters/04` | 为 §Test-Time Scaling、§Training-Time Scaling、§VEterfall 添加 `\label{}` 供附录引用 |
| 附录硬编码引用 | `appendices/B` | `\S3.2`/`\S4.2`/`\S4.3-4.4` → `\S\ref{...}`；`Figure~2`/`Table~1`/`Table~2` → `\ref{...}` |
| "main paper" 措辞 | `appendices/A/B` | 全部 `main paper` → `main chapter`（共 8 处） |

#### 投稿模板残留清理
| 问题 | 文件 | 修复内容 |
|-----|------|----------|
| 末尾 `\newpage`/`\clearpage` | `chapters/03/04/05` | 移除投稿模板残留的分页命令和注释块 |
| 多余连续空行 | `chapters/03/04/05` | 清理 excessive 连续空行（共删除 134 行空白） |

#### 参考文献
| 问题 | 文件 | 修复内容 |
|-----|------|----------|
| `qwen3vlembedding` 格式 | `references.bib` | `journal` 字段从 `arXiv preprint arXiv:2601.04720` 修正为标准格式 |

### 2026-06-22 修复

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
├── STYLE.md                 # 写作风格指南（编辑 .tex 前必读）
├── AGENTS.md                # AI 助手指令
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
| 2026-06-26 | 全面复查：确认 Ch2 清理完毕（无残留 em dash/分号/不必要 `\textbf{}`）；新增 Ch6 em dash (2处)、Ch4 "Importantly," 过渡词到高优先级；更新 Ch5 `\ie` 缺逗号实例数（1→8处）；新增 Ch7 em dash、Appendix A 缩写到低优先级；更新所有文档文件（README/AGENTS/TODO/STYLE） |
| 2026-06-25 | Ch2 内容扩展（5 类 video retrieval domain）、De-AI 润色、em dash/分号替换；创建 STYLE.md 和 AGENTS.md |
| 2026-06-25 | 全文综合审查（逻辑/格式/内容/排版/代码/伪代码）：新增 Ch5 Related Works 位置不当、Label 拼写错误（4处）、`\captionof` 误用、重复 label、注释残留代码（8处）、伪代码符号错误、语法问题等 10+ 项问题到待处理列表 |
| 2026-06-25 | 全文审查修复：拼写/语法错误 9 处、数据/代码错误 3 处、LaTeX 标签适配 8 处、投稿模板残留清理（删除 134 行空白）、参考文献格式 1 处；新增 Ch5 吞吐量数据矛盾、公式符号重载、章节重复等问题到待处理列表 |
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
