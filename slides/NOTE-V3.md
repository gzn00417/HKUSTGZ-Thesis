# Thesis Defense Speaker Notes — V3

This script corresponds to `thesis-slides-v3.pptx`. It starts from V2, compresses the three conclusion-synthesis pages into two, and improves the full oral script.

Target delivery: about 44–49 minutes, including short pauses and slide changes. Use the slide as the main prompt. The first sentence of each paragraph is a restart point.

## Slide 1 — Towards Scalable and Generalizable Video Retrieval

Good morning, professors, committee members, colleagues, and friends. My name is Zhuoning Guo. Thank you very much for attending my PhD thesis defense.

I am deeply grateful to my advisors, Prof. Xiaowen Chu and Prof. Renjing Xu. I am also honored to have Prof. Pan Hui, Prof. Jeffrey Xu Yu, Prof. Yutao Yue, Prof. Xuming Hu, and Prof. Meishan Zhang on my committee. Thank you for your time and valuable guidance.

My thesis is titled “Towards Scalable and Generalizable Video Retrieval.” It studies how retrieval should change when queries become more diverse, videos become longer, and candidate collections become much larger.

I also thank the administrative staff of AI Thrust and HKUST(GZ), especially Ms. Claire Ying Luo from AS, for helping organize today’s defense.

## Slide 2 — Thesis Roadmap

This is the roadmap. I will first introduce the overall problem. Then I will present three connected studies: semantic, observational, and search scaling. I will finish with the technical contributions, future directions, and limitations.

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

Training decides what meaning the embedding can represent. This is semantic scaling.

Sampling decides which parts of a long video the model can see. This is observational scaling.

Graph retrieval decides whether the learned score can still be used over a huge catalog. This is search scaling.

The order is simple: learn the right signal, keep the needed evidence, and make the signal usable at scale.

## Slide 7 — What Each Scaling Stage Changes

Each stage changes a different object.

Semantic scaling broadens the retrieval capability. A larger model does not automatically cover every task.

Observational scaling changes the frames and spatial tokens given to the encoder. The challenge is to spend a limited visual budget well.

Search scaling changes catalog size and online concurrency. The challenge is to follow the score on a graph and compute it efficiently.

So each stage needs a different response: targeted learning, controlled sampling, or co-designed graph retrieval.

## Slide 8 — Thesis Overview: Three Studies, One Connected Chain

This page gives the complete research chain.

Study 1 asks how one embedding model can cover diverse retrieval tasks. We diagnose weak abilities, synthesize targeted data, and train GVE with an adaptive curriculum.

Study 2 asks what happens when long videos must be compressed into a few frames and tokens. We build MG-LVR, study this sampling process, and transfer dense-input knowledge to sparse inputs with VEterfall.

Study 3 asks how the learned score can be searched over a very large catalog. GMP-GR jointly designs relevance learning, graph traversal, and GPU execution.

The chain is direct: representation defines the score, observation provides its evidence, and search makes it useful at scale.

## Slide 9 — Study 1: Semantic Scaling

Study 1 focuses on semantic scaling. It asks what capabilities a universal video retrieval model should have, and how one model can learn these capabilities together.

## Slide 10 — Universal Video Retrieval Remains Fragmented

Universal video retrieval covers textual, visual, and composed queries. It also covers coarse, fine-grained, and long-context domains, including spatial, temporal, and partially relevant information.

The core challenge is fragmentation. Tasks use separately prepared data, models are trained for separate tasks or domains, and evaluation is divided across isolated benchmarks. The field lacks one model with broad capability coverage.

This creates two research hurdles: quality-controlled data synthesis across tasks and connected multi-task learning. Foundational and complex tasks are related, not independent.

Our response is to diagnose first, build data for the missing abilities, and then train related tasks in a structured order.

## Slide R1 — Related Work: Progress Without Unified Capability Coverage

Before UVRB, I will briefly review two directions.

Video retrieval benchmarks now cover grounding, scene understanding, composed queries, and visual queries. However, each benchmark usually measures one specialized setting.

Embedding models have also moved from CLIP-based video extensions to stronger MLLM embedders. They improve language and temporal understanding, but no single evaluation shows their full capability pattern.

The missing piece is a unified diagnosis that can guide both data construction and shared-model training.

## Slide 11 — Universal Video Retrieval Benchmark

UVRB first makes the capability gaps visible. It organizes sixteen public datasets under one protocol.

All fourteen models use the same preprocessing, frozen embeddings, cosine similarity, and no task-specific fine-tuning.

UVRB gives each model one capability profile. It shows which abilities are weak and guides the next two steps: data construction and training.

## Slide 12 — V-SynFlow: Three-Stage Data Synthesis

After UVRB identifies the gaps, V-SynFlow repairs them through three data stages.

First, we clean the raw material. We correct annotations, remove weak text-video matches, and filter static samples. This gives us a reliable pool.

Second, we add the information that current models often miss. A multimodal language model writes temporal, spatial, and partially relevant descriptions. We pair them with frames, clips, or full videos.

Third, we turn these basic pairs into more task formats, including composed video retrieval, text retrieval, and text-image retrieval.

In plain words, UVRB tells us what is missing, and V-SynFlow creates focused practice for those missing skills.

## Slide 13 — UVRD: Scale and Capability Coverage

V-SynFlow produces UVRD with 1.55 million synthesized pairs. With public data, the training mixtures contain 12.55 million instances for GVE-3B and 13.73 million for GVE-7B.

The data covers textual, visual, and composed queries across several domains. A human audit found 95 correct cases out of 100. It provides broad, gap-targeted supervision for training.

## Slide 14 — General Video Embedder: Architecture and Objective

This slide shows the General Video Embedder, or GVE.

GVE adapts Qwen2.5-VL to encode text, images, videos, and composed queries in one shared space. Last-token pooling and normalization produce the retrieval embedding.

Symmetric InfoNCE teaches the space with a simple rule: a correct pair should be close, and the wrong pairs should be farther away. We apply the rule in both query-to-video and video-to-query directions.

The key point is that one model learns the diverse abilities supplied by UVRD, instead of using one model for each task.

## Slide 15 — Modality Pyramid: Adaptive Foundational-to-Composite Curriculum

The remaining problem is how to train all tasks together. If we mix everything at random, easy and hard tasks can pull the model in different directions.

The Modality Pyramid first checks the current state of each task. A small probing evaluation measures how well positive pairs are already aligned. A higher score means that task is more stable at this moment.

Training gives more weight to stable, foundational tasks first, like learning basic visual-text matching before harder temporal or composed cases. Later, the sampling becomes more even, so hard tasks receive more practice.

The order is not fixed by hand. The latest GVE checkpoint performs the next check, so the schedule changes as the model improves. This is the main difference from a fixed curriculum.

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

Study 1 follows one chain. UVRB finds weak abilities. V-SynFlow builds focused supervision. The Modality Pyramid schedules foundational and harder tasks as training changes. GVE brings them into one shared embedder.

The novelty is not a larger backbone. It is the connection from diagnosis, to data, to adaptive training.

This leads directly to Study 2. Even with the right semantic ability, can a model retrieve the answer when a long video is represented by limited frames and tokens?

## Slide 23 — Study 2: Observational Scaling

Study 2 moves from what the model should represent to what the model can actually see. It studies spatiotemporal sampling for long-video retrieval and transfers dense-input knowledge to sparse inputs.

## Slide 24 — Observational Scaling: Sampling Defines What Can Be Seen

The core challenge is missing evidence. The average MG-LVR video lasts about 706 seconds, but evidence for one query may last only a few seconds.

Frame count controls temporal coverage. Tokens per frame control spatial detail. If the right moment is not sampled, the model cannot recover it. If each frame is compressed too much, local detail may disappear.

This is why we need a controlled benchmark. Existing datasets provide long videos or several levels of query detail, but not both together. MG-LVR makes the sampling effect measurable.

## Slide R2 — Related Work: Long-Video Retrieval and Scaling

The related work reveals a missing testbed.

Early benchmarks use short clips, so sparse sampling often captures most of the content. Newer datasets extend duration or add fine temporal labels, but they do not jointly control long videos and several query granularities.

Model studies also tend to change model size, data volume, or frame count separately.

MG-LVR brings duration, granularity, continuity, frames, and spatial tokens into one controlled benchmark so their interaction can be studied.

## Slide 25 — Temporal Granularity and Continuity

This slide defines temporal granularity and temporal continuity.

Temporal granularity measures how much of a video is relevant to one query. Fine-grained evidence covers about one percent or less. Medium-grained evidence covers around ten to thirty percent. Coarse-grained queries describe broad video-level content.

Temporal continuity shows how that evidence is distributed. A value of one means one continuous event. A smaller value means several separate intervals.

Granularity tells us how much is relevant. Continuity tells us whether it is connected.

## Slide 26 — Multi-Granular Long Video Retrieval Benchmark

MG-LVR makes the sampling problem measurable. It contains 4,844 long videos and 9,971 queries at three granularities, with an average length of 706 seconds.

We evaluate twenty-three models. A human audit found 48 correct pairs out of 50. The benchmark jointly controls long duration, granularity, continuity, and sampling density.

## Slide 27 — How MG-LVR Controls Query Granularity

The main construction problem is repeated information. If the same event appears in several clips, we should not count every clip as a different event.

We split the long video into clips and caption each clip. Then we connect clips with similar meaning in a Clip Relation Graph. An isolated clip gives one unique piece of information. Related clips are grouped into one unit, even if they appear at different times.

For each unit, we generate a query and measure how much of the full video supports it. That coverage decides whether the query is fine, medium, or coarse. A final filter removes cases that also match other clips.

So the construction is: find distinct information, measure its coverage, and only then assign the granularity label.

## Slide 28 — Granularity Gap Under Sparse Sampling

This is the main benchmark finding.

With eight frames, coarse-grained retrieval remains strong, while fine-grained retrieval is much lower. Increasing the frame count sixteen times gives only a modest fine-grained gain.

More frames alone do not remove the gap. The model must also know how to use the added evidence. This motivates the scaling analysis.

## Slide 29 — MG-LVR Enables Test-Time and Training-Time Scaling Analysis

MG-LVR supports two analyses.

Test-time scaling changes only the input at inference. We vary frame count, tokens per frame, and their allocation under a fixed budget. This asks: what can the current model use when we show it more or less evidence?

Training-time scaling changes what the model has learned to expect. We post-train the same architecture at different densities, then test both matched and mismatched inputs.

This separation is important. One experiment changes what the model sees now. The other changes what the model learned before deployment.

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

VEterfall keeps the same base architecture. Dense, medium, and sparse describe only the input sampling.

The idea is teacher and student learning. A frozen copy sees dense input and produces a teacher embedding. A trainable copy sees the same video with fewer frames and tokens. Mean squared error asks the student to reproduce the teacher's video embedding. An auxiliary InfoNCE loss keeps it aligned with text.

After one stage, the student becomes the teacher for the next, sparser stage. We do not force one large jump from dense to very sparse input. We transfer the knowledge step by step.

The deployment model is still the same architecture. It simply learns to keep more of the dense representation when the input becomes sparse.

## Slide 36 — Progressive Transfer Across Three Sampling Densities

This table compares the original checkpoint and the progressive transfer stages at the same inference density.

The gains are strongest for difficult fine- and medium-grained queries. At medium density, fine-grained retrieval improves while coarse retrieval drops slightly. At sparse density, the fine-grained gain is larger and coarse retrieval is almost unchanged.

This is a real trade-off. The method helps sparse fine-grained evidence, but the gain is not uniform across every granularity.

## Slide 37 — Study 2 Summary: Scaling Analysis Guides Sparse Transfer

Study 2 also follows a clear chain. MG-LVR creates the controlled testbed. The analysis finds that the best token allocation depends on granularity, spatial knowledge is fairly robust, and temporal knowledge is anchored to the training frame count.

That last finding motivates VEterfall. Dense temporal knowledge does not move to sparse inference by itself, so we transfer it in stages through self-distillation.

This leads directly to Study 3. How can the resulting relevance signal be searched over a billion-scale catalog?

## Slide 38 — Study 3: Search Scaling for Web-Scale Retrieval

Study 3 focuses on search scaling. It asks how learned relevance can remain accurate, searchable, and efficient when the candidate catalog and serving concurrency become very large.

## Slide 39 — Web-Scale Video Retrieval: From Catalog to Candidates

At web scale, retrieval must reduce a billion-scale catalog before ranking. It cannot score every item, so graph search visits only promising candidates and returns a top-K set.

Retrieval must be both fast and accurate. If a relevant item is removed here, ranking cannot recover it. The problem is to preserve relevance while searching a huge graph under online constraints.

## Slide R3 — Related Work: Industrial Retrieval Optimizes Components Separately

This study builds on recommendation models and approximate nearest neighbor search.

Neural models learn user-item relevance, but separate behavior objectives may miss links across click, browse, and other signals.

Graph methods such as HNSW reduce exact search cost in high-dimensional spaces. Industrial systems connect learned metrics with graph search, but metric learning, graph traversal, and GPU work are still largely separate.

GMP-GR asks what happens if these parts are designed as one retrieval system.

## Slide 40 — Three Challenges in Web-Scale Graph Retrieval

The first challenge is relevance. Click, browse, and other behaviors share information. Separate metrics miss these links and are expensive to maintain.

The second challenge is graph navigation. Even an accurate score can produce a poor local path. The search must look deep enough without staying in one narrow region.

The third challenge is GPU execution. Each user follows a different path and creates small scoring jobs. Sending them one by one wastes GPU launch cost.

The three problems depend on each other. The score, the path, and the execution must work together.

## Slide 41 — GMP-GR: Offline Training and Online Search

GMP-GR follows the reading order from left to right. Think of it as learning a road map offline and using it during online search.

Offline, MUIRML learns one relevance metric from several user behaviors. SCL also shapes the score order so that graph navigation has a clearer direction.

Online, C-HiPANNS opens several paths for one query, so the search is less likely to get stuck. Q-HiPANNS then collects scoring work from many queries and forms GPU-friendly batches.

The novelty is the connection: the score, graph search, and GPU schedule are designed together.

## Slide 42 — MUIRML: Accurate Relevance That Remains Searchable

MUIRML replaces several behavior-specific metrics with one model. It predicts related behaviors together, and attention combines them into one relevance score.

Self-Covariant Loss, or SCL, adds a search-oriented guide. Graph search needs a useful direction. SCL softly adjusts the score order toward a Euclidean reference while preserving the main behavior prediction.

This is a soft guide, not a proof of triangle inequality. Its purpose is practical: make the learned score easier to follow during graph search.

## Slide 43 — HiPANNS: One Search Algorithm, Two Levels of Parallelism

HiPANNS uses two connected levels of parallelism.

C-HiPANNS works inside one query. Several seeded paths explore the graph together and share their best candidates. We search from several doors instead of trusting one path.

Q-HiPANNS works across queries. It groups small scoring jobs into bounded GPU batches and reduces frequent launches.

C-HiPANNS improves where we search. Q-HiPANNS improves how that work is executed. The second level directly serves the first.

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

Study 3 contributes one connected system. MUIRML and SCL learn a score that contains several behavior signals and is easier to navigate. C-HiPANNS broadens graph exploration inside a query. Q-HiPANNS batches the resulting work across queries.

The novelty is the co-design across learning, search, and execution. The main lesson is that relevance must be accurate, searchable, and executable at the same time.

## Slide 48 — Conclusion and Future Work

The three studies now cover representation, observation, and search. I will first connect their contributions, then explain how generalization is tested, and finally discuss future work and limitations.

## Slide 49 — Why These Three Problems Must Be Studied Together

These three problems come from three places where retrieval can fail.

First, the model may not represent the user's real intent. Standard text-to-video matching is not enough for visual, composed, temporal, or partly relevant cases. This is semantic scaling.

Second, the right ability is useless if the evidence never enters the encoder. A long video must be reduced to a few frames and tokens, so a short event can disappear before the model reasons about it. Observation is therefore the bridge.

Third, even a good embedding cannot score every item in a billion-scale catalog. Graph search and online execution must keep the score usable. Search scaling completes the chain.

The key is their dependency. Representation defines the signal. Observation supplies its evidence. Search turns it into a deployable result. Together, the studies form one end-to-end research path.

## Slide 50 — Technical Novelty and Contributions

This page summarizes what is technically new in each study.

In Study 1, UVRB diagnoses weak abilities and guides V-SynFlow and the 1.55-million-pair UVRD dataset. The Modality Pyramid rechecks task alignment and updates the schedule. This diagnosis-to-data-to-curriculum loop is the novelty. GVE-7B gains 6.5 percent over Unite-7B, and GVE-3B also beats it.

In Study 2, MG-LVR is the first controlled benchmark combining long videos with several granularities. It reveals frame-count anchoring. VEterfall then transfers the same model from dense to sparse input step by step, without external labels, giving up to about 20 percent relative R-at-one improvement.

In Study 3, GMP-GR co-designs the score, graph traversal, and GPU execution. MUIRML and SCL shape the score. C-HiPANNS explores several paths, and Q-HiPANNS batches work across queries. The stack is deployed in more than twenty applications and reports over three percent time-on-page improvement.

Across the thesis, the main principle is: match capacity to the active bottleneck, and then test whether the gain transfers.

## Slide 51 — Future Direction I: Retrieval-Native Multimodal Foundation Models

The first future direction is to make retrieval a native ability of multimodal foundation models.

Current models are mainly trained for generation, and retrieval is added later. A future model could use a retrieval token, routing mechanism, or lightweight adapter while keeping generation and instruction following.

The open question is how to produce compact retrieval states without reducing generation quality. Both abilities should be evaluated together.

## Slide 52 — Future Direction II: Video Retrieval as Long-Term Agent Memory

The second direction is long-term visual memory for agents.

An agent may need to find where an object was last seen or retrieve a rare event from many hours of video.

Semantic scaling supports different memory queries. Observational scaling decides what enters memory. Search scaling keeps the growing index available under latency limits.

Evaluation should include task success, decision time, and recall of rare events.

## Slide 53 — Future Direction III: Self-Evolving Data, Evaluation, and Curriculum

The third direction is a closed data and training loop.

Evaluation identifies a new gap. A synthesis system creates targeted examples. Curriculum training updates the model, which is then evaluated again.

This loop can adapt when user needs or video content changes. The open problem is retention: repair a new weakness without forgetting earlier abilities.

## Slide 54 — Limitations and Open Questions

There are three main limitations.

First, the studies examine separate pipeline stages rather than optimize the full system end to end.

Second, UVRD and MG-LVR partly rely on synthetic or caption-based signals. Broader human and natural-data validation is needed.

Third, GMP-GR is tested in one industrial stack. Throughput and latency depend on hardware, traffic, and serving design.

These limits point to end-to-end integration, stronger supervision, and cross-system transfer.

## Slide 55 — Acknowledgements

Before I close, I would like to express my sincere gratitude.

I am deeply grateful to my advisors, Prof. Xiaowen Chu and Prof. Renjing Xu, for their trust, guidance, patience, and support. I also thank my former supervisor, Prof. Hao Liu, for helping me build a strong research foundation.

I sincerely thank my collaborators, labmates, industry partners, family, and friends for their ideas, hard work, and steady support.

I am especially grateful to every committee member. Thank you for carefully reading my work, for your thoughtful questions, and for guidance that will continue to shape my research.

Finally, I thank the administrative staff of AI Thrust and HKUST(GZ), especially Ms. Claire Ying Luo from AS, for their patient and careful support.

## Slide 56 — First-Author Publications

The first three publications correspond to the three studies in this thesis: universal video retrieval, spatiotemporal scaling laws, and web-scale graph retrieval.

The remaining six first-author papers cover federated graph learning, labor-market modeling, and related graph problems. Together, the nine papers show my broader research path and PhD workload.

## Slide 57 — Questions

This concludes my presentation. Thank you again for your time, careful review, and valuable guidance. I welcome your questions and suggestions.

## Slide 58 — Appendix

The appendix contains detailed protocols, additional results, deployment evidence, and prepared committee questions. I will use it when a question needs more detail.

## Slide 59 — UVRB Protocol and Selected Ability Results

This slide provides the common UVRB protocol and selected ability-level results. It can support questions about evaluation fairness, preprocessing, or representative capability profiles.

## Slide 60 — UVRB Capability Radar and Correlation Findings

This slide provides the task-level radar view and the main correlation findings. It can support questions about capability imbalance and gap-targeted data design.

## Slide 61 — MG-LVR Benchmark Context and 128-Frame Results

This slide shows the MG-LVR benchmark context and the 128-frame results. The fine-to-coarse gap remains visible even with dense temporal sampling.

## Slide 62 — VEterfall Frame-Efficiency and Token-Efficiency

This slide compares frame efficiency and token efficiency. It shows that VEterfall is most useful in the sparse-input regime, especially for fine-grained retrieval.

## Slide 63 — MG-LVR Error Analysis

This slide separates missing temporal evidence from incomplete semantic matching. Not every fine-grained error can be explained by sampling alone.

## Slide 64 — GMP-GR Full Offline Results and Ablation

This slide provides the complete offline results and ablations. Removing either MUIRML or HiPANNS reduces the reported retrieval results.

## Slide 65 — Production Traffic and Latency Evidence

This slide shows anonymized production traffic and latency traces. It supports feasibility under the observed workload, but not identical behavior on every platform.

## Slide 66 — Prepared Committee Questions

This slide contains short answers to six likely questions about model choice, audit size, benchmark validity, method composition, SCL, and deployment transfer.
