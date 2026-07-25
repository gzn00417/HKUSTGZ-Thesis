# Defense Slides v0.6 Revision Plan

> 本文档整理了 v0.5 → v0.6 的所有修改建议，按通用问题、逐页建议、整体结构调整三大类组织，确保不遗漏任何原始意见。
>
> 来源：v0.5 用户逐页评审意见 + 论文原文对照 + v0.5-final-changelog 历史经验

---

## 一、通用问题（跨多页适用）

### 1.1 术语与表达问题

| 问题 | 涉及页面 | 修改方向 |
|------|---------|---------|
| "pipeline level" / "pipeline" 术语突兀，听众不知道指什么 | 第3、8、48页 | 用更通俗的表述替代，或首次出现时配以直观解释；考虑用 "retrieval pipeline stages" 等论文中使用的说法 |
| "structure-aware scaling" / "structure where scaling" 表述奇怪，不是标准学术用语 | 第3、48、49页 | 从论文 Introduction 原文中摘取更自然的表述；核心意思是"针对每个阶段的结构特点进行 scaling" |
| "evidence" 用词奇怪，不是本论文的核心概念 | 第37、49页 | 重点应放在 motivation 和方法上，而非 evidence；减少或重新组织该词的使用 |
| "intervene" 不是学术词汇，含义模糊 | 第37页 | 替换为论文中使用的标准术语 |
| "signal" 难以理解 | 第38页 | 明确具体指什么（relevance metric / retrieval score 等） |
| Takeaway 过于口语化，不够学术凝练 | 多页 | 从论文原文/摘要中提炼，确保学术性和准确性 |
| 自创表达（如 "Share the blind spot"、"Structured no random"、"Parameter scaling alone does not remove"）不规范 | 第12页 | **严格从论文原文中摘取句子和表达**，不要自行编造 |
| "diagnostic power" 有 over-claim 嫌疑 | 第11页 | 更克制、具体地说明其作用 |

**核心原则**：文字内容尽量从论文原文（尤其是各章 Introduction、Abstract、Conclusion）中提炼和摘取，保持学术规范，避免自行创造说法。

### 1.2 标题风格问题

- **现状**：几乎每页都用一个"结论式"的标题（类似 takeaway 作为标题）
- **问题**：不符合学术报告常规；听众看到标题时还没有上下文，难以理解
- **建议**：
  - 标题改为类似论文 section 的风格（陈述性/描述性标题）
  - 例如 "CLIP graph" 这样的标题不好，应改为 "Benchmark Construction Pipeline"
  - 核心结论/claim 可以放在副标题（claim line）或 takeaway 栏中

### 1.3 内容组织与逻辑顺序问题

- **Study 1（GVE）内容顺序需要调整**：
  - 当前问题：数据合成（V-SynFlow）放在了实验结果之后，逻辑颠倒
  - 建议顺序：Motivation/Diagnostic → Data Synthesis (V-SynFlow) → Model & Curriculum → Experiments
  - Findings 应该和实验结果放在一起

- **Study 2（MG-LVR）内容顺序**：
  - 补充 Spatial scaling 的内容（当前似乎只有 temporal）
  - 第 36 页内容像附录材料，应前移或移入附录

- **Study 3（GMP-GR）整体失衡**：
  - 实验部分讲得太多
  - 方法部分反而不够具体
  - 概念部分有冗余

### 1.4 公式与排版问题

- 公式没有正确编译（如下划线、符号等）——**必须修复**
- 部分页面公式出现乱码（第 34 页）
- 图的大小需要根据页面重要性调整（重要页面图可以小一点，留出空间给文字说明；纯结果页面图可以放大）

### 1.5 Takeaway 使用规范

- 不是每页都需要 takeaway 栏
- 实验结果页不必每页都有 takeaway，可以在图旁/表旁直接标注
- Takeaway 必须精准、凝练、学术，不能口语化
- 重要的方法页/核心发现页应该有清晰的 takeaway

### 1.6 重点突出原则

- 避免整页都是文字，要让听众一眼能找到重点
- 核心概念、关键数字、主要结论应该在视觉上突出
- 次要信息（如具体比例数字、工程细节）可以简化或放入 speaker notes

---

## 二、逐页修改建议

> 注：页码基于 v0.5 的 56 页主报告。带 * 的为结构性调整建议。

### 第 1 页 — 封面

| 项目 | 内容 |
|------|------|
| **现状问题** | ① 下方名字、学校、导师名字字体太小，看不清楚；② 标题下方的总结句不够精准，没有点出论文核心；③ 用问句形式可能不够直接 |
| **修改建议** | ① 增大底部文字字号；② 重新打磨副标题/总结句，要一针见血地点出论文核心贡献（三个 scaling 问题 + structure-aware 思路）；③ 考虑不用问句，改用陈述性的核心论断 |
| **参考来源** | 论文 Abstract 最后一段、Chapter 1 结论段 |

---

### 第 2 页 — 目录 / Outline

| 项目 | 内容 |
|------|------|
| **现状问题** | 太密集、不够美观 |
| **修改建议** | ① 松散一点，模块化设计（每个 section 一个独立区块）；② 目录中的小字描述需要仔细斟酌，要精准概括每个部分的核心；③ 可以加入章节编号或图标辅助视觉区分 |
| **优先级** | 中 — 属于视觉优化，不影响内容准确性 |

---

### 第 3 页 — Introduction / Motivation

| 项目 | 内容 |
|------|------|
| **现状问题** | ① "Introduction + Motivation" 并列很奇怪，Introduction 本身就包含 motivation；② "pipeline level scaling problem" 术语突兀，听众不知道 "pipeline level" 是什么；③ "Structure aware scaling" 直接抛出来没人懂 |
| **核心问题** | 直接抛出抽象概念，没有从基础、直观的问题入手 |
| **修改建议** | ① 去掉 Motivation 副标题，直接用 Introduction；② 从大家熟悉的 video retrieval 基本概念讲起，逐步引入 scaling challenge；③ 用更自然的语言描述三个层面的挑战（语义层、观测层、搜索层），而不是直接说 "pipeline level"；④ "structure-aware scaling" 这个表述可以后置，先讲清楚问题再引入我们的思路 |
| **参考来源** | 论文 Chapter 1 第 1 节 Background and Motivation，从 "Video retrieval is a central task..." 开始的引入方式 |

---

### 第 4 页 — 应用场景 / Motivation

| 项目 | 内容 |
|------|------|
| **现状问题** | ① "underpins" 用词不直观；② 三个应用部分介绍太简单，不够清晰，可能需要补充图；③ "The shift" 没讲清楚在说什么 |
| **修改建议** | ① 替换更通俗的动词；② 每个应用场景配一张示意图或图标，文字描述更具体一些（是什么场景、为什么需要检索、规模多大）；③ "The shift" 部分重新组织语言，明确说清楚"从什么转向什么、为什么这是一个重要转变" |
| **补充** | 用户提到图会自己补充粘贴，所以重点是文字部分要清晰 |

---

### 第 5 页 — Problem Formulation / Definitions

| 项目 | 内容 |
|------|------|
| **现状问题** | ① 公式排版有问题（如下划线没有编译），必须修正；② 整页字偏多、公式复杂，没有突出重点；③ "Why is hard?" 放的位置奇怪，也不是重点 |
| **修改建议** | ① **修复所有公式排版问题**；② 减少文字量，只保留最核心的 1-2 个定义；③ "Why is hard?" 可以去掉或移到下一页作为 motivation；④ 视觉上突出最关键的定义（如用卡片或高亮框） |
| **优先级** | 高 — 公式错误是硬伤 |

---

### 第 6 页 — Three Scaling Challenges 引入

| 项目 | 内容 |
|------|------|
| **布局问题** | 两边留白太多；建议图放左边，三个 scaling（semantic / observational / search）靠右竖向排列 |
| **内容问题** | ① Takeaway 信息量不足，应该明确说清楚"我们提出了三类 scaling 挑战"以及它们之间的关系；② 逻辑衔接不直观——前面在讲基础概念，这里突然冒出三个 scaling，需要过渡和解释 |
| **修改建议** | ① 调整布局：左图右文，三个 scaling 竖向排列，每个有简短描述；② 增加过渡性文字，说明"沿着检索 pipeline 的信息流向，我们识别出三个层面的 scaling 挑战"；③ Takeaway 要精准概括三个 scaling 的递进关系 |
| **参考来源** | 论文 Chapter 1 第 7 行起 "Building an embedding-based video retrieval system involves three decisions in sequence..." |

---

### 第 7 页 — Three Scaling 框架图

| 项目 | 内容 |
|------|------|
| **现状问题** | 和第 6 页内容有重合，有点散 |
| **修改建议** | 方案 A（合并）：如果内容可以精简，尝试合并到第 6 页一页呈现；方案 B（保留）：两页分工明确——第 6 页引入概念+关系，第 7 页展示框架图细节 |
| **如果保留第 7 页** | 先介绍什么是 semantic scaling，再放出框架图，展示三种 scaling 的关系和先后顺序 |
| **相关** | 与第 6 页一起考虑，作为一组 |

---

### 第 8 页 — Roadmap / Three Studies Overview

| 项目 | 内容 |
|------|------|
| **现状问题** | ① "three study address three pipeline max" 中 pipeline 术语令人困惑；② 只给了一些结果数字，听众不知道在讲什么；③ 缺少 high-level 的方法说明 |
| **修改建议** | ① 替换 "pipeline" 为更易懂的表述；② **每个 study 必须有 high-level 说明**：用什么方法解决了什么问题；③ 搬一些关键结果过来，但要配上下文解释（不要只扔数字）；④ 让听众读完这一页就能大概知道三个研究分别做了什么 |
| **参考来源** | 论文 Chapter 1 第 22 段 "To address these three challenges..." 及三个 study 的一句话总结 |

---

### 第 9 页 — Study 1 开篇（GVE / UVR）

| 项目 | 内容 |
|------|------|
| **论文状态** | 已被 **ACM MM 2026** accept，需要更新页面上的论文信息 |
| **内容问题** | ① "capability" 的 process 描述奇怪，太口语化；② 总结不够好，应该更学术 |
| **修改建议** | ① 更新论文发表信息（ACM MM 2026）；② 从论文 Abstract / CV 描述中摘取更学术、更凝练的表述；③ 作为 Study 1 的第 1 页，要讲清楚：这个 study 解决什么问题、核心思路是什么、主要贡献有哪些 |
| **优先级** | 高 — 论文状态是事实性错误，必须修正 |
| **参考来源** | 论文 Chapter 3 Abstract、MM2026 论文标题和摘要 |

---

### 第 10 页 — Study 1 Motivation / The Trap

| 项目 | 内容 |
|------|------|
| **Query format & domain** | 前面已有介绍，这里可以简单带过或压缩篇幅 |
| **"The Trap" 部分** | 问题：说得好像只针对 MSR-VTT 一个数据集。实际应该讲的是**两个核心问题**：① **领域狭窄**（模型只在一两个领域有效）；② **能力碎片化**（各种能力无法整合到一个模型中）。建议从论文中摘录经典表述 |
| **Take away** | 不够学术，过于口语化，需要精简凝练 |
| **重要性** | 这是 Study 1 的第 1 个内容页，很重要，要打好基础 |
| **参考来源** | 论文 Chapter 3 Introduction 第 20-32 行，关于 fragmented evaluation 和 two critical hurdles 的论述 |

---

### 第 11 页 — Study 1: UVRB / Diagnostic Framework

| 项目 | 内容 |
|------|------|
| **总体评价** | 没什么大问题 |
| **具体修改** | ① "Diagnostic power" 有点 over-claim，改得更克制、更具体（说明它能做什么、提供什么价值）；② 标题有点奇怪，文字再润色一下；③ 避免使用难以理解的词 |
| **建议标题** | 类似 "Unified Evaluation Protocol (UVRB)" 这样的描述性标题 |

---

### 第 12 页 — Study 1: Key Findings 1

| 项目 | 内容 |
|------|------|
| **布局** | 右边内容可以加个底框/卡片，不然和左边混在一起 |
| **文字问题（严重）** | 以下表达都不规范，需要重写：<br>• "Share the blind spot" — 没人知道是什么<br>• "Structured no random" — 不是学术表达，可用 "structured diagnostic targeting"<br>• "Parameter scaling alone does not remove" — 表达奇怪 |
| **修改原则** | **尽量从论文原文中摘句子**，用适合 PPT 的精炼方式总结，**绝对不要自己造说法** |
| **参考来源** | 论文 Chapter 3 Preliminary 部分和实验分析部分的 findings |

---

### 第 13 页 — Study 1: Key Findings 2

| 项目 | 内容 |
|------|------|
| **现状问题** | 和前一页有点脱节；感觉像是 findings，但放的位置和形式都奇怪 |
| **修改建议** | ① 回去对照论文看看 findings 部分是怎么组织的；② 考虑和第 12 页合并，或者和后面的实验结果（第 18 页）放在一起；③ 确保逻辑连贯 |
| **结构调整** | 见下方 "Study 1 整体结构调整建议" |

---

### 第 14 页 — Study 1: V-SynFlow / 数据合成

| 项目 | 内容 |
|------|------|
| **位置问题（严重）** | 数据合成的方法放在了实验后面，**顺序完全不对** |
| **建议的整体顺序** | 1. Motivation & Diagnostic（第 9-13 页）<br>2. **数据合成方法 V-SynFlow**（移到此处）<br>3. 模型架构 & Curriculum Learning<br>4. 实验结果 |
| **内容删减** | 60% / 30% / 10% 的比例数字不重要，**完全可以去掉**。不要把篇幅花在 temporal/spatial 占比这种细节上 |
| **内容重点** | 讲清楚三个步骤（而不是比例）：<br>① **Quality Control** — 过滤掉差数据<br>② **Dimensional Information Enrichment** — 做多维标注，丰富视频信息<br>③ **Multimodal Task Extension / Caption to Query** — 从 caption 生成多样化、高质量的 query；强调 Task Attention（对应前面 motivation 中要做多样任务） |
| **呼应 Motivation** | Task Attention / 多任务多样性要和前面的 motivation 呼应 |
| **参考来源** | 论文 Chapter 3 第 107-119 行，V-SynFlow 三个阶段的描述 |

---

### 第 15 页 — Study 1: UVRD / 数据集统计

| 项目 | 内容 |
|------|------|
| **现状问题** | ① "63 写成 10" 等数字呈现问题；② "Design" 部分奇怪 |
| **修改建议** | ① 老老实实列数据，强调关键数字大小（1.55M pairs 等）；② 加上 human evaluation 结果（95/100）；③ 这一页会快速带过，所以只要重点数字，不要花里胡哨的文字 |
| **核心数字** | 1.55M pairs、多任务覆盖、95% 人工审核准确率 |
| **参考来源** | 论文 Chapter 3 数据集部分和 Table/统计数据 |

---

### 第 16 页 — Study 1: GVE 模型架构

| 项目 | 内容 |
|------|------|
| **现状问题** | ① 内容有点超出必要范围；② 工程细节太多 |
| **修改建议** | ① 工程性的内容少讲，重点是为后面的 curriculum 做铺垫；② 只讲最基础的：模型架构大概什么样（基于 MLLM 的 embedding 模型）、用什么 loss；③ 不需要讲得特别复杂 |
| **参考来源** | 论文 Chapter 3 Model 部分 + 训练目标描述 |

---

### 第 17 页 — Study 1: Modality Pyramid / Curriculum

| 项目 | 内容 |
|------|------|
| **重要性** | 这块是 Study 1 最有 novelty 的部分，**值得详细讲** |
| **修改建议** | ① 文字描述可以更详细一些；② 多从论文中摘取内容，说明 curriculum 的**设计 motivation** 和具体细节；③ 讲清楚为什么这样设计有效（利用任务间的层级关系） |
| **核心要点** | 什么是 Modality Pyramid、为什么从简单到复杂、怎么实现的、为什么有效 |
| **参考来源** | 论文 Chapter 3 Curriculum 部分，包括 motivation 和具体设计 |

---

### 第 18 页 — Study 1: 主实验结果

| 项目 | 内容 |
|------|------|
| **结构问题** | 实验结果现在才出现，而 findings（12、13 页）在前面，顺序混乱 |
| **建议** | findings 应该和实验结果放在一起讲（可以是实验页上的标注，或紧随实验之后） |
| **内容评价** | 这一页简单呈现数据，有基本结果就行，OK |
| **Takeaway** | takeaway 总是写得很奇怪，建议更直观一点，有啥说啥（比如 "GVE-7B achieves SOTA across 16 datasets"） |

---

### 第 19 页 — Study 1: 实验结果 2 / Radar 图

| 项目 | 内容 |
|------|------|
| **Takeaway** | Take-away 是必须的；但实验部分不必每页都留 takeaway 栏的位置，在图旁边标注也行 |
| **其他** | 后面还有其他 findings，要统一考虑组织方式 |

---

### 第 20 页 — Study 1: Ablation

| 项目 | 内容 |
|------|------|
| **评价** | 可以，保持简洁 |
| **建议** | 稍微简单一点，没必要特别复杂；大概保持这样就行 |

---

### 第 21 页 — Study 1: 实验图

| 项目 | 内容 |
|------|------|
| **评价** | 还可以 |
| **建议** | 图可以稍微放大一点点；如果不好调整就算了 |

---

### 第 22 页 — Study 1: Data Scaling

| 项目 | 内容 |
|------|------|
| **重要性** | 这一页很重要 |
| **现状问题** | 图太大、字也太大；讨论和说明不够 |
| **修改建议** | ① 图稍微缩小一点，留出空间给文字讨论；② 增加分析说明（不同任务上 scaling behavior 不同等）；③ **写一个清晰的 takeaway**，总结 scaling 的关键发现 |
| **参考来源** | 论文 Chapter 3 中 data scaling 分析部分 |

---

### 第 23 页 — Study 1: Zero-shot Classification Transfer

| 项目 | 内容 |
|------|------|
| **建议** | **移到附录（Backup）中** |
| **理由** | 论文正文里也是放在附录的；主报告时间有限，这个不是核心内容 |

---

### 第 24 页 — Study 1 总结

| 项目 | 内容 |
|------|------|
| **现状问题** | 没有把工作的每个点讲清楚；前面页面顺序和总结页的顺序不一致 |
| **修改建议** | ① 好好 recap 整个 study 的流程和每一块在干什么；② 保持顺序一致性（diagnose → data synthesis → curriculum → results）；③ 每个方法模块：设计 motivation + 亮点 + 关键结果，各用一句话 recap；④ **不用 takeaway 栏**，内容本身就是总结；⑤ 配上核心实验结果（关键数字），让没跟上的听众也能回顾 |
| **参考来源** | 论文 Chapter 3 Conclusion / Contributions 总结 |

---

### 第 25 页 — Study 2 开篇（MG-LVR / Observational Scaling）

| 项目 | 内容 |
|------|------|
| **术语** | "observational" 不是很直观，可以考虑用 "sampling" 来解释（采样就是观测） |
| **论文状态** | 改为 **Submitted to AAAI 2027**（人工智能顶级会议） |
| **核心问题** | 把简单问题说清楚：视频输入模型时，应该怎么采样？采样就意味着我们观测到了什么 |
| **修改建议** | ① 更新论文状态；② 用更直观的语言引入 observational scaling（从"采样"这个大家熟悉的概念入手）；③ 作为 Study 2 第 1 页，讲清楚：解决什么问题、核心思路、主要贡献 |
| **优先级** | 高 — 论文状态是事实性更新 |

---

### 第 26 页 — Study 2 Motivation / Granularity Gap

| 项目 | 内容 |
|------|------|
| **现状评价** | 出发点是好的，想讲清楚事情 |
| **问题** | 不够直观，需要补充说明 |
| **修改建议** | ① 把"granularity gap（粒度鸿沟）"讲清楚；② 多参考论文内容，用更直观的方式解释；③ 可以用一个具体例子说明：同样的视频，查询粒度不同（整体主题 vs 某个具体瞬间），检索难度天差地别 |
| **参考来源** | 论文 Chapter 4 Introduction 第 17-21 行关于 granularity gap 的论述 |

---

### 第 27 页 — Study 2: Benchmark Definitions

| 项目 | 内容 |
|------|------|
| **工具/软件** | 图中工具软件部分还没弄好，需要编辑完善 |
| **颜色标注** | cos green 没有说明清楚范围；fine = Fine Green、medium = Medium Green，都缺了 "green" 这个词 |
| **Definition 布局** | 定义写完又拆到其他地方很奇怪；建议左边分两栏：上面文字、下面公式，一一对应 |
| **"Why it matters"** | 这部分在讲什么不清晰；需要说明为什么要做这些区分（为什么区分粒度很重要） |
| **缩写统一** | 全文统一缩写：Fine = FN、Coarse = COS = C、Medium = MD |

---

### 第 28 页 — Study 2: 主结果图

| 项目 | 内容 |
|------|------|
| **评价** | 还可以 |
| **修改建议** | ① "Takeaway message" 直接在副标题里说清楚，展示范围等即可；② 不用过多文字；③ **尽量把图放大一点** |

---

### 第 29 页 — Study 2: Benchmark Construction / CLIP Graph

| 项目 | 内容 |
|------|------|
| **标题问题（严重）** | 用 "CLIP graph" 做标题很奇怪。这张图实际展示的是 **MG-LVR benchmark 的整个构造流程**，CLIP graph 只是其中一步 |
| **修改建议** | ① 标题改为描述性的，如 "Benchmark Construction Pipeline"；② 在图中加一个文本框/标注，专门说明 CLIP graph 是什么、起什么作用（这可能是一个重点）；③ **统一标题风格**——不要再用结论式标题，改用论文 section 式的描述性标题 |
| **参考来源** | 论文 Chapter 4 第 101-124 行，MG-LVR 构造流程五步 |

---

### 第 30 页 — Study 2: Temporal Scaling Results

| 项目 | 内容 |
|------|------|
| **问题 1** | 没有说清楚 **Fine Green (FN)** 这边可以涨的百分点比较多 |
| **问题 2** | 缩写不统一：所有 COS 和 Fine 都用统一缩写（Fine = FN，COS = C） |
| **检查** | 转完 PPT 后要自己再检查一遍缩写一致性 |

---

### 第 31 页 — Study 2: Temporal Scaling 结论

| 项目 | 内容 |
|------|------|
| **问题 1** | 为什么只用了 temporal？spatial 去哪了？需要解释（或补上 spatial 内容） |
| **问题 2** | 结论太细了，应该更 **general（通用）** 一些 |
| **建议的通用结论方向** | ① 不同模型有不同的 scaling behavior，趋势不一样（有的下降、有的能保持）；② CLIP-based 模型确实表现不同；③ 空间 embedding 表现特别好，其他部分各有特点，强调"每个模型不一样"；④ 重点对比 fine / medium / cos 上的差异 |
| **原则** | 说一些通用的发现，不要太细的具体结论 |

---

### 第 32 页 — Study 2: Spatial + Trade-off

| 项目 | 内容 |
|------|------|
| **现状问题** | 前面只有 temporal，spatial 直接没了，跳到 tradeoff，很突兀 |
| **修改建议** | ① **补上 Spatial scaling 的内容**（哪怕简单过一下也行）；② 把 temporal 和 spatial 放在一起总结：不同模型在不同任务上的 scaling behavior 是不一样的；③ Trade-off 简单说一下即可——什么场景下帧多一点好（如翻译/精细查询），什么场景下清晰度高一点好（如个人视频/粗粒度查询） |

---

### 第 33 页 — Study 2: Resolution Scaling

| 项目 | 内容 |
|------|------|
| **现状问题** | 讲得不够清楚；只讲了实践上的结论；纯文字讲不清楚 |
| **修改建议** | ① 需要更直观的结论——让听众不用看数字、不用理解实验设置，也能知道实际中怎么选；② 考虑加一个示意图或决策流程图；③ 用更通俗的语言总结 practical guidelines |
| **核心信息** | 低帧数时分辨率更有用，高帧数时分辨率收益递减——这类实践性结论 |

---

### 第 34 页 — Study 2: VEterfall / Dense-to-Sparse Distillation

| 项目 | 内容 |
|------|------|
| **硬伤** | 公式有乱码——**必须修复** |
| **内容问题** | 没有给出重要结论；核心概念没讲清楚 |
| **必须讲清楚的四点** | ① **什么是 progressive？** ② **什么是 dense-to-sparse self-distillation？** |
| **Dense-to-sparse 解释** | 同一个模型，用不同的采样方式。拷贝一份模型，不同采样密度产出 embedding，用 MSE 做蒸馏——相当于"自己蒸自己"，只是产出方式（采样密度）不一样 |
| **Progressive 解释** | 每次产出两种密度的 embedding，不断从高密度到低密度逐步蒸馏。高密度 embedding 包含更多细节信息，作为老师教低密度的 |
| **核心 Insight** | 什么是好的 embedding？在同样的维度里，尽可能保留多的细节信息。维度是固定的，但视频信息在增长，不能指望全部保留，要尽可能多保留 |
| **建议** | 这一页很 interesting，**适合写一行清晰的 take-away message** |
| **参考来源** | 论文 Chapter 4 VEterfall 方法部分 + 论文第一章中的相关描述 |

---

### 第 35 页 — Study 2: VEterfall 续

| 项目 | 内容 |
|------|------|
| **建议** | 和第 34 页结合起来设计 |
| **重点讲清楚** | ① 什么是好的 embedding？② 不同密度下，什么样的 embedding 是好的？③ 为什么要用 dense 和 sparse？④ 为什么要用 progressive？ |

---

### 第 36 页 — Study 2: 补充结果

| 项目 | 内容 |
|------|------|
| **定位问题** | 很奇怪，像是 appendix 内容，用来辅助第 30 页或第 32 页的 |
| **修改建议** | 方案 A：**把结论前移**，整合到对应的主结果页中；方案 B：**直接移到附录**，主报告不再展示 |
| **理由** | 前面内容已经很 self-contained 了，这页不是必须的 |

---

### 第 37 页 — Study 2 总结

| 项目 | 内容 |
|------|------|
| **现状问题** | 和 Study 1 总结有同样的问题——不够好，看一遍没跟上的人不知道在讲什么 |
| **用词问题** | "intervene" 奇怪，不是学术词汇；"evidence" 也不是重点 |
| **修改建议** | ① 重点放在 **motivation + 方法** 上，而不是 evidence；② Take-away 可以有，但 evidence 部分没必要详细讲；③ 结构：问题 → 方法（benchmark + analysis + VEterfall）→ 核心发现；④ 因为 Study 2 的 novelty 在方法和发现上，要突出这一点 |
| **参考来源** | 论文 Chapter 4 Conclusion / Contributions |

---

### 第 38 页 — Study 3 开篇（GMP-GR / Search Scaling）

| 项目 | 内容 |
|------|------|
| **用词问题** | "signal" 奇怪，不直观 |
| **核心定位** | **不能聚焦在 recommendation 上**，那最多只是背景/应用场景。一定要讲清楚：**主要讲大规模部署时的检索问题** |
| **修改建议** | ① 明确说清楚这个 study 关注的是 large-scale deployment 下的 search scaling 挑战；② recommendation 只是验证场景；③ 作为 Study 3 第 1 页，讲清楚：问题是什么、为什么难、我们的思路 |
| **参考来源** | 论文 Chapter 5 Introduction 关于三个挑战的论述 |

---

### 第 39 页 — Study 3: Background / Retrieval Pipeline

| 项目 | 内容 |
|------|------|
| **建议** | 可以用论文 Introduction 里的那张图（工业界 recommendation pipeline 图）来说明：Ranking 之前先 Retrieval，主要是降数量级 |
| **现状问题** | 目前可能还没让人完全明白：输入输出是什么？里面需要注意什么？ |
| **修改建议** | ① 加一张 pipeline 示意图；② 讲清楚 retrieval 在工业推荐系统中的位置和作用；③ 明确挑战：从亿级 item 中快速找到相关的千级候选 |

---

### 第 40 页 — Study 3: Metric / SCL

| 项目 | 内容 |
|------|------|
| **现状问题** | 直接抛出概念很奇怪 |
| **修改建议** | 循序渐进：① 先讲 metric 和 triangle inequality 的基本概念（为什么度量性质对图搜索重要）；② SCL / Self-Covariant Contrastive Learning **放到后面方法页再讲**（比如移到第 41 页），不要在引入页就抛出来 |

---

### 第 41 页 — Study 3: 方法 1（MUIRML / Metric）

| 项目 | 内容 |
|------|------|
| **现状问题** | 太简略了，就几句话，不够清晰 |
| **修改建议** | ① 每块方法可以再详细一点；② 文字量增加 20-30%；③ 讲清楚 motivation + 核心思路 + 关键设计 |
| **重要性** | Study 3 方法部分整体偏弱，这是重点加强的第一页 |
| **参考来源** | 论文 Chapter 5 第 132-150 行 MUIRML 部分 |

---

### 第 42-43 页 — Study 3: 方法 2-3（HiPANNS / GPU Acceleration）

| 项目 | 内容 |
|------|------|
| **总体要求** | **更加尊重毕业论文原文** |
| **具体要求** | ① 可以使用公式；② 把 Motivation 和关键点讲清楚；③ 语言通俗但保持学术专业；④ 不用搞太多花里胡哨的，尊重原文就行 |
| **重点** | 每个方法模块：为什么需要（motivation）→ 核心思想 → 怎么实现 → 优势是什么 |
| **参考来源** | 论文 Chapter 5 方法部分各小节 |

---

### 第 44-45 页 — Study 3: 实验

| 项目 | 内容 |
|------|------|
| **建议** | 参考前面两个 study 实验的表现风格，保持一致 |

---

### 第 46 页 — Study 3: 部署 / Application

| 项目 | 内容 |
|------|------|
| **图的位置** | 前面提到的 Introduction 的 pipeline 图可以放到前面（第 39 页）去，当然放在这里也行 |
| **实验内容** | ① 可以加点上线的东西（online A/B results）；② throughput、compilation 等内容可以**捏到前面两页实验里**，更浓缩，不用占这么多页 |
| **整体方向** | Study 3 实验部分要压缩，方法部分要扩充 |

---

### 第 47 页 — Study 3 总结

| 项目 | 内容 |
|------|------|
| **总体评价** | 前面两个 study 的总结页都做得不够好，这一页要吸取教训 |
| **Study 3 特殊性** | 讲一些工业/上线的结果是挺重要的（和前两个 study 不同）；前两个 study 更强调 novelty |
| **建议结构** | 问题 → 方法（metric + HiPANNS + GPU 加速）→ 部署效果 → 核心贡献 |

---

### 第 48 页 — Synthesis / 综合论述 1

| 项目 | 内容 |
|------|------|
| **用词问题** | "structure where scaling" 很奇怪；整个 PPT 里 "pipeline level"、"structure-aware" 这类词都用得很生硬 |
| **修改建议** | 从论文原文中找更自然的表述；核心意思是"针对检索 pipeline 每个阶段的结构特点，设计相应的 scaling 方法"，但要用更流畅的学术表达 |

---

### 第 49 页 — Synthesis / 综合论述 2

| 项目 | 内容 |
|------|------|
| **总体要求** | 更尊重原文，总结更清晰简练；用词要简短、让人读得懂 |
| **深度要求** | **要真正体现研究上的贡献/insight**，不能只是陈列技术和工业上的东西。毕竟这是 PhD research defense |
| **修改建议** | 从更高的层次总结三个研究的关联和共同发现；提炼出方法论层面的 insight |
| **参考来源** | 论文 Chapter 6 Conclusion |

---

### 第 49-51 页 — Conclusion / Synthesis 整体

| 项目 | 内容 |
|------|------|
| **现状问题** | 三页的展现方式需要重新考虑；内容像是三个独立工作的罗列，没有呼应前面 Introduction 的框架 |
| **修改方向** | ① 不是三个独立工作的罗列，而是一个统一框架下的三个阶段；② 呼应 Introduction 中提出的三个 scaling 挑战；③ 更侧重于方法论上的总结 |
| **内容侧重** | • **Motivation / 整体框架**：不用讲太多，说明三个部分的关系，整体解决了 video retrieval scaling 的什么问题，呼应 scalable 和 generalizable<br>• **实验结果**：配合展示是必要的，但肯定不是重点<br>• **核心贡献**：方法层面的 insight 和贡献才是重点 |

---

### 第 52-54 页 — Future Work

| 项目 | 内容 |
|------|------|
| **现状问题** | 没有点到点子上 |
| **应该包含的三要素** | ① **难点与突破点**：热门的、可能用上的技术点，或者值得研究、有挑战的方向<br>② **研究框架**：技术不用计划太细，但要有一个 research framework，说明大致可以朝几个方向做<br>③ **具体规划**：在某个问题下，哪个点最吸引人？大概怎么做？解决了有什么意义？最终是什么样？ |
| **建议** | 重新组织 Future Work 的结构，按照上述三要素来设计 |

---

### 第 55 页 — Research Output / Publications

| 项目 | 内容 |
|------|------|
| **论文状态更新** | ① ACM MM 2026 → 已 accept（终稿）<br>② ECCV → 改为 **Submitted to AAAI 2027**<br>③ Web Conference (The WebConf) → 已 publish |
| **优先级** | 高 — 事实性更新 |

---

### 第 56 页 — Q&A / Questions

| 项目 | 内容 |
|------|------|
| **现状问题** | Question 页没有呼应前面的题目/主题，没有引导性 |
| **修改建议** | 加入一些引导性的内容，呼应论文主题；可以放一个核心问题或总括性的句子作为过渡 |

---

### 附录 / Backup Slides

| 项目 | 内容 |
|------|------|
| **内容** | 前面从主报告中移下来的内容都移到附录中（如第 23 页 zero-shot classification、第 36 页补充结果等） |
| **设计** | 每一页的设计也要遵循前面的设计规范（标题风格、排版等） |
| **原则** | 综合考虑，用户没有给出太细节的建议，自行按照前面的标准统一即可 |

---

## 三、Study 1 整体结构调整建议

> Study 1 的内容顺序问题最大，单独列出详细调整方案。

### 当前顺序（有问题）
```
9.  Study 1 开篇
10. Motivation / The Trap
11. UVRB / Diagnostic Framework
12. Key Findings 1
13. Key Findings 2
14. V-SynFlow 数据合成      ← 方法放在了实验之后！
15. UVRD 数据集统计
16. GVE 模型架构
17. Curriculum Learning
18. 主实验结果              ← 实验结果才出现
19. 实验结果 2 / Radar
20. Ablation
21. 实验图
22. Data Scaling
23. Zero-shot transfer     ← 建议移到附录
24. Study 1 总结
```

### 建议顺序
```
9.  Study 1 开篇 [ACM MM 2026]
    ├─ 问题：碎片化评估、能力缺口
    └─ 思路：诊断 → 数据 → 课程 → 通用嵌入

10. Motivation / The Trap [精简]
    ├─ 领域狭窄 + 能力碎片化
    └─ 为什么现有方法解决不了

11. UVRB / Diagnostic Framework [基本保持]
    └─ 统一评估协议，系统诊断能力缺口

12. Key Findings [与 13 页合并或重排]
    └─ 核心发现：什么能力缺失、为什么重要

13. V-SynFlow / 数据合成方法 [从 14 页前移]
    ├─ 三步骤：Quality Control → Info Enrichment → Task Extension
    ├─ 去掉 60/30/10 比例
    └─ 呼应前面的能力缺口

14. UVRD 数据集统计 [从 15 页前移，精简]
    ├─ 关键数字：1.55M pairs
    └─ Human evaluation: 95/100

15. GVE 模型架构 [从 16 页前移，精简工程细节]
    └─ 基础架构 + Loss（为 curriculum 铺垫）

16. Modality Pyramid / Curriculum [重点加强]
    ├─ 设计 motivation
    ├─ 具体细节
    └─ 为什么有效（novelty 所在）

17. 主实验结果 [从 18 页后移]
    └─ SOTA 结果 + 关键对比

18. 实验结果 2 / Radar 图 [从 19 页]
    └─ 多维度能力展示

19. Ablation [从 20 页，保持简洁]

20. 实验图 [从 21 页，可稍微放大]

21. Data Scaling [从 22 页，加强分析 + takeaway]

22. Study 1 总结 [重写]
    ├─ 流程 recap：diagnose → synthesize → curriculum → evaluate
    ├─ 每个模块的 motivation + 亮点 + 关键结果
    └─ 核心贡献总结

[附录] Zero-shot classification transfer [从 23 页移至附录]
```

**净变化**：主报告减少 1 页（23 页 → 22 页 + 1 页附录），顺序更符合学术报告逻辑。

---

## 四、Study 3 整体调整建议

### 核心问题
- 实验部分太多，方法部分太弱
- 概念部分有冗余
- 重点不够突出（方法才是 PhD defense 的重点）

### 调整方向
1. **方法部分扩充**（第 41-43 页）：增加 20-30% 文字量，讲清楚每个方法的 motivation + 核心思路 + 关键设计，可以加公式
2. **实验部分压缩**（第 44-46 页）：把 throughput、compilation 等内容合并浓缩，减少页数
3. **概念部分精简**（第 38-40 页）：去掉冗余，循序渐进引入
4. **总结页加强**（第 47 页）：突出方法贡献 + 工业验证价值

---

## 五、待确认事项

以下内容需要用户确认或提供更多信息：

1. **Study 2 论文状态**：确认是 "Submitted to AAAI 2027" 吗？之前提到的是 ECCV，用户说改成 "submitted to a AI"，这里理解为 AAAI 2027，对吗？
2. **第 23 页 zero-shot classification**：确认移至附录吗？
3. **第 36 页补充结果**：确认移至附录吗？
4. **Study 1 结构大调整**：上述顺序调整方案是否可行？
5. **标题风格大改**：所有标题从"结论式"改为"描述式"（类似论文 section），这个改动比较大，确认要改吗？

---

## 六、优先级排序

### P0 — 必须改（事实错误/硬伤）
- 论文发表状态更新（第 9、25、55 页）
- 公式排版错误修复（第 5、34 页）
- 乱码修复（第 34 页）

### P1 — 重要（内容准确性/逻辑顺序）
- Study 1 内容顺序调整（方法和实验顺序颠倒）
- 术语和表达修正（从论文原文摘取，不自创）
- Takeaway 学术化重写
- Study 3 方法部分扩充

### P2 — 中等（体验优化）
- 标题风格统一改为描述性
- 封面字号调整
- 目录页视觉优化
- 各页布局微调

### P3 — 较低（锦上添花）
- 图的大小微调
- 附录页面设计统一
- Future Work 深度优化

---

*文档版本：v0.6-plan · 整理日期：2026-07-25*
