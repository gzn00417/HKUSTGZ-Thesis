# V1.4 Speaker Notes

本讲稿对应 `thesis-slides-v1.4.pptx`，以当前 V1.3 deck 为基础，保留了作者最新的 slide 修改。

讲稿为较快但自然的语速设计。以 slide 为主要提示，先读出或转述 slide 上的关键短语，再用讲稿中的内容解释 research logic。

## Slide 1 — Towards Scalable and Generalizable Video Retrieval

各位老师、委员、同事和朋友们，早上好。我是郭卓宁，非常感谢大家参加我的博士论文答辩。

我衷心感谢我的导师 Prof. Xiaowen Chu 和 Prof. Renjing Xu。同时很荣幸邀请到 Prof. Pan Hui、Prof. Jeffrey Xu Yu、Prof. Yutao Yue、Prof. Xuming Hu 和 Prof. Meishan Zhang 担任我的答辩委员。感谢各位的时间、细致的审阅和宝贵的指导。

我还要感谢 AI Thrust 和 HKUST(GZ) 的行政人员，为今天的答辩做了细致的组织工作。

我的论文题目是 "Towards Scalable and Generalizable Video Retrieval"。它研究的是：当 query 变得更加多样、video 变得更长、candidate collection 变得大得多时，retrieval 应该如何变化。

## Slide 2 — Thesis Roadmap

这是我报告的 roadmap。我先介绍 video retrieval 问题，并解释它为什么产生三个相互关联的 scaling。

然后我会展示三个 study。Study 1 是 semantic scaling，Study 2 是 observational scaling，Study 3 是 search scaling。我会在 Study 1 结束时立刻连接到 Study 2，在 Study 2 结束时以同样方式连接到 Study 3。最后总结整篇 thesis，并讨论 future work 和 limitations。

建议：这边只要保持简单快速就可以了

## Slide 3 — Guiding Question

随着 query diversity、video length 和 corpus size 的增长，retrieval 方法应该如何变化？

这些变化不只是产生同一个问题的更大版本，而是在 representation、visual observation 和 large-corpus search 上分别产生不同的 bottleneck。请大家记住这个问题，因为每个 study 会解决一个 bottleneck，同时产生下一个 study 的需求。

## Slide 4 — Applications of Video Retrieval in Modern Multimedia Systems

这页展示了 video retrieval 在现代 multimedia 系统中的三个重要应用。

第一，在 search 场景中，用户可能提供 text、image、video clip 或 composed query。系统需要从 massive corpus 中找到相关 video，因此 relevance 由 query 与 candidate video 的匹配来定义。

第二，在 recommendation 场景中，系统需要将不断变化的用户兴趣与快速增长的 video catalog 进行匹配。Retrieval 是第一阶段，它选出一个 manageable 的 candidate set，然后 ranking model 生成最终的推荐列表。

第三，在 data processing 场景中，retrieval 可以为 foundation model training 过滤、清洗和组织 multimodal data。这在 large language model 时代对 understanding model 和 generative model 都有用。

这些应用共享一个不断变化的研究条件。Query 更加 heterogeneous，video 在更长的时长内包含更多信息，而 collection 太大以至于无法 exhaustive scoring。这 motivates 了本 thesis 研究的 scaling problem。

## Slide 5 — Problem Formulation: Embedding-Based Video Retrieval

这页对 embedding-based video retrieval 进行 formulating。

首先，我们将 user query 和 video corpus embed 到一个 shared space 中。Query 可以是 text、image、clip 或 composed query。Candidate video 可以 offline 编码。

其次，我们比较 query embedding 与每个 candidate embedding，通常使用 cosine similarity。在 training 时，相关的 query-target pair 应该比不相关的 pair 有更高的 score。

最后，我们对 candidate corpus 排序并返回 top-K video。这个基本 pipeline 很简单，但每个阶段都会引入不同的 scaling problem。

## Slide 6 — Why Video Retrieval Scales in Three Connected Steps

这页将 retrieval pipeline 与三个 study 连接起来。

我们从 user query 和 video corpus 出发。在 embedding training 阶段，model 学习什么信息和 retrieval 能力可以被 represent。在 embedding inference 和 deployment 阶段，sampling process 决定哪些 frame 和 spatial detail 实际被输入给 model。之后，retrieval system 搜索 candidate corpus 并返回少量相关 video。

第一个 challenge 是 representation。如果不同的 query format、domain 和 relevance condition 分别训练，一个 model 无法 balanced 地覆盖它们。这导致了 semantic scaling。

第二个 challenge 是 observation。即使 representation 很强，如果相关 frame 没有被 sample 到，或者保留了太少的 spatial detail，也无法 recover 一个短暂的事件。这导致了 observational scaling。

第三个 challenge 是 search。即使 relevance signal 是准确的，在 billion-scale graph 中 traversal 仍然困难，在高并发下执行也很昂贵。这导致了 search scaling。

因此方法也遵循同样的顺序：建立 comprehensive representation，保留充分的 visual evidence，然后支持 deployable 的 large-corpus search。

## Slide 7 — What Each Scaling Stage Changes

每个 scaling stage 改变不同的对象，因此每个阶段有自己的核心难点和研究方向。

Semantic scaling 改变 query format、retrieval domain 和 relevance condition。核心难点是简单地增加 data 或更大的 model 并不能自动产生 balanced capability。研究方向是识别缺失的 ability，构建 targeted data，并 joint 地学习相关 task。

Observational scaling 改变提供给 encoder 的 frame 和 spatial token。有用的 setting 取决于 video length、query granularity 和 model architecture。研究方向是 controlled 的 test-time 和 training-time analysis，然后从 dense observation 迁移到 sparse observation。

Search scaling 改变 candidate-set size 和 serving concurrency。准确的 relevance 可能在 graph 上仍然难以 follow，很多 irregular scoring job 在 GPU 上效率低下。研究方向是 co-design relevance learning、graph traversal 和 GPU execution。

所以三个阶段是相互关联的，但不能用一种通用的 scaling 方法来解决。

意见：以 what is scaled 和 core difficulty 为主，Research direction 可以非常简单带过

## Slide 8 — Thesis Overview: Three Studies, One Connected Chain

这页在逐一介绍 study 之前先给出完整的 thesis chain。

Study 1 问的是：一个 embedding 能否覆盖 heterogeneous 的 query format、domain 和 relevance condition。它的回答是 unified evaluation、targeted data synthesis 和 curriculum-trained General Video Embedder。一旦有了这样的 representation，紧接着的问题就是：在有限的 input budget 下，model 能否真正 observe 到所需的 visual evidence。

Study 2 通过 controlled 的 test-time 和 training-time scaling analysis 回答了这个问题，然后将 knowledge 从 dense sampling 迁移到 sparse sampling。一旦 relevance signal 在 deployable 的 input budget 下仍然可靠，紧接着的问题就是：这个 signal 能否在 billion-scale corpus 上被搜索。

Study 3 co-design 了 metric learning、graph traversal 和 GPU execution，使学到的 relevance signal 在 web scale 下 searchable 且 executable。

因此这个连接不是推迟到 conclusion 才建立的。Study 1 使 Study 2 的问题成为可能，Study 2 使 Study 3 的问题成为可能。

意见：相比于上一页，这一页应该更侧重于我们每一个 study 解决的问题，并大概讲一下方法。
因为这一页是 overview，所以最重要的内容是：
1. 每个 study 的核心内容（即每一页究竟回答了什么问题）；
2. 每两个 study 之间的关系。

## Slide 9 — Study 1: Semantic Scaling

第一个 study 是关于 semantic scaling 的。一个 universal video retrieval model 应该具备哪些 capability，我们如何 scale 到这些 capability？

## Slide 10 — Review of the Problem and Existing Research

Universal video retrieval 需要覆盖 textual、visual 和 composed query，还需要处理 coarse-grained、fine-grained 和 long-context domain，包括 spatial、temporal 和 partially relevant evidence。

Research gap 不是把几个 model 聚合起来用一个 average score 掩盖弱点。更深层的问题是这些 capability 是分别发展的。不同的 task 使用分别准备或合成的 data，model 也是针对特定 task 或 domain 分别训练的。结果是这个领域仍然是 siloed 的，没有一个 model 能提供 comprehensive capability coverage。

这产生了两个 research hurdle。第一个是跨 domain 和 task 的 large-scale、quality-controlled data synthesis。第二个是 interconnected multi-task representation learning，因为相关 task 之间有 internal hierarchy，不应该被当作独立的。

我们的 research design 是先 diagnose capability gap，然后构建 unified targeted data，以 structured 的方式训练相关 task。

意见：这一页在讲的时候，Research gap 比 research hurdle 更为重要，所以我们要引出 Research gap 这条结论。前面要做好一些铺垫，这比较重要。我觉得这也是博士毕业论文在讲 research 时比较重要的部分。

## Slide 11 — Universal Video Retrieval Benchmark

为了让 capability gap 可见，我们将十六个现有 public dataset 组织在一个 Universal Video Retrieval Benchmark protocol 下，即 UVRB。

每个被评估的 model 使用完全相同的 preprocessing、frozen embedding、cosine similarity，且没有 task-specific fine-tuning。我们评估了来自 CLIP-based 和 multimodal language model 两个家族的十四个 model。

目的不只是产生一个 leaderboard average。UVRB 给每个 model 一个跨 query format、domain 和 relevance condition 的 capability profile。这些 profile 展示了反复出现的 weak axis，直接指导后续的 data synthesis 和 training design。

## Slide 12 — V-SynFlow: Three-Stage Data Synthesis

在 UVRB 识别出缺失的 capability 之后，V-SynFlow 通过三个阶段将 weakly annotated web video 转化为 targeted training data。

第一阶段是 multi-granular quality control。我们先纠正 non-descriptive 或不正确的 annotation，然后进行 semantic-level cross-modal consistency filtering 去除不匹配的 video-text pair，再用 visual 和 temporal check 去除 static 或低质量 sample。目标是在生成任何新信息之前建立一个可靠的 asset pool。

第二阶段是 multi-dimensional information enrichment。一个 large multimodal model 生成更丰富的 temporal、spatial 和 partially relevant 信息描述。我们不是把所有细节都放进每个 query，而是 sample 不同的 information profile，visual lens 可以从 frame 到 clip 到完整 video。这产生了多样的 basic text-video pair。

第三阶段是 multimodal task extension。从 basic text-video pair 出发，我们构建了 text-image composed video retrieval、text-video composed video retrieval、text retrieval 和 text-image retrieval data。这些 auxiliary task 扩展了 training mixture，覆盖了更多 retrieval ability。

关键不是简单地增加 synthetic data，每个阶段都围绕 UVRB 诊断出的 capability gap 来设计。

意见：在讲的过程中，需要有意无意地说明以下两点：
1. 强调填补缺陷：说明通过前面 UBRB 的 benchmark 全面分析，我们发现了一些缺陷，因此在合成过程中，其实是要去填补这些缺陷的。
2. 说明数据用途：说明这些数据最终都要捏合在一起进行训练。可能不需要具体说明后面是怎么训练的，只需表示这些都会作为训练数据即可。

## Slide 13 — UVRD: Scale and Capability Coverage

这页总结了 V-SynFlow 的产出。

第一部分是 scale 和 validation。UVRD 包含 155 万 synthesized pair。加上 public data，完整的 training mixture 对 GVE-3B 包含 1255 万 instance，对 GVE-7B 包含 1373 万 instance。Human audit 在 100 个 sample 中发现 95 个正确。

第二部分是 capability coverage。Data 包括 textual、visual 和 composed query，覆盖 coarse-grained、fine-grained 和 long-context domain，包含 spatial、temporal 和 partially relevant sub-domain。

这个 workload 重要是因为 dataset 不仅大，它是按照前面定义的 capability taxonomy 来组织的。

意见：这一页要讲的内容让我更加精简和轻松一点。因为它只是一个结果的展示而已，不是特别重要，往后才更重要。

## Slide 14 — General Video Embedder: Architecture and Objective

这张图展示了 General Video Embedder，即 GVE。

GVE 基于 Qwen2.5-VL 进行 retrieval 适配。Text、image、video 和 composed query 由一个 multimodal backbone 处理，映射到一个 shared embedding space。Last-token representation 被 normalize 后用于 retrieval。

Training 使用 symmetric InfoNCE。匹配的 query-target pair 被拉近，不匹配的 example 和 mined hard negative 被推远。Loss 在 query-to-target 和 target-to-query 两个方向上都施加。

Infrastructure 支持 large-scale heterogeneous training，但 research point 是 shared representation。一个 model 被训练来覆盖 UVRB 诊断出的、UVRD 提供的 retrieval capability。

## Slide 15 — Modality Pyramid: Alignment-Aware Curriculum

剩下的问题是如何 joint 地训练这些 heterogeneous task。Random mixing 可能导致 modality interference。简单的 spatial-alignment task 可能在 training 早期占主导，而 temporal 和 composed task 仍然不稳定。

Modality Pyramid 给出了一个直观的解决方案。Model 从 better-aligned、更 foundational 的 task 开始，然后逐步扩展到更难的、更 composite 的 task。

在每个 epoch 开始时，一个 prober 对每个 task 测量一千个 positive pair 的 current alignment。最新的 GVE checkpoint 成为下一个 prober，因此 curriculum 随 model 一起变化，而不是遵循固定顺序。

Temperature 从 0.1 到 1.0 控制这个 ordering 的强度。开始时，低值强烈偏好当前 well-aligned 的 task，给 model 一个稳定的起步。后期偏好变得更平，harder task 被更频繁地 sample。

核心 insight 是 adaptive foundational-to-composite learning。两个端点值只是逐渐弱化初始 ordering 的 mechanism。

意见：还是要抓住核心。这些公式其实都还不是最重要的，第一、第二步都只是实现的细节而已。
我觉得这个方法的核心在于：
1. 我们哪来的这个估计分数？这个分数到底是什么意义？为什么我们能分出哪些任务简单，哪些任务难？
2. 为什么我们会去做这样的迁移？实际上，这些更简单、更容易、更基础的任务，它们的知识更好学，并且对下游这些更难、更复杂的任务具有迁移能力。这也是我们在实验里面发现的，这些可以口头上说。

## Slide 16 — Experiments: Capability Analysis on UVRB

这页给出 UVRB 上的整体 experimental readout。

首先，GVE-7B 在 dataset-level 和 ability-level radar plot 上都覆盖了最大面积，展示了在多个 dataset、query format 和 capability dimension 上的 strong and balanced performance。

其次，这些 plot 揭示了被评估 model 中反复出现的 weak capability。Temporal、composed 和 partially relevant retrieval 仍然困难，即使 model 在熟悉的 benchmark 上表现良好。

第三，这提供了 systematic assessment。UVRB 不只是说哪个 model 更好，它展示了 community 在哪些地方仍有 capability gap，哪里需要 targeted supervision。

所以这页同时展示了 model result 和 evaluation 的 diagnostic value。

意见：这页可以简单一点，大概说一下就行：我们的模型在几乎所有的数据集和所有的能力上都达到了最优，除了 Composer 和 Visual 还有提升的空间。这个我们后面也会再讨论。

## Slide 17 — Zero-Shot Retrieval Results on UVRB

这张表比较了相同 UVRB protocol 下的 zero-shot retrieval。

主要结果是 GVE-7B 在十六个 dataset 上的 average 最高，在被评估的 ability 上的 average 也最高。相对于 Unite-7B，两个 headline gain 分别约为 6.5% 和 7.3%。

还有一个重要的 model-size comparison。GVE-3B 已经超过了更大的 Unite-7B baseline。这意味着在这个比较中，targeted data 和 task-aware curriculum 可以弥补 model size 的差距。

结论不是每个 individual task 都被解决了。结论是一个 shared model 在广泛的 UVRB setting 下实现了更强、更 balanced 的 zero-shot generalization。

## Slide 18 — Ability-Level Retrieval Results

这张表将整体结果分解到 individual ability。

最大的 gain 出现在 composed、long-context 和 temporal retrieval 上。这些是 UVRB 识别出的重要 weakness，因此 improvement 与 research design 一致，而不是均匀分布的。

Boundary 也很清楚。Visual-only retrieval 几乎持平，compact CLIP encoder 仍然难以超越。GVE 改善了 targeted weak capability，但一个 model 不会自动 dominate 每个 retrieval setting。

意见：这一页和前两页都是差不多的，可以快速讲一下，把篇幅留给后面的页。

## Slide 19 — Ablation: UVRD and Modality Pyramid

Ablation 分离了 targeted data 和 structured task ordering 的作用。

加入 UVRD 在 composed retrieval 上带来主要 gain，也提升了 dataset average。再加入 Modality Pyramid 进一步提升了 average。

这两部分解决不同的问题。UVRD 为缺失的 capability 提供 supervision，Modality Pyramid 在 heterogeneous task 联合训练时减少 interference。它们的 complementary gain 支持了完整的 GVE design。

## Slide 20 — Capability Correlations Motivate the Design Choice

这个 correlation analysis 很重要，因为它解释了 capability axis 代表什么。

Partially relevant retrieval 是 overall UVR capability 最强的 proxy，correlation 约为 0.97。它与跨多个 dataset 的 performance 高度相关，因此比依赖一个传统 benchmark（如 MSR-VTT）更有代表性。如果这个 capability 强，我们可以获得一个有用的 indication 表明 model 更广泛的 retrieval ability 也强，虽然 correlation 不能证明 causality。

Spatial 和 temporal ability 的 correlation 很弱，只有约 0.12。这意味着 model 可能学到了详细的 visual information 但没有学到 temporal evidence，或者反过来。仅靠 model scale 很难同时 combine 好这两种 ability。

Visual-only comparison 给出了相关的 lesson。一个 compact CLIP4Clip model 可以超过大得多的 multimodal model。Fine visual detail 和 broad semantic understanding 不会自动在一个 representation 中同时学到。

这些比较支持 capability-specific diagnosis 和 targeted supervision，而不是一个 coarse benchmark 或一个 large model。

意见：这里应该再从原文里面摘一些比较合理的内容，多讨论一下。
现在的讨论还可以，但是你光说这些结论，对于非这个子领域问题的 researcher，或者在做一些应用时，到底最近有什么 insight，或者同领域做有什么 insight，还不够清晰。
我觉得这边可以讲得更加通俗易懂一点，让这些 committee 一下子就能听懂，也能 get 到这边有一些 research 的点。

## Slide 21 — Data Scaling Across UVRB Abilities

这页聚焦于主图中展示的两条 average scaling curve。

随着 training pair 数量增加，dataset average 和 ability average 在评估范围内呈近似 log-linear 上升。GVE-3B 的 average slope 更陡，而 GVE-7B 从更高的水平开始并持续改善。

主要 message 是 targeted data scaling 提升了 overall retrieval capability，但速率取决于 model size。Individual ability 的详细 scaling behavior 是 supporting evidence，这里不需要逐一解读。

意见：没必要说什么“Individual ability 的详细 scaling behavior 是 supporting evidence，这里不需要逐一解读。“，占用我时间，其他页也是

## Slide 22 — Study 1 Summary: From Evaluation to GVE

让我回到 universal video retrieval 来总结 Study 1。

UVR 意味着跨 query format、data domain 和 relevance condition 的 systematic capability coverage。之前的 research gap 是这些 capability 被分别处理。Data 为 isolated task 准备，model 为 isolated setting 训练，evaluation 也是 fragmented 的。

我们的 solution 遵循一条有序的研究链。UVRB 先 unify evaluation 并识别 weak capability。V-SynFlow 然后生成 quality-controlled、gap-targeted supervision。Modality Pyramid 利用 task 之间的 hierarchy 从 foundational 到 harder capability 训练。GVE 是最终的 cross-domain、multi-task video embedder。

因此 contribution 不是一个 benchmark、一个 dataset 或一个更大的 model，而是一个 capability-driven 的过程，连接了 evaluation、data、training 和最终的 representation。

这个结果立刻产生了下一个问题。即使 representation 能覆盖所需的 meaning，当 long video 只用有限数量的 frame 和 visual token 来表示时，它能否 retrieve 到那个 meaning？这就是从 semantic scaling 到 observational scaling 的连接。

## Slide 23 — Study 2: Observational Scaling

第二个 study 从 Study 1 提出的问题出发。一个 representation 可能具备正确的 capability，但它只能使用进入 encoder 的 evidence。

Observational scaling 因此问的是：当 input budget 有限时，哪些 visual evidence 必须被 observe 到。我会先介绍一个 controlled multi-granular long-video benchmark，然后分析 test-time 和 training-time scaling，最后通过 dense-to-sparse transfer 应用发现的 asymmetry。

意见：简单一点

## Slide 24 — Observational Scaling: Sampling Defines What Can Be Seen

MG-LVR 中 video 的平均时长约 706 秒，而 query-relevant evidence 可能只持续几秒。

Frame count 控制 temporal coverage。每个 frame 保留的 token 控制 spatial detail。如果相关时刻没有被 sample 到，representation 之后无法 recover 它。如果每个 frame 被压缩得太厉害，重要的 local detail 也可能消失。

现有 benchmark 通常只提供 long video 或 multi-granular query 中的一个，不在一个 controlled setting 中同时提供两者。我们需要两个 dimension 来 isolate sampling 如何改变 embedding model 实际能看到的内容。

## Slide 25 — Temporal Granularity and Continuity

这页定义了两个不同的 property。

Temporal granularity 衡量一个 video 中有多少比例与一个 query 相关。Fine-grained query 描述一个短暂时刻，relevant ratio 在 0.001 到 0.01 之间。Medium-grained query 覆盖中等比例，在 0.1 到 0.3 之间。Coarse-grained query 描述 broad video-level content。我们对每个 query-video pair 计算这个 ratio 并用它来划分三组。

Temporal continuity 描述相关 evidence 如何分布。值为 1 表示一个 continuous event，更小的值表示 evidence 分散在多个 interval 中。

Granularity 和 continuity 不应混淆。Granularity 描述有多少 evidence 是相关的，continuity 描述这些 evidence 是 contiguous 的还是 distributed 的。

意见：不用描述那么细节，大概说一下就行。说明有一些比较少，有些比较多：
1. 比较少的：举例说明大概是 0.01 左右。
2. 比较多的：其他的密的话可能是 0.3 左右，剩下的比较多的就是 cos。
这一页就说得简单一些，不用太复杂，都提一下就行。

## Slide 26 — Multi-Granular Long Video Retrieval Benchmark

MG-LVR 使 sampling problem 变得可测量。

它包含 4844 个 long video 和 9971 个 fine、medium、coarse granularity 的 query。平均 video 时长约 706 秒。我们评估了来自 CLIP-based 和 multimodal language model 两个家族的二十三个 model。

Human audit 在 50 个 pair 中发现 48 个正确。Contribution 是一个 controlled testbed，结合了 long duration、query granularity、temporal continuity 和 sampling density，用于 large cross-model analysis。

## Slide 27 — How MG-LVR Controls Query Granularity

这张图展示了 construction pipeline，但最重要的 challenge 是一个 long video 内部的重复信息。

如果相同的事件或 semantic content 出现在多个 clip 中，我们不能把每个重复的 clip 都当作新 evidence。否则 relevant duration 和 query granularity 就变得 ambiguous。

我们先对 video 进行 split 和 caption，embed clip caption 并构建 Clip Relation Graph。近乎 isolated 的 node 代表 unique single-clip information。Louvain community detection 将 semantically related 的 clip 分组为 unique multi-clip unit，即使它们出现在不同的 timestamp。

对每个 unique unit，我们生成一个 natural-language query，然后计算其 relevant-duration ratio，分配 fine、medium 或 coarse granularity，并去除与 non-target clip 在 semantic 上冲突的 query。

核心逻辑是：先找到 distinct information，再测量其 coverage，最后才分配 granularity label。

## Slide 28 — Granularity Gap Under Sparse Sampling

这是主要的 benchmark finding。

在 sparse 8-frame sampling 下，coarse-grained retrieval 保持强劲，而 fine-grained retrieval 低得多。将 frame count 增加 16 倍只带来 modest 的 fine-grained improvement。

结论是仅增加 test-time frame 不能消除 granularity gap。Architecture 和 learned representation 还必须知道如何使用 additional evidence。这 motivates 了更 systematic 的 scaling analysis。

## Slide 29 — Test-Time and Training-Time Scaling Analysis

MG-LVR 支持跨多个 model 和 sampling setting 的两种 complementary analysis。

Test-time scaling 改变 inference 时 observe 到的 evidence。我们变化每个 frame 保留的 spatial token、sampled frame 数量，以及在固定 visual-token budget 下的 frame 分配方式。

Training-time scaling 改变 learned representation。我们在不同的 spatial 和 temporal density 下 post-train 相同 architecture，然后在 matched 和 mismatched input setting 下评估。

使用相同的 fine、medium、coarse benchmark 分离了 inference-time evidence effect 和 training-time representation effect。后续 slide 聚焦于 supported insight，而不是逐一读每个数字。

## Slide 30 — Test-Time Scaling: Spatial Density

首先，我们研究 test-time spatial density，frame count 固定为 32。

增加每个 frame 的 spatial token 并不产生 universal monotonic gain。有些 architecture 受益，有些 saturate。Response 在 fine、medium、coarse query 之间也不同。

Insight 是更多 spatial detail 不自动更好。它的价值取决于 model architecture 和 query granularity。

## Slide 31 — Test-Time Scaling: Temporal Density

接下来，我们变化 test-time frame count。

Multimodal language model 在更 dense 的 temporal sampling 下可以继续改善，特别是对依赖短暂时刻的 fine-grained query。CLIP-based model 通常更早 plateau，甚至在很多 frame embedding 被 average 时可能 degrade。

Insight 是 fine-grained retrieval 需要 temporal coverage，但更多 frame 只在 architecture 能有效 integrate 它们时才有帮助。

## Slide 32 — Test-Time Scaling: Spatiotemporal Trade-Off

这页固定总 visual-token budget，改变 budget 在 frame 和 token per frame 之间的分配。

Coarse-grained query 通常偏好更少 frame 加更高 spatial resolution，因为 broad scene-level cue 占主导。Fine-grained query 偏好更多 frame，即使 spatial detail 更低，因为主要风险是错过短暂的目标时刻。

在相同 computational budget 下，最优 sampling strategy 取决于 query granularity。不存在适用于所有 query 的单一 spatial-temporal allocation。

## Slide 33 — Training-Time Scaling: Spatial Resolution Robustness

现在我们转向 training-time representation。

我们在不同 spatial token density 下 post-train 相同 architecture，并在相同 input setting 下测试每个 checkpoint。High-density spatial training 能很好地 transfer 到 lower-density inference。这就是 spatial resolution robustness。

Improvement 不是无限的。在 extreme density 下，overall gain 变得很小，某些 fine 或 coarse 结果可能略有下降。Spatial representation 跨 resolution transfer，但 very high density 有 diminishing return。

## Slide 34 — Training-Time Scaling: Temporal Frame-Count Anchoring

Training-time temporal scaling 表现不同。

我们用 4、8、16 或 32 个 frame 训练相同 architecture，然后测试 matched 和 mismatched frame count。Retrieval 通常在 training frame count 附近达到 peak。大的 mismatch 在两个方向上都降低 performance，特别是对 fine-grained query。

我们称之为 frame-count anchoring。Dense temporal training 不自动 transfer 到 sparse inference，即使 model architecture 不变。这个 asymmetry 直接 motivates 了下一页的 method。

## Slide 35 — VEterfall: Progressive Dense-to-Sparse Self-Distillation

VEterfall 不使用 separate 的 dense、medium、sparse model architecture。Dense、medium、sparse 描述的是同一个 base video embedder 的不同 sampling density。

首先，我们 freeze 一份 model，用 dense sampling 处理一组 video，产生更强的 teacher embedding。

然后，另一份相同 architecture 的 model 用 medium sampling 处理相同 video。它的 video embedding 被训练来 match dense embedding，通过 mean squared error。一个 auxiliary InfoNCE loss 保持 video-text alignment。

接着，medium-density checkpoint 成为 sparse-density model 的 frozen teacher，重复相同过程。

因此 model 在 sampling density 之间 supervise 自己。Dense observation 下可用的 knowledge 被逐步 transfer 到 sparse inference，而不改变 deployment architecture。

## Slide 36 — Progressive Transfer Across Three Sampling Densities

这张表比较了原始 model 和 progressive transfer 各阶段在三种 sampling density 下的表现。

Benefit 集中在困难的 fine- 和 medium-grained query 上。在 medium density 下，fine-grained retrieval 明显提升，coarse-grained retrieval 略有下降。在 sparse density 下，最终 checkpoint 带来更大的 fine-grained gain，同时 coarse retrieval 几乎不变。

这是一个 honest trade-off。当 broad scene semantics 已经很强时，post-training 可以将 capacity 重新分配到 sparse fine-grained evidence，在某些 density 下略微降低已经 saturated 的 coarse capability。

因此 VEterfall 对 sparse input 最有用，但它的 gain 不是在每个 query granularity 上都均匀。

## Slide 37 — Study 2 Summary: From Controlled Scaling to Sparse Transfer

Study 2 从一个目标开始：发现并应用 long-video retrieval 的 spatial-temporal scaling principle。

现有 benchmark 无法 jointly control long duration、query granularity、temporal continuity 和 sampling。MG-LVR 提供了这个 testbed。跨多个 model family 和 setting，analysis 揭示了 granularity-dependent test-time allocation、training-time spatial resolution robustness 和 temporal frame-count anchoring。

Frame-count anchoring 解释了为什么 sparse inference 仍然困难。对于同一个 base model，dense sampling 可以产生更好的 embedding，但那个 knowledge 不自动 transfer 到 lower-density input。

VEterfall 应用了这个发现的 scaling principle。它用 model 的 dense-input embedding 来 supervise progressively sparser configuration，experiment 证实了这种 transfer 在 sparse regime 下有效。

这个结果立刻产生了下一个问题。一旦在 deployable observation budget 下有了有用的 relevance signal，我们如何在 billion-scale catalog 上 preserve 并 execute 这个 signal？这就是从 observational scaling 到 search scaling 的连接。

## Slide 38 — Study 3: Search Scaling for Web-Scale Retrieval

第三个 study 从 Study 2 提出的问题出发。如果 system 无法在非常大的 catalog 上搜索，一个有用的 relevance signal 是不够的。

Search scaling 问的是 learned relevance 能否在 graph 上被 traversal 并在高并发下高效执行。我会介绍 retrieval setting、三个 challenge、GMP-GR method，以及 offline 和 online evidence。

意见：所有这种过渡页都更加简练一点

## Slide 39 — Web-Scale Video Retrieval: From Catalog to Candidates

Retrieval 在 ranking 之前缩小 billion-scale video catalog。

给定 user 或 user-item query，目标是在不 scoring 整个 catalog 的情况下返回 learned relevance 最高的 top-K item。Approximate nearest neighbor search 在 graph 上移动，只对 promising candidate 进行 scoring。

Relevance model、graph path 和 online execution system 必须协同工作。下一页分开讲三个 challenge。

意见：我们前面已经定义了什么是 retrieval，他们已经知道这就是在找相似的 items。但是，我们这边要强调的是“大规模”这件事。

retrieval 在推荐系统里面的一大意义，就是我们要快速地缩小候选集，给后面的 ranking 提供缩小后的集合，这是它的一个很大作用。

这样做是为了给后面加速，但本质上，为了加速而做的步骤本身也不能太慢，同时又要保证准确。因为我们的集合一旦筛选得不好，那后面 ranking 怎么做也做不好了。

所以你可以再考虑一下，这一页要精炼，但是一定要抓住这个重点去讲。

## Slide 40 — Three Challenges in Web-Scale Graph Retrieval

第一个 challenge 是 unified multi-relational relevance。相关 behavior，如 click、view、browse，应该 joint 建模，而不是使用 separate relevance model。

第二个 challenge 是 efficient billion-scale graph search。一个 strong learned score 可能仍然产生 poor local path，因此 search 必须 balance depth、breadth 和 candidate reuse。

第三个 challenge 是 irregular、high-concurrency GPU computation。很多 concurrent query 产生 small 且 irregular scoring job，频繁的 GPU launch 变得昂贵。

因此 research problem 是在一个 retrieval framework 中 co-design relevance learning、graph traversal 和 GPU execution。

意见：就这一页，在写 challenge 的时候，尽量精简，并且要把好处写出来。

虽然我觉得现在稍微有一点精简，但我们在讲的时候，至少可以回顾一下论文原文，讲得稍微详细一点。我觉得这还是比较重要的，这一页还是值得多花一点篇幅去讲。

## Slide 41 — GMP-GR: Offline Training and Online Search

GMP-GR 按从左到右的阅读顺序。

Offline，MUIRML 从多种 user behavior 中学习一个 relevance metric。它还引入一个 search-oriented ordering signal，使 learned relevance 在 graph navigation 时更容易使用。

Online，C-HiPANNS 在一个 query 内通过使用多个 connected search path 和 shared candidate 来 broaden exploration。Q-HiPANNS 然后跨 concurrent query 聚合 scoring job，形成 GPU-friendly batch。

关键 design 是从 training 到 serving 的 continuity。同一个 learned relevance signal 用于 offline modeling、graph traversal 和 online GPU execution。

## Slide 42 — MUIRML: Accurate Relevance That Remains Searchable

MUIRML 先用一个 model 学习相关 user behavior。它预测 click、browse 等 behavior 的 interaction vector，然后用 attention 将这些 signal 组合成一个 relevance score。

Self-Covariant Loss（SCL）添加了一个 soft ordering regularizer。它鼓励 graph-friendly 的 relative order，同时保留 prediction objective。

目的不是声称 formal metric guarantee。Novelty 是 joint 地学习 multi-relational relevance 和 search-oriented ordering signal，使 model 在 graph navigation 时仍然有用。

## Slide 43 — HiPANNS: Two Levels of Parallel Search

HiPANNS 使用两层 connected parallelism。

C-HiPANNS 在一个 query 内工作。几个 seeded search 共享 candidate 并 broaden graph exploration，降低了只 follow 一条 poor local path 的风险。

Q-HiPANNS 跨 query 工作。它从 concurrent search 中收集 small scoring job，形成 bounded batch，发送给 GPU。

一个 component 改善 exploration quality，另一个改善 execution efficiency。两者一起使 learned relevance 在 web-scale retrieval 中更实用。

## Slide 44 — Web-Scale Video Deployment and System Optimization

Deployment system 将 retrieval framework 与几项 engineering optimization 结合。

Compilation 简化 serving graph 并提升 throughput。Quantization 将 model 从 32-bit 降到 16-bit，产生额外的 throughput gain。Streaming update 保持 user 和 video-item embedding 的时效性。

该 framework 在超过二十个 Baidu 应用中报告。这些结果支持 deployment feasibility，而 exact throughput 和 latency 仍取决于 hardware 和 serving environment。

## Slide 45 — Offline Retrieval Effectiveness and Efficiency

Offline evaluation 使用四个 real-world video dataset，测量 coverage、recall 和 time cost。

GMP-GR 在所有四个 dataset 上改善了 coverage，在被测方法中给出了 favorable coverage 和 time-cost trade-off。它还提升了 video dataset 上的 Recall@10。

详细数值在 slide 上。主要结论是 jointly designed 的 relevance 和 search framework 在不牺牲 practical efficiency 的情况下提升了 retrieval quality。

## Slide 46 — Online A/B Evaluation

Online A/B evaluation 覆盖两个 production video service。

两个 service 都展示了正向的 time-on-page 和 daily-active-user 结果。Component analysis 也分别报告了 MUIRML 和 HiPANNS 的贡献。

这支持了完整 framework 在报告的 production configuration 下的价值。Evidence boundary 是 controlled A/B table 覆盖两个 service，而更广泛的 system 在超过二十个应用中报告。

## Slide 47 — Study 3 Summary: Co-Design Keeps Learned Relevance Searchable

Study 3 从三个 coupled challenge 开始：unified multi-relational relevance、efficient graph traversal 和 irregular high-concurrency GPU execution。

MUIRML 学习一个 multi-relational relevance signal，SCL 使其 relative order 对 graph navigation 更有用。C-HiPANNS 在一个 query 内 broaden search，Q-HiPANNS 跨 query batch irregular GPU work。System optimization 然后支持 production deployment。

Novelty 不是一个 isolated accuracy improvement 或一个 faster kernel，而是 relevance signal、traversal process 和 execution system 的 co-design。

核心 insight 是 retrieval accuracy 单独不够。Learned signal 必须在 web scale 下保持 searchable 和 executable。

意见：可以参考一下其他页的一些意见，然后再润色优化一下。

## Slide 48 — Conclusion and Future Work

现在让我回到 guiding question，总结三个 connected study。

Conclusion 分三部分。首先，我展示三个阶段如何相互依赖。其次，我总结什么被 scaled 以及什么 evidence 支持每个 claim。第三，我讨论 future direction 和主要 limitation。

## Slide 49 — One Thesis, Three Connected Retrieval Constraints

三个 study 按顺序保护了三个 requirement。

Semantic scaling 问什么可以在不同 retrieval setting 下被 represent。Observational scaling 问在有限 frame 和 spatial token 下什么 evidence 实际被看到。Search scaling 问 relevance signal 能否通过 graph traversal 和 high-concurrency serving 被 preserve。

这个顺序很重要。一个 searchable system 仍然需要可靠的 relevance signal，一个可靠的 representation 仍然需要相关的 visual evidence。三个 study 一起形成了从 representation 经 observation 到 large-corpus search 的一条路径。

## Slide 50 — What Scaled, What Generalized, and What Evidence Supports It

这张表总结了三个阶段的 evidence。

Study 1 在十六个 public dataset 上测试了 query format、domain 和 relevance condition。Study 2 在三种 query granularity 和多个 model 上测试了 frame 和 token density。Study 3 通过 offline dataset 和报告的 production service 测试了 large catalog。

Generalizability 在每个阶段有不同的 operational test。Semantic capability 跨 task 和 domain 测试。Observational capability 跨 sampling density 测试。Search capability 跨 dataset 和 online service 测试。

意见：这里的 evidence 我其实是可以理解的，但是这一页的感觉重点还是不是很清楚，到底要讲什么？是要讲我们的方法、evaluation，还是 evidence boundary 这个东西？我自己都不是很理解，你讲讲 evidence boundary 是什么意思？我觉得在讲义上说明得也不是特别清楚。另外，这一页要和第 49 页、第 51 页区分开。这三页（49、50、51 页）要有自己独立且重要的分享点。

## Slide 51 — Why This Thesis Matters for Video Retrieval

本 thesis 为 scalable and generalizable video retrieval 提供了一条研究路径。

它将 capability coverage、limited visual observation 和 large-corpus search 分开，然后给每个 bottleneck 匹配了 benchmark、analysis、method 和 evidence。

Video retrieval 是一个有用的 real-world setting，因为 query 多样、relevant evidence 可能很短暂、corpus 持续增长。这些 property 也将 thesis 连接到 multimodal foundation model、long-term agent memory 和不断变化的 data。

意见：这一页标题也不是很好，定位也不是很清晰。我希望你在第 49、50、51 页能有明确的想法，到底他们要做什么、要说什么，感觉没有重点。如果你实在觉得这些内容都挺散的，那是不是可以压缩到两页来讲呢？

## Slide 52 — Future Direction I: Retrieval-Native Multimodal Foundation Models

第一个方向是让 retrieval 成为 multimodal foundation model 的 native ability。当前 model 主要学习 generation，retrieval 通常是后来添加的。

未来的 model 可以使用 retrieval token、routing mechanism 或 lightweight adapter，同时保留 generation。Open question 是如何产生 compact retrieval state 而不损害 model 的 generative ability。因此 retrieval 和 generation 应该 joint 评估。

## Slide 53 — Future Direction II: Video Retrieval as Long-Term Agent Memory

第二个方向是 agent 的 long-term visual memory。

Agent 可能需要找到某个 object 最后一次出现的位置，或从很多小时的 video 中 retrieve 一个 rare event。Semantic scaling 支持不同的 memory query。Observational scaling 决定什么进入 memory。Search scaling 在不断增长的 memory index 下保持 latency constraint 内的可用性。

Future evaluation 应该包括 task success、decision time 和 sparse event 的 recall。

## Slide 54 — Future Direction III: Self-Evolving Data, Evaluation, and Curriculum

第三个方向是一个 closed data 和 training loop。

Evaluation 先识别新的 capability gap。Synthesis system 创建 targeted example。Curriculum scheduling 更新 model，improved model 再次被评估。

目标是当 query format、video domain 和 relevance condition 变化时能够 adapt。一个重要的 open problem 是 retention。Model 应该在修复新 gap 的同时不忘记已经学到的 capability。

## Slide 55 — Limitations and Open Questions

有三个主要 limitation。

第一，三个 study isolate 了 separate stage，而不是 end-to-end 优化完整 pipeline。第二，UVRD 和 MG-LVR 部分依赖 synthesized 或 caption-based signal，因此更广泛的 human 和 natural-data validation 仍然必要。第三，GMP-GR 在一个 industrial stack 中验证，absolute throughput 和 latency 取决于 hardware、traffic 和 serving design。

这些 boundary 定义了 end-to-end integration、更强 supervision 和 cross-system transfer 的具体 next step。

## Slide 56 — Acknowledgements

在结束之前，我想表达我衷心的感谢。

我深深感谢我的导师 Prof. Xiaowen Chu 和 Prof. Renjing Xu，感谢他们的信任、指导、耐心和支持。我也感谢我的前任导师 Prof. Hao Liu，帮助我建立了严谨的研究基础。

我真诚感谢所有合作者、labmate 和 industry partner 的想法、辛勤工作和友谊。

我特别感谢我的答辩委员会的每一位成员。感谢你们仔细阅读我的工作、提出深思熟虑的问题，以及帮助我更清晰地理解这篇 thesis 的指导。

我感谢我的父母、我的妹妹、我的家人和朋友一直以来的支持。

最后，我感谢 AI Thrust 和 HKUST(GZ) 的行政人员，特别是 AS 的 Claire Ying Luo 老师，耐心细致的支持。

## Slide 57 — First-Author Publications

这页先列出直接对应 thesis 三个主要 study 的三篇 publication。

第一篇是 ACM Multimedia 2026 关于 universal video retrieval 和 GVE 的 paper。第二篇是关于 spatial-temporal scaling law 和 VEterfall 的 arXiv paper。第三篇是 Web Conference 2026 关于 GPU-accelerated multi-relational graph retrieval 的 paper。

其余六篇 first-author work 涵盖 federated graph learning、labor-market modeling 和相关 graph-learning 问题。我将它们放在三篇 thesis publication 之后，以展示更广泛的研究路径和博士期间完成的工作。

## Slide 58 — Questions

我的报告到此结束。再次感谢各位的时间、仔细审阅和宝贵指导。欢迎各位提问和建议。

## Slide 59 — Appendix

Appendix 包含详细的 protocol、supplementary result、deployment evidence 和准备好的 committee question。我仅在问题需要更多细节时使用。

## Slide 60 — UVRB Protocol and Selected Ability Results

这个 backup slide 给出了 common UVRB evaluation protocol 和 representative model 的 selected ability-level result。

## Slide 61 — UVRB Capability Radar and Correlation Findings

这个 backup slide 展示了 task-level radar view 和支持 capability-targeted data design 的主要 correlation finding。

## Slide 62 — MG-LVR Benchmark Context and 128-Frame Results

这个 backup slide 给出了 MG-LVR benchmark context，并展示了即使在 128 frame 下 fine-grained 和 coarse-grained gap 仍然可见。

## Slide 63 — VEterfall Frame-Efficiency and Token-Efficiency

这个 backup slide 比较了 frame 和 token efficiency，展示了 dense-to-sparse transfer 在哪里帮助最大，以及 coarse retrieval 在哪里保持稳定。

## Slide 64 — MG-LVR Error Analysis

这个 backup slide 将 missing temporal evidence 与 incomplete semantic-constraint matching 分开，因此不是每个 fine-grained error 都归因于 sampling。

## Slide 65 — GMP-GR Full Offline Results and Ablation

这个 backup slide 包含完整的 offline result，并展示了去掉 MUIRML 或 HiPANNS 中任何一个都会降低报告的 metric。

## Slide 66 — Production Traffic and Latency Evidence

这个 backup slide 展示了 anonymized production traffic 和 latency trace。它支持在 observed workload 下的 deployment feasibility，但不保证在另一个 platform 上的相同行为。

## Slide 67 — Prepared Committee Questions

最后一个 backup slide 记录了对六个可能问题的简短回答，涉及 model choice、audit size、benchmark validity、method composition、SCL 和 deployment transfer。
