# TODO: 论文待解决问题与潜在风险

> **最后更新**: 2026-06-28
> **编译状态**: 已验证 (TeX Live 2026, XeLaTeX)
> **审查范围**: 全文综合审查（逻辑、格式、内容、排版、代码、伪代码、跨章一致性）

---

## 当前状态

- **编译**: 已验证 (`latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` + `supplementary.tex`)
- **PDF**: [main.pdf](main.pdf) (117页) + [supplementary.pdf](supplementary.pdf) (51页), 2026-06-28 编译
- **交叉引用**: 已通过 `xr-hyper` 双向验证（main 引用 appendix labels，supplementary 引用 chapter labels），零未解析引用
- **致命错误**: 无
- **未定义引用/引用**: 无
- **Introduction**: 已完整重写（7段 + Organization），叙事围绕 semantic/observational/search scaling 展开；已完成 overclaim 风险降低（移除绝对化表述，所有 thesis-level claim 加 scope qualifier）；已插入论文框架图 `figures/thesis-framework.pdf`（Figure 1.1），第六段扩展为详细方法描述并与图中三列结构对齐
- **Abstract**: 已修改，与 intro 的 scaling 叙事对齐；使用 scoped proposition 替代 slogan
- **Conclusion**: 已重写，Future Directions 替换为四个前沿方向（Retrieval-Native Foundation Models / Agentic Visual Memory / Self-Evolving Data / Continuous Generative Representations），篇幅压缩约 50%
- **Ch2 状态**: 已清理完毕（无残留 em dash、分号、不必要 `\textbf{}`、AI 特征词）
- **跨章一致性**: 已验证（2026-06-28），无实质性矛盾，发现 3 处轻微不对称（见高优先级）
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
| **Ch2 taxonomy 与 Ch3 UVR 定义不对齐** | `chapters/02` + `chapters/03` | Ch2 §1.1 列出 5 个 semantic domain（含 long-video），但 Ch3 Definition 1 只列 4 个（不含 long-video）。读者可能质疑为何 "universal" evaluation 未覆盖 long-video。建议在 Ch2 §1.1 或 Ch3 Preliminary 中加一句说明 |
| **Ch2 与 Ch4 措辞重复** | `chapters/02` + `chapters/04` | ~~Ch2 L93 与 Ch4 L19 措辞几乎完全重复~~ **已修复**：Ch2 已改写为 "No existing evaluation setting provides the combination of..."，与 Ch4 原文区分 |
| **Ch2 对三章贡献预览详细度不对称** | `chapters/02` | Ch2 §2.2 明确提到 VEterfall 的名字和技术描述，但 Ch2 §2.3 未提及 GMP-GR、HiPANNS、MUIRML 的名字。建议 Ch2 §2.3 也提及 GMP-GR 和 HiPANNS 以保持一致 |
| **Ch6 em dash** | `chapters/06-conclusion.tex` | ~~L7、L15 各一处 em dash (`---`)~~ **已修复**（2026-06-28）：替换为逗号和从句 |
| **Ch4 "Importantly," 过渡词** | `chapters/04-spatiotemporal-scaling.tex` | L21 `Importantly, the benchmark allows...`，需移除过渡词并自然衔接 |
| **Ch5 吞吐量数据矛盾** | `chapters/05-scale-efficient-retrieval.tex` + `chapters/06-conclusion.tex` | ~~Abstract/Conclusion 写 "one hundred million requests per second"（≈86亿/天），但 Ch5 L52/L491 写 "one hundred billion requests per day"（≈116万/秒），两者相差约 86 倍~~ **已修复**（2026-06-28）：Ch6 改为 "validated under production-scale serving traffic"，避免混用不同层面的数字 |
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

### 2026-06-28 修复（第五轮：Introduction 框架图插入 + 第六段扩展）

#### 框架图插入与第六段扩展
| 修复内容 | 文件 |
|---------|------|
| 插入论文框架图 `figures/thesis-framework.pdf` 为 Figure 1.1，放置于第二段与第三段之间（`[t]` 放置） | `chapters/01-introduction.tex` |
| 第六段（"To address these three challenges..."）扩展：为三项研究各增加方法细节描述，与框架图三列结构对齐 | `chapters/01-introduction.tex` |
| 第六段新增 `Figure~\ref{fig:thesis-framework}` 引用 | `chapters/01-introduction.tex` |
| 上下文一致性验证：Intro P6 方法描述与 Abstract、Conclusion、框架图内容完全对齐 | 全文 |

### 2026-06-28 修复（第四轮：Future Directions 重写 + 全文审查）

#### Future Directions 重写
| 修复内容 | 文件 |
|---------|------|
| Future Directions 完全重写：从 4 个增量扩展方向替换为 4 个前沿方向（Retrieval-Native Foundation Models / Agentic Visual Memory / Self-Evolving Data / Continuous Generative Representations） | `chapters/06-conclusion.tex` |
| Future Directions 篇幅压缩约 50%（4 subsection 各 1 段 + closing paragraph） | `chapters/06-conclusion.tex` |
| Conclusions 段落精简：删除冗余组织概述段落 | `chapters/06-conclusion.tex` |

#### 格式与元数据修复
| 修复内容 | 文件 |
|---------|------|
| `\subject{Doctor of Philosophy in Artificial Intelligence}` → `\subject{Artificial Intelligence}`（修复封面 degree 重复） | `main.tex` |
| "time of page" → "time on page" | `chapters/06-conclusion.tex` |
| "Conclusions and Future Directions" → "Conclusion and Future Directions" | `chapters/06-conclusion.tex` |
| Ch6 em dash `---` → ", where" | `chapters/06-conclusion.tex` |
| Ch6 吞吐量数据 "throughput exceeding one hundred million requests per second" → "validated under production-scale serving traffic" | `chapters/06-conclusion.tex` |
| STYLE.md "Avoidoidance" → "Avoidance" | `STYLE.md` |

#### Defensive language 修复
| 修复内容 | 文件 |
|---------|------|
| Intro P7 "form a coherent trajectory" → "address successive bottlenecks" | `chapters/01-introduction.tex` |
| Ch6 "each depends on the conclusions of the preceding one" → "each addresses the scaling bottleneck at its respective stage" | `chapters/06-conclusion.tex` |
| Ch6 "form a coherent methodology that extends from..." → "address successive stages of the retrieval pipeline" | `chapters/06-conclusion.tex` |

#### Overclaim 修复
| 修复内容 | 文件 |
|---------|------|
| Ch2 §2.1.4 "is fundamentally a video retrieval problem" → "instantiates the same infrastructure problem faced by deployment-scale video retrieval" | `chapters/02-related-work.tex` |

#### 分号修复
| 修复内容 | 文件 |
|---------|------|
| Ch6 Conclusions 段落中 2 处分号拆分为独立句子 | `chapters/06-conclusion.tex` |

### 2026-06-27 修复（第三轮：Overclaim 风险降低）

#### 移除绝对化表述与 slogan
| 修复内容 | 文件 |
|---------|------|
| 移除 "naive scaling does not produce generalization" 金句，替换为 scoped proposition："Across the three stages studied in this thesis, the results show that scaling model capacity, observation density, or metric accuracy alone is insufficient for broader retrieval generalization unless it is aligned with the structure of the corresponding bottleneck" | `chapters/01-introduction.tex` |
| Abstract 同步替换为 scoped proposition + "Scalable video retrieval therefore requires structure-aware scaling" | `chapters/00-abstract.tex` |
| "no amount of representation learning can compensate for" → "cannot be addressed by representation learning alone" | `chapters/01-introduction.tex` |
| "a fundamental asymmetry" → "a consistent asymmetry" | `chapters/01-introduction.tex` |
| "cannot be resolved by optimizing an upstream stage alone" → "is not eliminated by optimizing an upstream stage alone"（Intro P2 + Conclusion 开头段） | `chapters/01-introduction.tex` + `chapters/06-conclusion.tex` |

#### Generalizability claim 操作化
| 修复内容 | 文件 |
|---------|------|
| "Generalizability... is not a separate objective... but the validation" → "generalizability serves as an empirical criterion for assessing whether such scaling has been performed effectively" | `chapters/01-introduction.tex` + `chapters/00-abstract.tex` |
| Conclusion Unified Insights 新增三种 generalization 段落：semantic (query modalities, domains, granularities) / observational (densities, durations, granularities) / deployment (contexts, traffic, serving constraints) | `chapters/06-conclusion.tex` |

### 2026-06-27 修复（第二轮：基于教授反馈的稳定改进）

#### 术语与措辞修正
| 修复内容 | 文件 |
|---------|------|
| "Future Works" → "Future Directions"（章节标题 + section 标题） | `chapters/06-conclusion.tex` |
| "naive scaling" 表述变体：Abstract 改为 "scaling alone is insufficient without structural guidance" | `chapters/00-abstract.tex` |
| "naive scaling" 表述变体：Intro P3 改为 "expanding model parameters and data volume does not by itself yield broader retrieval capability" | `chapters/01-introduction.tex` |
| "naive scaling" 表述变体：Conclusion 改为 "scaling capacity does not automatically translate into retrieval generalization" | `chapters/06-conclusion.tex` |
| Intro P7 保留 "naive scaling does not produce generalization" 作为全文唯一金句（**后续已在 overclaim reduction 中移除**） | `chapters/01-introduction.tex` |

#### 跨章措辞去重
| 修复内容 | 文件 |
|---------|------|
| Intro P4 改写避免与 Ch4 撞句："jointly provides long-form videos and multi-granular query categorization" → "combines long-form visual evidence with queries at multiple granularity levels" | `chapters/01-introduction.tex` |
| Ch2 §2.2 同步改写："No existing benchmark jointly provides..." → "No existing evaluation setting provides the combination of..." | `chapters/02-related-work.tex` |
| Ch2 §2.2 MG-LVR 描述："jointly provides" → "combines... with" | `chapters/02-related-work.tex` |

#### Conclusion 结构加强
| 修复内容 | 文件 |
|---------|------|
| 开头段从 1 段扩展为 2 段：第一段回到 thesis problem（pipeline-level scaling），第二段用 "three studies, each addressing a distinct stage" 过渡到 summaries | `chapters/06-conclusion.tex` |
| Generalization claim 加 scope qualifier："Generalizability, in this thesis, is... the validation" → "Within the scope of this thesis, generalizability serves as an empirical criterion for assessing whether scaling has been performed in a structure-aware manner" | `chapters/06-conclusion.tex` |

### 2026-06-27 修复（Introduction 重写与全文一致性对齐）

#### Introduction 完整重写
| 修复内容 | 文件 |
|---------|------|
| 完整重写 Introduction（7段 + Organization，1482词，34个引用） | `chapters/01-introduction.tex` |
| 建立 semantic/observational/search scaling 三线叙事框架 | `chapters/01-introduction.tex` |
| P1: 问题与背景（video retrieval 定义、演化、scaling 从第一段出现） | `chapters/01-introduction.tex` |
| P2: 三个 research challenges 框架（pipeline 递进 + 独立瓶颈） | `chapters/01-introduction.tex` |
| P3-P5: 三个 scaling gap 的详细论述（对应 Ch3/Ch4/Ch5） | `chapters/01-introduction.tex` |
| P6: 三篇 paper 如何解决这些 challenges | `chapters/01-introduction.tex` |
| P7: 三篇 paper 如何串起 thesis（naive scaling 不产生 generalization） | `chapters/01-introduction.tex` |
| Section 1.2: Organization of the Thesis（逐章一段，精简） | `chapters/01-introduction.tex` |

#### Abstract 与 Conclusion 对齐
| 修复内容 | 文件 |
|---------|------|
| Abstract 第二段改为 "scaling problem along the retrieval pipeline"，引入三个 scaling 术语 | `chapters/00-abstract.tex` |
| Conclusion 开头段和 "Unified Methodology and Insights" 段重写，与 intro 的 scaling 叙事对齐 | `chapters/06-conclusion.tex` |

#### 术语一致性修复
| 修复内容 | 文件 |
|---------|------|
| Ch2 "dimensions" → "scaling challenges"（L75） | `chapters/02-related-work.tex` |
| Ch7 "dimensions" → "scaling challenges"（L4） | `chapters/07-publications.tex` |

#### 技术修复
| 修复内容 | 文件 |
|---------|------|
| `\graphicspath` 语法修复：`{{dir1/},{dir2/}}` → `{{dir1/}{dir2/}}`，消除 VSCode LSP 误报 | `main.tex` |

#### 跨章一致性验证
| 验证内容 | 结果 |
|---------|------|
| 三维度名称（semantic/observational/search）跨全文一致性 | 一致 |
| 数值声明（16 datasets, 1.55M pairs, 9971 queries, 75% gap, 20% improvement, 4-16× efficient, 20+ apps, 100M+ RPS） | 一致 |
| 模型名称（GVE, MG-LVR, VEterfall, GMP-GR, HiPANNS, MUIRML）跨章节引用 | 一致 |
| Pipeline 递进关系（representation → observation → search）跨章节描述 | 一致 |
| 发现 3 处轻微不对称（Ch2 taxonomy vs Ch3, Ch2/Ch4 措辞重复, Ch2 预览详细度不对称） | 已记录到高优先级 |

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

# 完整编译（推荐，需按顺序）
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error supplementary.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex   # 第二轮同步交叉引用

# 清理辅助文件
latexmk -c
```

---

## 文件结构

```
HKUSTGZ-Thesis/
├── main.tex                 # 主论文编译文件（Ch1-6 + Publications + References）
├── main.pdf                 # 主论文输出（117页）
├── supplementary.tex        # 补充材料编译文件（Appendix A-C + References）
├── supplementary.pdf        # 补充材料输出（51页）
├── chapters/                # 论文章节
├── appendices/              # 附录（由 supplementary.tex 加载）
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
| 摘要 | `chapters/00-abstract.tex` | 英文摘要；scaling problem along the retrieval pipeline 叙事；需确认是否补充中文摘要 |
| 致谢 | `chapters/00-acknowledgments.tex` | 通用致谢，建议个性化 |
| 第 1 章 | `chapters/01-introduction.tex` | 研究背景、semantic/observational/search scaling 三维度、三篇 paper 解决方案、论文组织 |
| 第 2 章 | `chapters/02-related-work.tex` | 视频检索概念、embedding models、spatiotemporal sampling、ANNS/图检索、文献综述 |
| 第 3 章 | `chapters/03-universal-video-retrieval.tex` | UVRB、V-SynFlow、Modality Pyramid、GVE |
| 第 4 章 | `chapters/04-spatiotemporal-scaling.tex` | MG-LVR、时空缩放规律、VEterfall |
| 第 5 章 | `chapters/05-scale-efficient-retrieval.tex` | GMP-GR、MUIRML、HiPANNS、百度在线部署 |
| 第 6 章 | `chapters/06-conclusion.tex` | 贡献总结与四个前沿方向（Retrieval-Native Foundation Models / Agentic Visual Memory / Self-Evolving Data / Continuous Generative Representations） |
| 第 7 章 | `chapters/07-publications.tex` | 三篇相关论文列表 |
| 附录 A | `appendices/A-universal-video-retrieval.tex` | GVE 实验细节、prompt、训练参数 |
| 附录 B | `appendices/B-spatiotemporal-scaling.tex` | MG-LVR 错误分析、补充表格、prompt |
| 附录 C | `appendices/C-scale-efficient-retrieval.tex` | HiPANNS 伪代码、实现细节、额外实验 |

---

## 更新日志

| 日期 | 更新内容 |
|-----|---------|
| 2026-06-28 | **Introduction 框架图插入**：在 `01-introduction.tex` 中插入 `figures/thesis-framework.pdf` 为 Figure 1.1（`[t]` 放置于第二段与第三段之间）；扩展第六段为详细方法描述，与框架图三列结构（Semantic Scaling → GVE / Observational Scaling → MG-LVR + VEterfall / Search Scaling → HiPANNS + GPU Execution）对齐；上下文一致性验证通过（Intro P6 vs Abstract vs Conclusion vs Figure）；main.pdf 从 116 页增至 117 页；编译验证无错误 |
| 2026-06-28 | **Supplementary 拆分**：将附录从 main.tex 分离到独立的 supplementary.tex；main 仅保留 Ch1-6 + Publications + References（116页）；supplementary 包含 Appendix A-C + 独立 Bibliography（51页）；通过 `xr-hyper` 实现双向交叉引用（main↔supplementary labels），零未解析引用；supplementary 使用简洁标题页（论文标题 + "Supplementary Material"）；更新 AGENTS.md / TODO.md / README.md |
| 2026-06-28 | 第四轮修改（Future Directions 重写 + 全文审查）：Future Directions 完全重写为 4 个前沿方向并压缩 50%；修复封面 degree 重复、Ch6 em dash、吞吐量数据矛盾、defensive language（3 处）、Ch2 overclaim、Ch6 分号（2 处）；全文 style check（无残留 em dash/分号/AI 词）；编译验证 163 页无错误 |
| 2026-06-27 | 第三轮修改（Overclaim 风险降低）：移除 "naive scaling does not produce generalization" 金句，替换为 scoped proposition；Abstract/Intro/Conclusion 全文统一为 empirical/operational claim；"no amount of" → "alone cannot"；"fundamental" → "consistent"；"cannot be resolved" → "is not eliminated"；Conclusion 新增三种 generalization 段落（semantic/observational/deployment）；编译验证 167 页无错误 |
| 2026-06-27 | 第二轮修改（基于教授反馈）：Future Works → Future Directions；naive scaling 表述变体（保留 Intro P7 金句，Abstract/Intro P3/Conclusion 改写）；消除 Intro P4 和 Ch2 与 Ch4 的措辞重复；Conclusion 开头段加厚（1段→2段）；Generalization claim 加 scope qualifier；编译验证 167 页无错误 |
| 2026-06-27 | Introduction 完整重写（7段 + Organization，1482词，34个引用）；Abstract/Conclusion 与 intro scaling 叙事对齐；Ch2/Ch7 术语一致性修复（dimensions → scaling challenges）；`\graphicspath` 语法修复；全文跨章一致性验证（无实质性矛盾，3 处轻微不对称已记录）；完整编译验证（166页，无错误） |
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
