# Defense Slides V0.9：重构后的审阅意见与迭代规范

> **归档状态（2026-07-28）**：该审阅计划已通过 V0.82–V0.87 分批实施，
> 最终成果定版为 V0.9。本文档保留为合并后的意见来源与验收依据，最终版本、
> 关键修改过程和 QA 结果以 `v0.9-build/CHANGELOG.md` 为准。
>
> 本文档由原始 `TODO-v0.9.md` 整理而来。原始重复记录已在 V0.9 归档时
> 移入系统废纸篓。
>
> 整理依据：
>
> 1. 用户对 `thesis-slides-v0.81.pptx` 的逐页意见；
> 2. 对 V0.81 全部 69 页的内容与视觉检查；
> 3. 论文 `main.pdf`、`supplementary.pdf` 及对应 `.tex` 源文件；
> 4. `SLIDES-GUIDE.md` 与历史 `TODO-v0.6.md` 中仍然有效的证据边界和失败经验。
>
> 本轮工作的目标不是机械修正被点名的页面，而是把具体意见泛化为覆盖全套
> 幻灯片的审阅标准，并通过 V0.82、V0.83、V0.84、V0.85 等小步版本逐步实现。

---

## 一、最高层目标

这是一场博士论文答辩，不是三篇论文的串联汇报，也不是以结果数字为主的项目
报告。整套幻灯片必须让答辩委员会清楚理解：

1. 论文在 video retrieval 研究中的位置；
2. 为什么现实检索从短视频、固定文本查询和小规模候选集，发展为需要处理异构
   查询、长且信息密集的视频以及超大候选集的方法论问题；
3. 为什么论文选择 semantic、observational 和 search scaling 这三个问题；
4. 三个问题为什么沿检索过程依次出现，上游能力为什么不能自动解决下游问题；
5. 每个 Study 的研究缺口、关键挑战、设计原则、方法创新、工作机制和证据边界；
6. 三个 Study 如何共同构成“可扩展且具有泛化能力的视频检索”这一篇完整博士
   论文。

建议用一句话检查全套幻灯片的沟通任务：

> 答辩结束时，委员会应当理解，视频检索的扩展不是单纯增加模型、帧数或指标
> 精度，而是要在语义表示、视觉观测和大规模搜索三个连续阶段分别解决不同的
> scaling challenge，并检验所得能力能否迁移到优化条件之外。

---

## 二、两种角色的联合审阅方法

### 2.1 顶级审稿人视角

每页都要追问：

- 这一页的论断是否来自论文，还是幻灯片临时创造的口号？
- motivation、research gap 和 challenge 是否被清楚地区分？
- 方法是否真正回应了前面提出的问题？
- “为什么有效”是否有机制解释，而不只是“方法存在 + 实验提升”？
- 数字是否有比较对象、实验条件、样本量和适用边界？
- 是否把单个实验点夸成普遍规律，把软约束夸成形式保证，或把 token reduction
  夸成实际 latency/throughput？
- 听众在当前页是否已经知道公式、缩写、变量和方法名的最小必要定义？
- 这一页是否推进博士论文的主线，还是只展示一项局部结果？

### 2.2 顶级作者视角

每页都要追问：

- 听众在这一刻最需要知道什么？
- 上一页提出了什么问题，本页回答什么，下一页为什么自然出现？
- 论文原文中最准确、最有辨识度的关键词和句子是什么？
- 哪些内容应该放在主页面，哪些数字和工程细节应放入附录或演讲备注？
- 视觉重点是否与论证重点一致？
- 是否能用更普通、更清楚、更学术的语言保持原意？

两种角色的共同准则是：**先恢复论文的因果链，再选择文字和布局。**

---

## 三、原论文可见性与证据优先级

### 3.1 已确认可访问的关键材料

- V0.81：`slides/thesis-slides-v0.81.pptx`，69 页；
- 主论文：`main.pdf` 与 `main.tex`；
- 补充材料：`supplementary.pdf` 与 `supplementary.tex`；
- 章节源文件：`chapters/*.tex`；
- 附录源文件：`appendices/*.tex`；
- 论文图：`figures/`；
- 幻灯片复用图：`slides/figures/`。

因此，本轮工作不存在“看不到原论文”或“看不到 PPT”的致命缺失。

### 3.2 证据优先级

同一内容在论文不同位置表述不完全一致时，按下列顺序判断：

1. 对应研究章节的方法、实验表格和图；
2. 对应章节的 Introduction 与 Conclusion；
3. 论文总 Introduction、Abstract 和总 Conclusion；
4. 现有幻灯片与历史维护记录。

幻灯片应保持论文原意和 claim strength，但不要求逐字照抄。答辩表达可以更
简洁、更直观。

### 3.3 需要批判性继承的原文

- 论文使用 `bottleneck` 和 `diagnose/diagnostic`，但用户明确认为这些词在答辩
  中突兀。幻灯片保留其概念，优先改成 `scaling challenge`、
  `stage-specific constraint`、`capability assessment`、`identify` 或
  `analyze`。
- `pipeline` 只有在先定义“检索的连续阶段”后才使用。面向听众时优先使用
  `retrieval stages` 或直接说 representation、observation、search。
- 论文总 Introduction 对 VEterfall 有一处“adaptive allocation across video
  segments”的概括，但第四章方法明确是 progressive dense-to-sparse
  self-distillation。幻灯片以第四章方法为准，不能讲成自适应片段分配。
- 第五章部分文字接近于声称 SCL 赋予 triangle inequality，但现有证据只支持
  软排序约束带来的实证改善。幻灯片继续使用“encourages ordering regularity”
  等克制表述，不能宣称形式化保证。

---

## 四、全套幻灯片的共性问题

### 4.1 博士论文主线不够持续

V0.81 已经给出三个 scaling 名称，但关系主要停留在“按检索过程排列”。需要在
Introduction、三个 Study 的过渡、三个 Summary 和 Conclusion 中持续回答：

- 为什么这三个阶段共同决定可扩展性；
- 为什么前一个 Study 的成功仍会暴露下一个 Study 的问题；
- 每个 Study 为下一阶段提供了什么前提；
- 为什么三者不是三个平行项目，而是一条从表示到部署的研究链。

建议的递进关系：

1. **Semantic scaling**：先获得覆盖异构查询、领域和相关性条件的表示能力；
2. **Observational scaling**：表示能力只有在模型观察到与查询相关的视觉证据时
   才能发挥作用；
3. **Search scaling**：得到可靠的表示和相关性信号后，还必须在超大候选集中
   以可部署的效率保留这种相关性。

### 4.2 页内因果链经常被压扁

许多页面直接从问题名跳到方法名或结果数字。核心页面应尽量恢复以下链条：

**Motivation → Research gap → Challenge → Design implication → Method →
Why it works → Evidence → Boundary → Novelty/Contribution**

不是每页都要写齐所有环节，但相邻页面合起来必须完整，且顺序不能颠倒。

### 4.3 方法中心性不足

当前多个 overview、summary 和 conclusion 页面把 benchmark 数量、数据规模和
结果数字放得过重。博士答辩应优先解释：

- 为什么选择这一设计；
- 方法的关键机制是什么；
- 机制具体解决哪一个 challenge；
- 实验如何验证机制，而不仅是验证最终分数；
- 方法相对于已有做法的新意是什么。

数字应服务于结论，不应替代结论。

### 4.4 “为什么有效”讲得不足

三个 Study 都需要明确的方法机制：

- Study 1：能力评估如何指导数据合成，任务层级为什么能减少异构任务之间的
  干扰；
- Study 2：为什么高密度表示中包含可迁移到稀疏输入的信息，为什么逐级蒸馏比
  直接改变采样配置更合理；
- Study 3：为什么多关系建模、排序规律、图遍历宽深平衡和跨查询 GPU 聚合必须
  联合设计。

### 4.5 自包含性不足

首次出现时必须给出最小定义：

- semantic / observational / search scaling；
- UVR、UVRB、UVRD；
- query formats、domains、S/T/PR；
- temporal granularity、continuity、FN/MD/CR；
- `F` 表示采样帧数，`T` 表示每帧保留的视觉 token 数；
- `4F-100T`、`8F-200T` 等配置；
- offline training 与 online search；
- MUIRML、SCL、C-HiPANNS、Q-HiPANNS。

定义不能依赖听众记住未来页面，也不能让公式单独承担解释。

### 4.6 术语和标题仍有生产式语言

需要全套搜索并修正：

- `bottleneck-aligned`、`bottleneck-specific`；
- 不必要的 `diagnose/diagnosis`；
- 未定义的 `pipeline`；
- 过于口号化、像生产备注或词语堆叠的标题和 takeaway；
- 同一术语的缩写、大小写和单复数不一致。

论文确有 `bottleneck` 等词，但用户对答辩表达的判断优先。建议使用普通而准确的
学术表达，不为了“高级”而增加抽象词。

### 4.7 实验页数字多，结论和机制对应不足

每个实验页应让听众快速看出：

1. 改变了什么；
2. 保持什么不变；
3. 观察到什么；
4. 结果说明方法或问题的哪一部分；
5. 结论的适用范围是什么。

不必在主页面展示所有数据。重要的是实验结论、分析深度和对方法设计的启发。
完整表格、次要配置和补充证据可放附录。

### 4.8 三个 Study 的 Summary 不统一

第 22、37、47 页应共享研究逻辑，但不强制相同框数或相同版式。每个 Summary
至少回答：

- 起点是什么 research gap；
- 研究过程如何从 benchmark/analysis 走到方法；
- 方法 novelty 是什么；
- 对应解决了什么 challenge；
- 哪项证据支持结论；
- 对整篇论文和下一个 Study 有什么意义。

Summary 的核心是 novelty 和 contribution，不是 evaluation evidence 清单。

### 4.9 Conclusion 没有完成“重新解释整篇论文”

第 49–51 页当前分别使用表格、三列卡片和 generalizability 卡片，信息存在，但
仍像分类整理。应重新分工：

- 第 49 页：回顾三个 Study 的递进关系，以及为什么选择这三个 challenge；
- 第 50 页：综合三个方法怎样解决对应问题，并把 generalizability 融入方法和
  验证；
- 第 51 页：提出完成三项研究后的领域级 insight，解释什么是 scalable、
  generalizable video retrieval，以及这一框架把研究推进到了哪里。

### 4.10 Future Work 仍偏关键词化

第 52–55 页不能只显示概念和流程框。每个方向都应明确：

1. 当前研究状态或动机；
2. 尚未解决的 research gap；
3. 最难的 technical challenge；
4. 可能的方法方向；
5. 成功后带来的研究贡献或意义；
6. 哪些内容仍是推测，不能作为已完成结果。

### 4.11 视觉组件有时替代了文字判断

V0.81 整体视觉稳定，但存在以下共性：

- 卡片和框很多，容易把因果关系切成平行信息；
- 表格和数字的视觉权重有时高于方法逻辑；
- 部分 overview 和 conclusion 页面过密；
- 少数重要页面的核心文字过小或埋在底部条带中；
- 框的数量、对称性和颜色不应决定内容结构。

文字、图和布局都必须服务于论证。框不是贡献，清楚的研究逻辑才是。

### 4.12 全局一致性和已发现的硬问题

- 顶部导航目前多页写作 `Observational`，应统一为论文术语
  `Observational Scaling`；
- 第 11 页同页同时出现 `14 evaluated models` 和 `14 baselines`，应按语境统一；
- 第 26 页存在 `high-fieldty` 拼写错误，应改为 `high-fidelity`；
- 第 30 页必须继续使用
  `figures/mglvr/mglvr_testtime_spatial_scaling_2.png`；
- 所有 `F`、`T` 配置必须先定义再使用；
- 继续保留 `95 / 100`，不能把初步人工审核只写成孤立的 `95%`；
- 不把 input-token reduction 写成已测得的 latency、throughput 或端到端效率；
- 不把单个配置写成完整 operating curve 或 Pareto 证明；
- 不把 SCL 写成 triangle-inequality 保证；
- 不把相关性分析当作因果证明。

---

## 五、分区重构要求

### 5.1 Introduction（第 1–8 页）

#### 当前共性缺陷

- `bottleneck` 在封面、副标题、框架、方法列和结尾反复出现；
- 第 7 页把三个工作压缩成“naive scaling / why it fails / method”，带有生产式
  诊断语言和孤立数字，方法论层次不够；
- 第 8 页过密，benchmark 数字和实验结果抢占 overview；
- 三个 Study 的关系虽然写成顺序，却没有充分解释为什么一个阶段自然引出下一
  阶段；
- 在 video retrieval 领域从短视频固定匹配走向真实复杂条件的 position 仍可
  更突出。

#### 重构目标

- 第 1–5 页完成领域位置、基本问题和现实扩展；
- 第 6 页定义三个连续的 scaling challenges；
- 第 7 页聚焦每个 Study 的 challenge 与 design direction，不放孤立实验数字；
- 第 8 页聚焦三个具体方法、验证方式和递进关系，减少统计数字；
- Introduction 结束时，听众已经知道为什么是这三个 Study、每个 Study 做什么、
  三者如何组成一篇论文。

### 5.2 Study 1：Semantic Scaling（第 9–22 页）

#### 结构问题

第 12 页详细的 Capability Correlation Analysis 位于 benchmark 之后、方法
之前，用户认为它更像实验分析。建议：

- 第 11 页保留 UVRB 的能力空间和最小必要评估结论，用于说明方法动机；
- 将第 12 页详细相关性分析移动到方法和主要结果之后的实验分析块；
- 移动后同步修复第 13 页 V-SynFlow 的引入、实验页引用、Summary 和页码逻辑。

#### 第 13–16 页

- 尽量复用第三章 Introduction 和 Methodology 的关键词；
- V-SynFlow 讲清质量控制、信息丰富和多任务扩展如何回应能力缺口；
- UVRD 强调 gap-targeted，而不是单纯规模大；
- GVE 架构只保留理解 Modality Pyramid 所需的基础；
- Modality Pyramid 是核心 novelty，需要解释任务层级、从基础到复杂的顺序、
  如何动态调节采样，以及为什么能减少任务干扰。

#### 第 17–21 页

- 实验从“分数展示”转为“验证哪一项方法机制”；
- 将 capability correlation 作为实验分析，而非方法之前的突发结论；
- 说明 UVRD 与 curriculum 的互补性；
- 保留 VIS 的诚实边界；
- 数据 scaling 强调不同能力和模型规模的不同斜率，不夸大为普遍规律。

#### 第 22 页

按以下逻辑重写：

**fragmented evaluation → capability assessment → gap-targeted synthesis →
task-hierarchy curriculum → broader zero-shot generalization**

突出方法 novelty、各 contribution 之间的关系，以及 Study 1 为后续研究建立的
表示基础。结果数字只保留一项必要证据。

### 5.3 Study 2：Observational Scaling（第 23–37 页）

#### 第 24 页

- 更精炼地说明为什么 sampling 决定可用证据；
- 明确实际输入如何形成：从长视频中采样 `F` 帧，每帧保留 `T` 个视觉 token；
- 解释 temporal coverage 与 spatial detail 的权衡；
- 避免只画抽象刻度而不说明真实采样过程；
- 将“structural bottleneck”改为更清楚的 sampling constraint/challenge。

#### 第 25–29 页

- temporal granularity、continuity、FN/MD/CR 定义必须直观；
- MG-LVR 的数字服务于“为什么可以做受控分析”；
- `F`、`T`、test-time scaling、training-time scaling 在实验前完成定义；
- 说明 test-time 改变观测证据，training-time 改变学到的表示。

#### 第 30–34 页

主报告不能漏掉 training-time spatial scaling：

1. test-time spatial density；
2. test-time temporal density；
3. fixed-budget spatiotemporal trade-off；
4. training-time spatial scaling：resolution robustness 与极高密度下的
   diminishing returns/trade-off；
5. training-time temporal scaling：frame-count anchoring 与双向 mismatch。

实验页强调结论和设计启发，不复制完整大表。训练时 spatial 与 temporal 的
不对称性必须清楚，并自然引出 VEterfall。

#### 第 35–36 页

- 先解释高密度表示中的知识为什么不会自动迁移到稀疏配置；
- 说明逐级 dense-to-sparse 比一次大幅降低密度更可靠；
- MSE 是主要 distillation signal，InfoNCE 是保持 video-text alignment 的辅助
  正则；
- `4F-100T` 之前必须定义；
- 结果不能只展示 `4F-100T`。主页面至少说明 `16F-400T`、`8F-200T`、
  `4F-100T` 三个配置的整体趋势；
- 明确 8F 和 4F 的收益更明显，高密度配置可能只有边际改善或出现 trade-off；
- 更完整表格留在附录。

#### 第 37 页

保留 Benchmark → Analysis → Methodology 的研究过程，但进一步强调：

- benchmark 为什么必要；
- scaling analysis 得出的核心不对称性；
- VEterfall 如何由该不对称性自然产生；
- novelty 是把受控分析转化为 progressive dense-to-sparse self-distillation，
  而不是只报告效率数字。

### 5.4 Study 3：Search Scaling（第 38–47 页）

V0.81 的方法链相对完整，后续以精修为主：

- 保持“问题定义 → 三个 challenge → offline/online overview → MUIRML →
  C-HiPANNS/Q-HiPANNS → system → evidence → summary”的顺序；
- 公式和 SCL 解释继续使用普通语言；
- 明确 SCL 是 soft ordering regularizer，不是 triangle inequality 的形式保证；
- 明确 C-HiPANNS 负责 query 内宽深平衡搜索，Q-HiPANNS 负责 query 间 GPU
  聚合，二者前后依赖；
- 生产优化数字必须与 method contribution 分开；
- 第 47 页进一步突出“metric、traversal、execution 的 co-design”为什么是核心
  novelty，实验只作为验证。

### 5.5 Conclusion（第 48–51 页）

#### 第 49 页：关系与选择理由

- 回到 Introduction 的同一组术语；
- 讲三个挑战为什么按顺序出现；
- 说明为什么这三个问题构成博士研究，而不是三个独立 case；
- 不再以大表格罗列 Scope、Validation 等分类项。

#### 第 50 页：方法综合与 generalizability

- 逐项说明方法怎样回应 challenge；
- 将 generalizability 放进每个方法的验证逻辑；
- semantic：跨 query formats、domains、relevance conditions；
- observational：跨 sampling densities、video lengths、query granularities；
- search：跨 offline/online、traffic patterns 和 serving constraints；
- 避免继续使用 `bottleneck-aligned scaling`。

#### 第 51 页：领域级 insight

- 解释完成三个 Study 后得到的研究框架；
- 说明“scalable”不是资源增加，而是方法与阶段约束匹配；
- 说明“generalizable”是能力是否迁移到优化条件之外；
- 说明本论文如何连接 representation learning、observation-aware embedding
  generation 和 deployment-scale retrieval；
- 给 Future Work 留出自然问题，而不是重复上一页。

### 5.6 Future Work（第 52–55 页）

每页采用以下内容骨架，而不是只采用流程框：

**Current limitation / research gap → key challenge → possible direction →
expected contribution → evaluation/boundary**

- Retrieval-native foundation models：生成隐藏状态与紧凑可判别表示之间的张力；
- Agent memory：连续流、稀疏事件、在线索引、实时查询和 perception-action loop；
- Self-evolving loop：新能力修复与旧能力保持之间的稳定性问题；
- Generative representations：连续生成状态可能对应不同抽象层，但判别性和成本
  仍是开放问题。

最后应回到第六章的总意义：video retrieval 可能从 standalone embedding task
发展为 multimodal intelligence 的基础接口，用于记忆、适应和视觉经验推理。

---

## 六、分版执行优先级

### V0.82：主线语言与 Introduction

- 清除全套 audience-facing 文本中不合适的 `bottleneck` 与生产式
  `diagnose/diagnosis`；
- 重写第 1、6、7、8 页的主线；
- 强化领域位置、三个 challenge、设计方向和 Study 递进关系；
- 统一顶部 `Observational Scaling`；
- 修复 `14 models/baselines`、`high-fieldty` 等硬问题；
- 保持 69 页，不做大规模重排。

### V0.83：Study 1

- 调整 capability correlation analysis 的位置；
- 重写第 13–16 页的 source-faithful 方法说明；
- 让实验对应 UVRD 和 Modality Pyramid 的机制；
- 重写第 22 页 Summary。

### V0.84：Study 2

- 第 24 页补足真实采样过程和 `F/T` 定义；
- 主报告补足 training-time spatial scaling；
- 第 30–34 页恢复完整 scaling hierarchy；
- 第 36 页扩展为多配置的 VEterfall 结果和 trade-off；
- 重写第 37 页 Summary。

### V0.85：Study 3、Conclusion 与 Future Work

- 精修第 47 页；
- 重构第 49–51 页；
- 让第 52–55 页明确 gap、challenge、意义和边界；
- 全套统一 novelty、contribution、finding 和 evidence 的层级。

如 V0.85 全量检查后仍有结构性问题，再继续 V0.86–V0.89。不能为了版本号停止，
也不能为了赶到 V0.89 一次改完。

---

## 七、每版必须保留的材料

每次迭代均需保留：

1. 新版本 PPTX，禁止覆盖旧版本；
2. 对应版本的编辑代码；
3. 该版本的变更记录，包括修改页、来源、理由和未解决问题；
4. 全量渲染结果放在临时 QA 目录，不放入公开版本目录；
5. 结构、溢出、关键图、包完整性和打开重载检查结果。

版本间要能回答：

- 本版只解决了哪一批问题；
- 哪些页保持不变；
- 哪些判断来自论文原文；
- 哪些内容因证据不足而没有改；
- 下一版的优先级是什么。

---

## 八、最终验收标准

### 8.1 内容

- Introduction 能独立说明领域位置、三个 scaling 的关系和三个 Study 的必要性；
- 每个 Study 都有完整的 motivation、gap、challenge、method、why it works、
  evidence、boundary 和 contribution；
- 三个 Summary 以方法 novelty 和研究逻辑为核心；
- Conclusion 真正综合三个 Study，而非再次分类罗列；
- Future Work 讲清难点、研究意义和推测边界；
- 所有重要句子均可追溯到论文或被标记为谨慎的编辑性概括。

### 8.2 视觉

- 每页一个主要论证任务；
- 标题、副标题、图、正文和结论的视觉权重符合论证层级；
- 无意外重叠、裁切、换行、孤词、过小文字或贴近页脚；
- 图像比例、清晰度和实验身份正确；
- 不用更多框来掩盖逻辑不清；
- 关键方法页和结论页在投影环境下仍然易读。

### 8.3 技术

- 每版文件名唯一，旧版不覆盖；
- PPTX 包结构有效，打开时不需要修复；
- 页数和 section boundary 符合预期；
- 所有图片存在，notes 和页面编号正常；
- 第 30 页继续使用正确的 spatial scaling 图；
- 每张最终幻灯片均完成全尺寸视觉检查；
- 自动 overflow 检查通过，但自动检查不能替代人工视觉检查；
- 未修改页与上一版比较后不存在意外漂移。

---

## 九、V0.9 落实结果

- **V0.82**：完成 Introduction、全局主线语言、三个 scaling 的关系和硬错误
  修正。
- **V0.83**：完成 Study 1 顺序、V-SynFlow、GVE、相关性分析和总结页重构。
- **V0.84**：完成 Study 2 的采样定义、完整 scaling hierarchy、VEterfall
  连接和总结页重构。
- **V0.85**：完成 Study 3、跨 Study 结论、Future Work 和全套稳定性检查。
- **V0.86**：继续全套精修任务/领域/子领域术语、V-SynFlow 阶段名、MG-LVR
  定义、SCL 证据边界、结论表达、附录范围和自包含 Q&A。
- **V0.87**：重构 Problem Formulation、三个 scaling 的关系、UVRD 覆盖、
  Modality Pyramid 技术细节、Experiment 分界和 Study 1 总结逻辑。

最终 V0.87 已原样提升为 V0.9，共 69 页。全套已完成逐页全尺寸检查，并通过
overflow、template fidelity 和 PPTX package integrity 检查。V0.81–V0.87
的关键修改过程、哈希、来源和 QA 结果统一在 `v0.9-build/CHANGELOG.md`
中追溯，最后一次精修的精确编辑代码保留为
`v0.9-build/edit-final-pass.mjs`。

仍需作者决定或后续处理：

- 第 23 页 publication status 按明确要求保持不变；
- 第 12 页嵌入的原论文图仍保留 “Multimodal Task Extending”，未擅自重绘；
- SCL 的实现级 score/distance sign convention 仍需代码证据；
- 最终试讲时长、主讲跳页方案和答辩前外部状态复核。
