# Thesis Defense Speaker Notes — V2

This script corresponds to `thesis-slides-v2.pptx`. It is based on the author-edited V1.3 deck, the coordinated V1.4 revision, and the latest related-work review.

Target delivery: 40–50 minutes, including short pauses and slide changes. Use the slide as the main prompt. The first sentence of each paragraph is a restart point.

## Slide 1 — Towards Scalable and Generalizable Video Retrieval

Good morning, professors, committee members, colleagues, and friends. My name is Zhuoning Guo. Thank you very much for attending my PhD thesis defense.

I am deeply grateful to my advisors, Prof. Xiaowen Chu and Prof. Renjing Xu. I am also honored to have Prof. Pan Hui, Prof. Jeffrey Xu Yu, Prof. Yutao Yue, Prof. Xuming Hu, and Prof. Meishan Zhang on my committee. Thank you for your time and valuable guidance.

My thesis is titled “Towards Scalable and Generalizable Video Retrieval.” It studies how retrieval should change when queries become more diverse, videos become longer, and candidate collections become much larger.

I also thank the administrative staff of AI Thrust and HKUST(GZ), especially Ms. Claire Ying Luo from AS, for helping organize today’s defense.

## Slide 2 — Thesis Roadmap

This is the roadmap. I will first introduce the overall problem. Then I will present three connected studies: semantic scaling, observational scaling, and search scaling. I will finish by connecting their contributions and discussing future directions and limitations.

## Slide 3 — Guiding Question

Video retrieval has moved beyond matching a short text query with a short video clip. Queries are more diverse, videos are longer, and candidate collections are much larger.

This leads to one guiding question: how should retrieval methods change as query diversity, video length, and corpus size grow?

These changes create bottlenecks in representation, visual observation, and large-corpus search. Each study addresses one bottleneck and leads to the next.

## Slide 4 — Applications of Video Retrieval in Modern Multimedia Systems

Video retrieval identifies relevant videos from a candidate collection. It supports three important applications.

For search, a user may provide text, an image, a video clip, or a composed query. The system must find the right videos in a very large corpus.

For recommendation, retrieval first reduces a huge catalog to a manageable candidate set. A ranking model then produces the final list. If retrieval misses a relevant item, ranking cannot recover it.

For data processing, retrieval can filter, clean, and organize multimodal data for model training. It helps find useful samples and remove poor or repeated matches.

Across these applications, queries are more diverse, videos contain denser information, and collections are too large for full scoring. These changes motivate the three studies.

## Slide 5 — Problem Formulation: Embedding-Based Video Retrieval

This slide defines embedding-based video retrieval.

First, an encoder maps the query and candidate videos into one shared embedding space. Candidate videos can be encoded offline.

Second, we compare the embeddings with cosine similarity. Training makes a relevant query-video pair score higher than an irrelevant pair.

Finally, we sort the candidates and return the top-K results. These three steps create the scaling problems in this thesis.

## Slide 6 — Why Video Retrieval Scales in Three Connected Steps

This slide connects the retrieval pipeline with the three studies.

During embedding training, the data, tasks, and objective decide what the model can represent. This is semantic scaling.

During inference, a long video is reduced to limited frames and spatial tokens. Sampling decides which visual evidence enters the model. This is observational scaling.

After embeddings are produced, the system must search a huge corpus without scoring every item. The relevance signal must support efficient graph search and online execution. This is search scaling.

The studies follow this order: learn broad meaning, preserve useful evidence, and search the learned relevance at scale.

## Slide 7 — What Each Scaling Stage Changes

Each scaling stage changes a different object.

Semantic scaling changes query formats, domains, and relevance conditions. The difficulty is balanced capability coverage. A larger model does not automatically fill every gap.

Observational scaling changes the frames and spatial tokens given to the encoder. The difficulty is allocating limited visual evidence.

Search scaling changes corpus size and serving concurrency. The difficulty is following an accurate score on a graph and computing it efficiently.

The response is stage-specific: targeted capability learning, controlled sampling analysis, and co-designed graph retrieval.

## Slide 8 — Thesis Overview: Three Studies, One Connected Chain

This page gives the complete research chain.

Study 1 asks how one embedding model can cover different query formats, domains, and relevance conditions. We diagnose capability gaps, synthesize targeted data, and train GVE with an adaptive curriculum.

The first result motivates Study 2. A model can use only the visual evidence that enters its encoder. We build MG-LVR, analyze frame and token scaling, and transfer dense-input knowledge to sparse inputs with VEterfall.

The second result motivates Study 3. The useful relevance signal must be searched over a very large catalog. GMP-GR co-designs relevance learning, graph traversal, and GPU execution.

The logic is direct: representation defines the signal, observation decides whether the evidence enters that signal, and search decides whether the signal remains usable at scale.

## Slide 9 — Study 1: Semantic Scaling

Study 1 focuses on semantic scaling. It asks what capabilities a universal video retrieval model should have, and how one model can learn these capabilities together.

## Slide 10 — Universal Video Retrieval Remains Fragmented

Universal video retrieval covers textual, visual, and composed queries. It also covers coarse, fine-grained, and long-context domains, including spatial, temporal, and partially relevant information.

The core challenge is fragmentation. Tasks use separately prepared data, models are trained for separate tasks or domains, and evaluation is divided across isolated benchmarks. The field lacks one model with broad capability coverage.

This creates two research hurdles: quality-controlled data synthesis across tasks and connected multi-task learning. Foundational and complex tasks are related, not independent.

This motivates our method: diagnose the gaps first, build targeted data for those gaps, and learn related tasks in a structured curriculum.

## Slide R1 — Related Work: Progress Without Unified Capability Coverage

Before introducing UVRB, I will briefly review two related directions.

First, video retrieval benchmarks have become more diverse. Some focus on spatiotemporal grounding, scene understanding, camera motion, composed queries, or visual queries. These benchmarks are useful, but each one usually measures a specialized setting.

Second, video embedding models have moved from CLIP-based temporal extensions to MLLM-based embedders. CLIP4Clip and InternVideo2 improve temporal modeling. LLaVE, UNITE, and VLM2Vec-V2 provide stronger language understanding.

The problem is not a lack of progress. The problem is fragmentation. Training data, models, and evaluation are still separated by task or domain. We therefore need a unified diagnosis before deciding what data to synthesize and how to train one shared model.

[Sources]

- `chapters/03-universal-video-retrieval.tex`, Related Works.

## Slide 11 — Universal Video Retrieval Benchmark

UVRB first makes the capability gaps visible. It organizes sixteen public datasets under one protocol.

All fourteen models use the same preprocessing, frozen embeddings, cosine similarity, and no task-specific fine-tuning.

UVRB gives each model a profile across query formats, domains, and relevance conditions. This profile shows which abilities are missing and guides the data and training design.

## Slide 12 — V-SynFlow: Three-Stage Data Synthesis

After UVRB identifies the gaps, V-SynFlow builds targeted training data in three stages.

First is multi-granular quality control. We correct annotations, remove pairs with low cross-modal consistency, and filter static samples. This creates a reliable asset pool.

Second is multi-dimensional information enrichment. A multimodal language model produces temporal, spatial, and partially relevant descriptions. We sample different information profiles and use frames, clips, or full videos as the visual input. This creates text-video, frame-video, and clip-video pairs.

Third is multimodal task extension. The basic pairs are extended to composed video retrieval, text retrieval, and text-image retrieval.

All sources are combined for training. Each stage fills a capability gap found by UVRB.

## Slide 13 — UVRD: Scale and Capability Coverage

V-SynFlow produces UVRD with 1.55 million synthesized pairs. With public data, the training mixtures contain 12.55 million instances for GVE-3B and 13.73 million for GVE-7B.

The data covers textual, visual, and composed queries across several domains. A human audit found 95 correct cases out of 100. It provides broad, gap-targeted supervision for training.

## Slide 14 — General Video Embedder: Architecture and Objective

This slide shows the General Video Embedder, or GVE.

GVE adapts Qwen2.5-VL to encode text, images, videos, and composed queries in one shared space. Last-token pooling and normalization produce the retrieval embedding.

Symmetric InfoNCE pulls a matched query-target pair closer and pushes unmatched pairs apart in both directions.

The key point is that one model learns the diverse abilities supplied by UVRD, instead of using one model for each task.

## Slide 15 — Modality Pyramid: Adaptive Foundational-to-Composite Curriculum

The remaining problem is how to train these different tasks together. Random mixing can create interference, and hard temporal or composed tasks may remain unstable.

The Modality Pyramid estimates the current alignment of each task. A prober measures the average similarity of positive pairs. A higher score means the current model already aligns that task more reliably.

Training first favors better-aligned, foundational tasks. Their basic visual and textual alignment supports later temporal and composed learning. The sampling then becomes flatter, so harder tasks appear more often.

The order is adaptive, not fixed. The latest GVE checkpoint becomes the next prober, so task difficulty is estimated again as the model changes.

## Slide 16 — Experiments: Capability Analysis on UVRB

The experiments return to the same capability space used for diagnosis.

GVE-7B covers the largest area on both radar plots and performs strongly across most datasets and abilities. Composed and visual retrieval still have room for improvement.

Existing models also show recurring weak capabilities. UVRB makes these patterns visible across a full capability profile.

## Slide 17 — Zero-Shot Retrieval Results on UVRB

Under the same zero-shot protocol, GVE-7B has the highest averages across sixteen datasets and the evaluated abilities. Its gains over Unite-7B are about 6.5 and 7.3 percent.

GVE-3B also outperforms the larger Unite-7B. Targeted data and task-aware training can therefore matter more than model size alone.

## Slide 18 — Ability-Level Retrieval Results

The largest gains appear in composed, long-context, and temporal retrieval. These are the weaknesses targeted by the data and curriculum.

Visual-only retrieval remains the main exception. A compact CLIP encoder is still hard to beat. One universal model does not dominate every setting.

## Slide 19 — Ablation: UVRD and Modality Pyramid

The ablation separates the two roles. UVRD provides the main gain, especially for composed retrieval. The Modality Pyramid improves the averages further.

UVRD supplies missing supervision. The curriculum reduces interference when different tasks are learned together.

## Slide 20 — Capability Correlations Reveal What Model Scale Misses

This analysis gives three practical insights.

First, partially relevant retrieval has the highest average correlation with overall UVR performance, about 0.97. It tests whether an embedding keeps both global meaning and small local details.

Second, spatial and temporal abilities have a weak correlation, about 0.12. Current models do not automatically learn “where” and “when” together.

Third, model size has limited impact on visual-only retrieval. The 87-million-parameter CLIP4Clip can outperform the 8-billion-parameter Unite-7B. Larger models improve broad semantics, but not always fine visual detail.

These results support capability-specific diagnosis and targeted supervision. Model scale alone does not fill every gap.

## Slide 21 — Data Scaling Across UVRB Abilities

This slide shows the average data-scaling trend.

As the training pairs increase, both average curves rise in an approximately log-linear pattern over the tested range.

GVE-3B has a steeper slope. GVE-7B starts higher and still improves. Targeted data scaling helps overall capability, but the rate depends on model size.

## Slide 22 — Study 1 Summary: Evaluation Guides Data and Training

The core challenge is fragmentation across data, models, and evaluation. The motivation is that we must first know which capabilities are missing before deciding what data to build and how to train.

Our contribution follows one chain. UVRB identifies weak abilities. V-SynFlow builds quality-controlled, targeted supervision. The Modality Pyramid learns foundational and harder tasks in an adaptive order. GVE brings these abilities into one shared embedder.

The insight is that semantic scaling needs a direction. Evaluation defines that direction, and data synthesis and curriculum learning follow it.

This leads directly to Study 2. Even with the right semantic ability, can a model retrieve the answer when a long video is represented by limited frames and tokens?

## Slide 23 — Study 2: Observational Scaling

Study 2 moves from what the model should represent to what the model can actually see. It studies spatiotemporal sampling for long-video retrieval and transfers dense-input knowledge to sparse inputs.

## Slide 24 — Observational Scaling: Sampling Defines What Can Be Seen

The core challenge is missing evidence. The average MG-LVR video lasts about 706 seconds, but evidence for one query may last only a few seconds.

Frame count controls temporal coverage. Tokens per frame control spatial detail. If the right moment is not sampled, the model cannot recover it. If each frame is compressed too much, local detail may disappear.

This motivates a controlled benchmark. Existing datasets provide long videos or multi-granular queries, but not both together. MG-LVR fills this gap and makes sampling effects measurable.

## Slide R2 — Related Work: Long-Video Retrieval and Scaling

The related work reveals a specific missing testbed.

Early benchmarks such as MSR-VTT and DiDeMo use short clips, so sparse sampling often captures most of the content. LoVR extends video duration. TVR and ActivityNet Captions provide finer temporal annotations. However, long duration and multiple query granularities are not jointly controlled.

At the model level, CLIP-based methods add temporal aggregation, while newer MLLM-based embedders use stronger multimodal language backbones. Existing scaling studies mainly examine model size, data volume, or frame scaling on shorter clips.

What remains unclear is how spatial and temporal sampling interact with query granularity in long videos. This is why MG-LVR controls duration, granularity, continuity, frames, and spatial tokens in one benchmark.

[Sources]

- `chapters/04-spatiotemporal-scaling.tex`, Related Works.

## Slide 25 — Temporal Granularity and Continuity

This slide defines temporal granularity and temporal continuity.

Temporal granularity measures how much of a video is relevant to one query. Fine-grained evidence covers about one percent or less. Medium-grained evidence covers around ten to thirty percent. Coarse-grained queries describe broad video-level content.

Temporal continuity shows how that evidence is distributed. A value of one means one continuous event. A smaller value means several separate intervals.

Granularity tells us how much is relevant. Continuity tells us whether it is connected.

## Slide 26 — Multi-Granular Long Video Retrieval Benchmark

MG-LVR makes the sampling problem measurable. It contains 4,844 long videos and 9,971 queries at three granularities, with an average length of 706 seconds.

We evaluate twenty-three models. A human audit found 48 correct pairs out of 50. The benchmark jointly controls long duration, granularity, continuity, and sampling density.

## Slide 27 — How MG-LVR Controls Query Granularity

The construction challenge is repeated information. If the same event appears in several clips, we should not count each clip as new evidence.

We split and caption each video, embed the clip captions, and build a Clip Relation Graph. An isolated node is unique single-clip information. Louvain groups related clips into one multi-clip unit, even when they appear at different times.

For each unique unit, we generate a query, measure its video coverage, assign fine, medium, or coarse granularity, and remove queries too similar to non-target clips.

The order is: find distinct information, measure coverage, then label granularity.

## Slide 28 — Granularity Gap Under Sparse Sampling

This is the main benchmark finding.

With eight frames, coarse-grained retrieval remains strong, while fine-grained retrieval is much lower. Increasing the frame count sixteen times gives only a modest fine-grained gain.

More frames alone do not remove the gap. The model must also know how to use the added evidence. This motivates the scaling analysis.

## Slide 29 — MG-LVR Enables Test-Time and Training-Time Scaling Analysis

MG-LVR supports two analyses.

Test-time scaling changes the evidence seen during inference. We vary frames, tokens per frame, and their allocation under a fixed budget.

Training-time scaling changes the learned representation. We post-train the same architecture at different sampling densities, then test matched and mismatched inputs.

This separates inference-time evidence from knowledge learned during training.

## Slide 30 — Test-Time Scaling: Spatial Density

First, we fix the frame count and vary the spatial tokens per frame.

More spatial tokens do not give one universal gain. Some architectures improve, while others quickly reach a plateau. The response also changes across query granularities.

More spatial detail is not automatically better. Its value depends on architecture and granularity.

## Slide 31 — Test-Time Scaling: Temporal Density

Next, we vary the number of sampled frames.

Multimodal language models keep improving with denser temporal sampling, especially for fine-grained queries. CLIP-based models usually plateau earlier and may decline when many frame embeddings are averaged.

Fine-grained retrieval needs coverage, but more frames help only when the model can combine them.

## Slide 32 — Test-Time Scaling: Spatiotemporal Trade-Off

This slide keeps the total visual-token budget fixed and changes how it is divided.

Coarse-grained queries usually prefer fewer frames with more spatial detail. Fine-grained queries prefer more frames, even with lower detail, because the main risk is missing a short event.

The best allocation depends on query granularity. One setting is not optimal for every query.

## Slide 33 — Training-Time Scaling: Spatial Resolution Robustness

Now we change the spatial density used during post-training.

Models trained at higher spatial density usually transfer well to lower-density inference. We call this resolution robustness.

At the highest density, the gain becomes small, and some results decline slightly. Spatial knowledge transfers across resolutions, but extreme density has diminishing returns.

## Slide 34 — Training-Time Scaling: Temporal Frame-Count Anchoring

Temporal training behaves differently.

We train the same architecture with four, eight, sixteen, or thirty-two frames, then test matched and mismatched frame counts. Performance usually peaks near the training count. A large mismatch hurts fine-grained retrieval.

We call this frame-count anchoring. Dense temporal training does not automatically transfer to sparse inference, which motivates the next method.

## Slide 35 — VEterfall: Progressive Dense-to-Sparse Self-Distillation

VEterfall uses the same base model. Dense, medium, and sparse refer to sampling density, not different architectures.

First, a frozen model processes dense input and produces teacher embeddings. Second, a trainable copy uses fewer frames and tokens. Mean squared error aligns its video embedding with the teacher, while an auxiliary InfoNCE loss keeps video-text alignment. Third, the trained checkpoint becomes the teacher for the next, sparser stage.

Dense-input knowledge is transferred step by step to sparse input without changing the deployment architecture.

## Slide 36 — Progressive Transfer Across Three Sampling Densities

This table compares the original checkpoint and the progressive transfer stages at the same inference density.

The gains are strongest for difficult fine- and medium-grained queries. At medium density, fine-grained retrieval improves while coarse retrieval drops slightly. At sparse density, the fine-grained gain is larger and coarse retrieval is almost unchanged.

This is a real trade-off. The method helps sparse fine-grained evidence, but the gain is not uniform across every granularity.

## Slide 37 — Study 2 Summary: Scaling Analysis Guides Sparse Transfer

The core challenge is evidence loss under limited frames and tokens. The motivation is to discover how observation changes retrieval before designing a transfer method.

Our contribution starts with MG-LVR, a controlled testbed for duration, granularity, continuity, and sampling. The analysis finds granularity-dependent allocation, spatial resolution robustness, and temporal frame-count anchoring.

The insight is that dense temporal knowledge does not transfer automatically to sparse inference. VEterfall turns this finding into progressive dense-to-sparse self-distillation.

The logic is benchmark, analysis, and then a method motivated by the discovered scaling behavior.

This leads directly to Study 3. How can the resulting relevance signal be searched over a billion-scale catalog?

## Slide 38 — Study 3: Search Scaling for Web-Scale Retrieval

Study 3 focuses on search scaling. It asks how learned relevance can remain accurate, searchable, and efficient when the candidate catalog and serving concurrency become very large.

## Slide 39 — Web-Scale Video Retrieval: From Catalog to Candidates

At web scale, retrieval must reduce a billion-scale catalog before ranking. It cannot score every item, so graph search visits only promising candidates and returns a top-K set.

Retrieval must be both fast and accurate. If a relevant item is removed here, ranking cannot recover it. The problem is to preserve relevance while searching a huge graph under online constraints.

## Slide R3 — Related Work: Industrial Retrieval Optimizes Components Separately

This study builds on two related areas.

The first is DNN-based recommendation. Neural collaborative filtering and two-tower models learn nonlinear user-item relevance and support large-scale candidate generation. However, separate behavior objectives may miss dependencies across click, browse, and other signals.

The second is approximate nearest neighbor search. KD-trees and LSH reduce exact search cost. Graph methods such as NSW and HNSW work better in high-dimensional spaces. Industrial systems such as SL2G and NANN further connect DNN relevance metrics with graph search.

The remaining issue is system-level separation. Multi-relational learning, breadth-depth traversal, and irregular GPU computation are still optimized as different problems. GMP-GR is motivated by the need to co-design these components for both retrieval quality and online efficiency.

[Sources]

- `chapters/05-scale-efficient-retrieval.tex`, Related Works.

## Slide 40 — Three Challenges in Web-Scale Graph Retrieval

The first challenge is multi-relational relevance. Click, browse, and related behaviors share useful signals. Separate metrics miss these relations and increase update cost. Joint learning should improve relevance.

The second challenge is graph search at billion scale. A strong score can still create poor local paths. Search must reach good candidates within limited steps by balancing depth and breadth.

The third challenge is irregular computation under high concurrency. Different queries create many small scoring jobs, and frequent GPU launches waste time. These jobs must be combined into efficient batches.

These challenges motivate one co-designed solution. Improving the score alone, the traversal alone, or the GPU code alone cannot solve the full retrieval problem.

## Slide 41 — GMP-GR: Offline Training and Online Search

GMP-GR follows the reading order from left to right. Its contribution connects offline metric learning with online traversal and execution.

Offline, MUIRML learns one metric from several user behaviors and adds a search-oriented ordering signal.

Online, C-HiPANNS broadens exploration within one query through connected search paths. Q-HiPANNS collects scoring jobs across concurrent queries into GPU-friendly batches.

The same relevance signal is learned offline, followed on the graph, and executed online.

## Slide 42 — MUIRML: Accurate Relevance That Remains Searchable

MUIRML predicts related user behaviors with one model. Attention combines click, browse, and other signals into one relevance score.

Self-Covariant Loss, or SCL, adds a soft ordering regularizer. It moves the relative order of learned scores closer to a Euclidean reference while keeping the behavior-prediction objective.

SCL is not a formal triangle-inequality guarantee. It makes the learned relevance more suitable for graph navigation.

## Slide 43 — HiPANNS: One Search Algorithm, Two Levels of Parallelism

HiPANNS uses two connected levels of parallelism.

C-HiPANNS works within one query. Several seeded searches share candidates and explore different graph paths, reducing the risk of one poor local path.

Q-HiPANNS works across queries. It collects small scoring jobs, forms bounded batches, and sends them to the GPU.

One improves exploration; the other executes it efficiently.

## Slide 44 — Web-Scale Video Deployment and System Optimization

Compilation simplifies the serving graph. Sixteen-bit quantization gives another throughput gain. Streaming updates keep user and video embeddings current.

The framework is reported across more than twenty Baidu applications. This supports deployment feasibility, while exact performance still depends on hardware and traffic.

## Slide 45 — Offline Retrieval Effectiveness and Efficiency

The offline evaluation uses four real-world video datasets and measures coverage, recall, and time cost.

GMP-GR improves coverage on all four datasets, gives a good balance between coverage and time, and improves Recall at ten on the video dataset.

The result supports both retrieval quality and practical efficiency.

## Slide 46 — Online A/B Evaluation

The online A/B evaluation covers two production video services.

Both services show positive gains in time on page and daily active users. The component analysis also reports gains from MUIRML and HiPANNS.

The controlled A/B table covers two services. The wider deployment claim covers more than twenty applications. These are different ranges of evidence.

## Slide 47 — Study 3 Summary: Co-Design Makes Learned Relevance Searchable

The core challenges are multi-relational relevance, billion-scale graph traversal, and irregular GPU work. The method is motivated by their interaction: a better score is not enough if graph search cannot follow it or the GPU cannot execute it efficiently.

Our contribution co-designs all three layers. MUIRML and SCL shape the relevance signal. C-HiPANNS broadens search within a query. Q-HiPANNS batches work across queries. Offline and online experiments test retrieval and deployment value.

The insight is that learned relevance must be accurate, searchable, and executable at the same time.

## Slide 48 — Conclusion and Future Work

The three studies now cover representation, observation, and search. I will first connect their contributions, then explain how generalization is tested, and finally discuss future work and limitations.

## Slide 49 — Three Retrieval Stages Form One Research Chain

The three studies protect three requirements in order, and each result motivates the next problem.

Semantic scaling builds a shared representation across queries, domains, and relevance conditions. Observational scaling keeps useful evidence available when frames and tokens are limited. Search scaling preserves that relevance through graph traversal and online serving.

The order matters. Observation is the bridge between representation and search. Search depends on a useful relevance signal, and that signal depends on relevant evidence entering the model. Together, the three contributions form one research chain.

## Slide 50 — Generalization Is Tested Differently at Each Stage

Each study needs a different transfer test.

Study 1 tests transfer across query formats, domains, and relevance conditions. Study 2 tests transfer across video granularities and sampling densities. Study 3 tests transfer across offline datasets and the reported online services.

The last column states the evidence boundary. Visual-only retrieval remains difficult. VEterfall gains vary by granularity. SCL is a soft regularizer, and the system is validated in one industrial stack.

Generalizability means useful transfer beyond one optimized condition, with a clear statement of where the evidence stops.

## Slide 51 — Three Research Principles for Scalable and Generalizable Retrieval

The thesis gives three research principles.

First, diagnose the active bottleneck. Semantic capability, visual evidence, and graph execution are different constraints.

Second, match the method to that constraint. Target data and training, input sampling, or graph execution where each problem appears.

Third, test transfer. A larger model, denser input, or more accurate score matters only if it remains useful in the next condition.

These principles lead to the three future directions.

## Slide 52 — Future Direction I: Retrieval-Native Multimodal Foundation Models

The first future direction is to make retrieval a native ability of multimodal foundation models.

Current models are mainly trained for generation, and retrieval is added later. A future model could use a retrieval token, routing mechanism, or lightweight adapter while keeping generation and instruction following.

The open question is how to produce compact retrieval states without reducing generation quality. Both abilities should be evaluated together.

## Slide 53 — Future Direction II: Video Retrieval as Long-Term Agent Memory

The second direction is long-term visual memory for agents.

An agent may need to find where an object was last seen or retrieve a rare event from many hours of video.

Semantic scaling supports different memory queries. Observational scaling decides what enters memory. Search scaling keeps the growing index available under latency limits.

Evaluation should include task success, decision time, and recall of rare events.

## Slide 54 — Future Direction III: Self-Evolving Data, Evaluation, and Curriculum

The third direction is a closed data and training loop.

Evaluation identifies a new gap. A synthesis system creates targeted examples. Curriculum training updates the model, which is then evaluated again.

This loop can adapt to changing query formats, domains, and relevance conditions. The open problem is retention: repair a new weakness without forgetting earlier abilities.

## Slide 55 — Limitations and Open Questions

There are three main limitations.

First, the studies examine separate pipeline stages rather than optimize the full system end to end.

Second, UVRD and MG-LVR partly rely on synthetic or caption-based signals. Broader human and natural-data validation is needed.

Third, GMP-GR is tested in one industrial stack. Throughput and latency depend on hardware, traffic, and serving design.

These limits point to end-to-end integration, stronger supervision, and cross-system transfer.

## Slide 56 — Acknowledgements

Before I close, I would like to express my sincere gratitude.

I am deeply grateful to my advisors, Prof. Xiaowen Chu and Prof. Renjing Xu, for their trust, guidance, patience, and support. I also thank my former supervisor, Prof. Hao Liu, for helping me build a strong research foundation.

I sincerely thank my collaborators, labmates, industry partners, family, and friends for their ideas, hard work, and steady support.

I am especially grateful to every committee member. Thank you for carefully reading my work, for your thoughtful questions, and for guidance that will continue to shape my research.

Finally, I thank the administrative staff of AI Thrust and HKUST(GZ), especially Ms. Claire Ying Luo from AS, for their patient and careful support.

## Slide 57 — First-Author Publications

The first three publications correspond to the three studies in this thesis: universal video retrieval, spatiotemporal scaling laws, and web-scale graph retrieval.

The remaining six first-author papers cover federated graph learning, labor-market modeling, and related graph problems. Together, the nine papers show my broader research path and PhD workload.

## Slide 58 — Questions

This concludes my presentation. Thank you again for your time, careful review, and valuable guidance. I welcome your questions and suggestions.

## Slide 59 — Appendix

The appendix contains detailed protocols, additional results, deployment evidence, and prepared committee questions. I will use it when a question needs more detail.

## Slide 60 — UVRB Protocol and Selected Ability Results

This slide provides the common UVRB protocol and selected ability-level results. It can support questions about evaluation fairness, preprocessing, or representative capability profiles.

## Slide 61 — UVRB Capability Radar and Correlation Findings

This slide provides the task-level radar view and the main correlation findings. It can support questions about capability imbalance and gap-targeted data design.

## Slide 62 — MG-LVR Benchmark Context and 128-Frame Results

This slide shows the MG-LVR benchmark context and the 128-frame results. The fine-to-coarse gap remains visible even with dense temporal sampling.

## Slide 63 — VEterfall Frame-Efficiency and Token-Efficiency

This slide compares frame efficiency and token efficiency. It shows that VEterfall is most useful in the sparse-input regime, especially for fine-grained retrieval.

## Slide 64 — MG-LVR Error Analysis

This slide separates missing temporal evidence from incomplete semantic matching. Not every fine-grained error can be explained by sampling alone.

## Slide 65 — GMP-GR Full Offline Results and Ablation

This slide provides the complete offline results and ablations. Removing either MUIRML or HiPANNS reduces the reported retrieval results.

## Slide 66 — Production Traffic and Latency Evidence

This slide shows anonymized production traffic and latency traces. It supports feasibility under the observed workload, but not identical behavior on every platform.

## Slide 67 — Prepared Committee Questions

This slide contains short answers to six likely questions about model choice, audit size, benchmark validity, method composition, SCL, and deployment transfer.
