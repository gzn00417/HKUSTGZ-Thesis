# V1 Speaker Notes

This is the clean speaker-note script for `thesis-slides-v1.pptx`.

The main talk contains 56 slides. The appendix contains 9 backup slides. The
script uses short sentences, common words, and clear restart points. Strong
phrases already visible on the slides are reused when they are easy to say.
Appendix notes only explain what each backup slide contains.

The main script contains about 3,450 spoken words. At a careful pace of 80 to 90
words per minute, the direct reading time is about 38 to 43 minutes. With normal
pauses, slide changes, and brief recovery time, the conservative delivery range
is about 44 to 49 minutes.

## Slide 1 — Towards Scalable and Generalizable Video Retrieval

Hello, everyone. My name is Zhuoning Guo. Thank you for attending my PhD thesis
defense.

I would first like to thank my advisors, Prof. Xiaowen Chu and Prof. Renjing Xu.
I also thank the committee. The chair is Prof. Pan Hui. The other members are
Prof. Jeffrey Xu Yu, Prof. Yutao Yue, Prof. Xuming Hu, and Prof. Meishan Zhang
from HIT (Shenzhen).

My thesis is “Towards Scalable and Generalizable Video Retrieval.” It asks how
retrieval should change when queries, videos, and candidate collections grow.

## Slide 2 — Thesis Roadmap

This is the roadmap of my talk. I will first introduce the video retrieval
problem and the three scaling stages. Then I will present three studies.

Study 1 is about semantic scaling. Study 2 is about observational scaling.
Study 3 is about search scaling. Finally, I will connect the three studies,
summarize the thesis, and discuss future work and limitations.

## Slide 3 — Guiding Question

The guiding question is simple: How should retrieval methods change as query
diversity, video length, and corpus size grow?

These three changes lead to three different bottlenecks. Please keep this
question in mind as I explain what each study changes, and why that change is
needed.

## Slide 4 — Applications of Video Retrieval

Video retrieval is used in several common settings. In search, a text, image, or
video query is used to find relevant videos. In recommendation, retrieval gives
the ranking system a smaller candidate set. In data processing, retrieval helps
filter and organize multimodal training data.

The conditions are also changing. Queries are more diverse, videos are longer
and richer, and collections are too large for exhaustive scoring.

## Slide 5 — Embedding-Based Video Retrieval

This slide gives the basic retrieval process. First, we encode the query and
each video into a shared embedding space. The query may be text, an image, a
clip, or a composed query.

Second, we compare the embeddings, usually with cosine similarity. Third, we
rank the corpus and return the top-K videos. During training, a relevant pair
should have a higher score than an irrelevant pair.

## Slide 6 — Three Connected Scaling Decisions

The three stages follow the retrieval pipeline in order.

Semantic scaling asks what the representation can cover. Observational scaling
asks what evidence the model can see under a limited input budget. A model
cannot recover a moment that was never sampled. Search scaling asks whether the
learned relevance still works over a very large corpus.

This dependency explains the research order: representation, then observation,
and finally deployment-scale search.

## Slide 7 — What Each Scaling Stage Changes

Each stage scales a different object.

Semantic scaling covers more queries and domains, but model or data growth does
not give balanced ability by itself. Observational scaling changes the frames
and visual tokens, but the useful choice depends on the video, query, and model.
Search scaling changes corpus size and concurrency, but accurate scores may
still be hard to follow on a graph and expensive to run.

So each stage needs its own research design.

## Slide 8 — Three Studies, One Connected Chain

Study 1 asks whether one embedding can cover different retrieval settings. It
uses unified evaluation, targeted data, and curriculum-trained GVE. This enables
the next question: what evidence can this representation see?

Study 2 answers with controlled sampling analysis and dense-to-sparse transfer.
This enables practical relevance signals under a limited input budget.

Study 3 co-designs relevance learning, graph search, and GPU execution for a
billion-scale corpus. This completes the chain.

## Slide 9 — Study 1: Semantic Scaling

The first study is about semantic scaling. The question is: What capabilities
should a video retrieval model have, and how can we scale toward them?

I will move from the capability gap, to unified evaluation, targeted data
synthesis, model training, and the main results.

## Slide 10 — Review of the Problem and Existing Research

Video retrieval includes textual, visual, and composed queries. It also covers
coarse-grained, fine-grained, and long-context settings, including spatial,
temporal, and partially relevant evidence.

The gap has two parts. These abilities are usually split across separate models
and benchmarks. Existing work also lacks one framework that first identifies
the gaps and then trains for them together.

## Slide 11 — Universal Video Retrieval Benchmark

To make these gaps visible, I organize sixteen public datasets into the
Universal Video Retrieval Benchmark, or UVRB.

All models use the same preprocessing and cosine similarity, with no
task-specific fine-tuning. The evaluation covers fourteen models from both CLIP
and multimodal language-model families.

The goal is not only to give one leaderboard score. It is to show which
capabilities are weak for each model, so the next data and training steps can be
guided by evidence.

## Slide 12 — V-SynFlow

After finding the gaps, V-SynFlow builds targeted training data in three steps.

First, multi-granular quality control removes weak or inconsistent supervision.
Second, information enrichment adds temporal, spatial, and partially relevant
details. Third, task extension converts the enriched content into textual,
visual, and composed retrieval pairs.

The important point is that the synthesis process follows the weaknesses found
by UVRB. It is not general data growth without a target.

## Slide 13 — UVRD Scale, Tasks, and Domains

The first block shows scale and validation. UVRD contains 1.55 million
synthesized pairs. With public data, the full mixture contains 12.55 million
instances for GVE-3B and 13.73 million for GVE-7B. A human check found 95
correct cases out of 100.

The second block shows textual, visual, and composed queries across
coarse-grained, fine-grained, and long-context settings.

## Slide 14 — General Video Embedder

This figure shows the General Video Embedder, or GVE.

First, GVE adapts Qwen2.5-VL for retrieval and maps text, images, videos, and
composed queries into one embedding space.

Second, symmetric InfoNCE pulls a matched pair closer and pushes unmatched
examples apart in both directions. At inference time, the final normalized
representation is used for retrieval. The other details support training speed.

## Slide 15 — Modality Pyramid

Random task mixing can cause interference. The Modality Pyramid uses current
task alignment to set the training order.

At each epoch, a prober measures average cosine similarity on one thousand
positive pairs per task. A higher score means better alignment. The temperature
then rises from 0.1 to 1.0, so training starts with better-aligned tasks and
slowly adds harder ones.

The scores are measured again from the latest checkpoint, so the curriculum is
adaptive rather than fixed.

## Slide 16 — Experimental Readout on UVRB

The experiments measure GVE across datasets, query formats, and capability
groups under one protocol. One strong benchmark result is not enough.

The radar plots give the main view. GVE-7B covers the largest area. They also
show common weak axes, especially temporal, composed, and partially relevant
retrieval. The next slides explain the result.

## Slide 17 — Overall Zero-Shot Results

This table compares zero-shot retrieval under the same UVRB protocol.

Please focus on the highlighted averages. GVE-7B gives the strongest overall
dataset and ability averages among the evaluated models. GVE-3B also
outperforms the larger Unite-7B baseline in this comparison.

The main conclusion is that targeted data and task-aware training can matter as
much as model size. I will leave the detailed values on the slide for reference.

## Slide 18 — Ability-Level Results

This table breaks the result into different abilities.

The largest gains appear in composed, long-context, and temporal retrieval.
These are also important gaps identified by the earlier evaluation, so the
improvement matches the design goal.

There is also a clear boundary. Visual-only retrieval stays almost flat, and a
compact CLIP encoder remains difficult to beat. So the method improves the
targeted weak abilities, but it does not solve every retrieval setting equally.

## Slide 19 — Ablation Study

The ablation separates the effect of targeted data from the effect of task
ordering.

Adding UVRD gives the main gain on composed retrieval and also improves the
dataset average. Adding the Modality Pyramid improves the averages further.

So these two parts solve different problems. UVRD broadens the supervision for
missing capabilities. The curriculum improves optimization when the tasks are
trained together. The highlighted numbers show the size of each step.

## Slide 20 — Capability Correlations

This analysis gives three observations. Partially relevant retrieval has the
strongest correlation with overall UVR. Spatial and temporal abilities are only
weakly correlated, so one cannot stand in for the other. The visual-only
comparison also shows that more parameters do not guarantee a better result.

These correlations support gap-targeted data design, but they do not prove
causality.

## Slide 21 — Data Scaling

Both dataset and ability averages rise in an approximately log-linear way over
the tested data range. However, the rates differ across abilities and model
sizes. GVE-3B improves faster on most abilities, while GVE-7B benefits more on
long-context retrieval.

Data scaling is useful, but it is task-dependent. Not every capability grows at
the same rate.

## Slide 22 — Study 1 Summary

Study 1 follows one clear research chain.

UVRB first unifies sixteen datasets and shows which capabilities are weak.
V-SynFlow then builds 1.55 million targeted pairs for these gaps. The Modality
Pyramid reduces interference by moving from better-aligned tasks to harder
ones. These parts together produce GVE, a cross-domain and multi-task video
embedder.

The key lesson is that evaluation, data, training, and the final model should be
designed as one connected process.

## Slide 23 — Study 2: Observational Scaling

The second study is about observational scaling. It asks which visual evidence
enters the model when the input budget is limited.

The main idea is that sampling is not only preprocessing. It sets the
information boundary of the representation. I will first introduce a controlled
benchmark, then analyze test-time and training-time scaling, and finally present
dense-to-sparse transfer.

## Slide 24 — Sampling Defines What Can Be Seen

The average MG-LVR video is about seven hundred and six seconds long, but the
relevant evidence may last only a few seconds.

The frame count controls temporal coverage. The tokens kept for each frame
control spatial detail. Existing benchmarks usually provide long videos or
multi-granular queries, but not both. We need both conditions to isolate how
sampling changes retrieval.

## Slide 25 — Temporal Granularity and Continuity

Temporal granularity measures how much of the video is relevant. A fine-grained
query may refer to one moment, while a coarse query describes the video more
broadly.

Temporal continuity asks whether the evidence is one segment or several
scattered parts. The distinction matters because fine-grained queries usually
need more temporal coverage, while coarse queries can benefit more from spatial
detail.

## Slide 26 — MG-LVR Benchmark

MG-LVR is designed to make these sampling effects measurable.

It contains 4,844 long videos and 9,971 queries at fine, medium, and coarse
granularity. The average video is about 706 seconds. We evaluate 23 models,
including six CLIP-based models and seventeen multimodal language models.

A human audit found 48 correct pairs out of 50. The main contribution is one
testbed that combines long videos, controlled query granularity, and controlled
sampling.

## Slide 27 — Controlling Query Granularity

This figure shows how MG-LVR controls query granularity.

The pipeline finds useful clips and builds a relation graph. Isolated moments
support fine-grained queries, while related clip groups support broader queries.
Granularity and collision checks keep each query grounded and distinct.

This creates a benchmark where the amount and location of evidence can support
controlled scaling analysis.

## Slide 28 — The Granularity Gap

This is the main benchmark finding. With eight frames, coarse retrieval remains
strong, but fine-grained retrieval is much lower. Increasing the frame count by
sixteen times gives only a modest fine-grained improvement.

So adding more frames at test time does not remove the gap. The model must also
use the extra evidence. This motivates the scaling analysis.

## Slide 29 — Two Scaling Analyses

MG-LVR supports two different analyses.

Test-time scaling changes the evidence seen during inference. We vary the tokens
kept for each frame and the number of sampled frames.

Training-time scaling changes the learned embedding. We train the same
architecture at different sampling densities and test both matched and
mismatched settings.

Using the same benchmark for both phases helps separate an input-evidence effect
from a learned-representation effect.

## Slide 30 — Test-Time Spatial Density

Here the frame count is fixed at thirty-two, and only the tokens per frame
change.

The curves do not show one universal rule. Some models benefit from more spatial
detail, while others plateau. The response also differs across query
granularities.

Higher spatial density is therefore not always better. Its value depends on the
architecture and the query.

## Slide 31 — Test-Time Temporal Density

Here we change the number of frames.

Multimodal language models can improve up to about one hundred and twenty-eight
frames, especially on fine-grained queries that need dense temporal evidence.
CLIP-based models often plateau much earlier and may even degrade when more
frames are averaged together.

So more frames help only when the architecture can integrate them. Temporal
coverage and representation design must be considered together.

## Slide 32 — Spatiotemporal Trade-Off

This slide keeps the total visual-token budget fixed.

Coarse queries usually prefer more spatial detail and fewer frames because
scene-level cues matter. Fine-grained queries prefer more frames because the
main risk is missing a short event.

At the same cost, the best allocation depends on query granularity. There is no
single setting for every query.

## Slide 33 — Training-Time Spatial Scaling

Now I move to training-time representation.

The same architecture is trained at several spatial densities and tested across
the same settings. High-density training transfers well to sparse spatial
input. Training with four hundred tokens per frame gives the best overall result
in every test group, but the gain becomes smaller at the highest density.

Spatial embeddings are therefore fairly robust to resolution change.

## Slide 34 — Training-Time Temporal Scaling

The temporal result is different.

We train with four, eight, sixteen, or thirty-two frames and test both matched
and mismatched frame counts. Performance usually peaks near the training frame
count. A mismatch can lower retrieval in both directions, especially for
fine-grained queries.

This means that dense temporal training does not automatically transfer to
sparse inference. The frame count becomes an anchor in the learned
representation. This finding directly motivates VEterfall.

## Slide 35 — VEterfall

VEterfall transfers dense knowledge to sparse input step by step.

A frozen dense teacher first supervises a medium-density student. That student
then becomes the teacher for a sparser model. The architecture stays the same.

Mean squared error preserves the video embedding, and InfoNCE keeps video-text
alignment. After two rounds, the input-token budget is sixteen times smaller.
Dense embeddings therefore help improve sparse-input representations.

## Slide 36 — Progressive Transfer Results

This table reports the original model and two transfer stages at three matched
input densities.

Please focus on the direction, not every decimal. The first stage gives the main
medium-density gain. The second carries much of it to the sparse setting. Fine
and medium queries benefit most, while coarse retrieval stays broadly stable.

Progressive transfer improves sparse-input performance without changing the
architecture.

## Slide 37 — Study 2 Summary

Study 2 also follows a clear chain.

MG-LVR combines long videos, multi-granular queries, and controlled sampling.
The analysis shows a large granularity gap, different spatial and temporal
responses, spatial robustness, and temporal frame-count anchoring.

That last asymmetry motivates VEterfall. A dense checkpoint teaches a sparser
checkpoint step by step. So the benchmark does not only report a problem. Its
analysis directly leads to the method design.

## Slide 38 — Study 3: Search Scaling

The third study is about search scaling. After learning a useful relevance
signal, we must search a very large catalog and serve many queries together.

The question is whether this signal can be followed on a graph and executed
efficiently on GPUs. I will present the setting, the three challenges, GMP-GR,
and the offline and online evidence.

## Slide 39 — From Catalog to Candidates

Retrieval narrows a billion-scale catalog before ranking.

The goal is to return the top-K items with the highest learned relevance without
scoring every item. Approximate nearest neighbor search moves through a graph
and scores only promising candidates.

The relevance model, graph path, and online execution must work together. The
next slide separates these three parts.

## Slide 40 — Three Coupled Challenges

There are three connected challenges. Related user behaviors should be modeled
together, not with isolated relevance models. A strong learned score may still
create poor graph paths, so search needs enough depth and breadth. Many queries
also create small and irregular scoring jobs, making GPU launches expensive.

This leads to one problem: co-design relevance learning, graph traversal, and
GPU execution.

## Slide 41 — GMP-GR Framework

GMP-GR has one offline stage and two connected online stages.

Offline, MUIRML learns one relevance model from multiple user behaviors. It also
adds a soft ordering signal for graph search.

Online, C-HiPANNS uses several starting paths within each query to broaden
exploration. Q-HiPANNS collects scoring jobs across concurrent queries and forms
GPU-friendly batches.

The same relevance model is therefore used from training, through traversal, to
online execution.

## Slide 42 — MUIRML and SCL

MUIRML learns related user behaviors with one model. It predicts an interaction
vector for behaviors such as click and browse, then attention combines the
vector into one relevance score.

Self-Covariant Loss, or SCL, adds a soft ordering regularizer. It encourages a
graph-friendly relative order while keeping the prediction objective. It is an
empirical regularizer, not a formal metric guarantee.

## Slide 43 — Two Levels of Parallel Search

HiPANNS uses two levels of parallelism.

C-HiPANNS works within one query. Several seeded searches share candidates and
broaden graph exploration. Q-HiPANNS works across queries. It collects small
scoring jobs, forms bounded batches, and sends them to the GPU.

One part improves exploration. The other reduces irregular GPU work.

## Slide 44 — Deployment and System Optimization

The system is reported across more than twenty Baidu applications.

Compilation simplifies the serving graph and improves throughput. Quantization
reduces the model from thirty-two-bit to sixteen-bit and gives another gain.
Streaming updates keep user and item embeddings fresh.

These results support practical deployment, but exact numbers still depend on
the hardware and serving setting.

## Slide 45 — Offline Evaluation

The offline evaluation uses four real-world video datasets and measures
coverage, recall, and time cost.

GMP-GR improves coverage on all four datasets and gives a favorable coverage
and time-cost trade-off among the tested settings. It also improves Recall at
ten on the video dataset.

The detailed values remain on the slide.

## Slide 46 — Online A/B Evaluation

The online A/B test covers two production video services.

Both services show positive time-on-page and daily-active-user results. The
component study also shows separate gains from MUIRML and HiPANNS.

This supports the value of the full framework under the reported production
configuration. The evidence boundary is important: the controlled A/B table
covers two services, while the wider deployment is reported across more than
twenty applications.

## Slide 47 — Study 3 Summary

Study 3 co-designs three layers.

MUIRML learns one multi-relational relevance signal. SCL makes its relative
order more useful for graph navigation. C-HiPANNS broadens search within a
query, and Q-HiPANNS batches irregular work across queries.

The lesson is that retrieval accuracy alone is not enough. The learned signal
must remain searchable and executable at web scale.

## Slide 48 — Conclusion and Future Work

I will now connect the three studies and return to the guiding question.

The conclusion has three parts. First, I will show how the stages depend on one
another. Second, I will summarize what scaled and what evidence supports the
claims. Third, I will discuss future directions and the main limitations.

## Slide 49 — Three Connected Retrieval Constraints

The studies protect three requirements in order.

Semantic scaling asks what can be represented across different retrieval
settings. Observational scaling asks what evidence is seen under limited frames
and tokens. Search scaling asks how the signal is preserved through graph
traversal and high-concurrency serving.

Together, they form a path from representation, through observation, to
large-corpus search.

## Slide 50 — What Scaled and What Generalized

This table gives the evidence across the three stages.

Study 1 tests query forms and domains across sixteen datasets. Study 2 tests
frame and token densities across three query granularities. Study 3 tests large
catalogs and reported production settings with offline and online evidence.

Generalizability has a different test at each stage, but every test goes beyond
one optimized condition.

## Slide 51 — Why This Thesis Matters for Video Retrieval

This thesis gives a grounded way to study scalable and generalizable video
retrieval. It separates capability coverage, limited visual evidence, and
large-corpus search, then gives each bottleneck a matching design and
evaluation.

Video is a useful real-world setting because queries are diverse, evidence may
be brief, and the corpus keeps growing. This links retrieval to multimodal
models, long-term memory, and changing data.

## Slide 52 — Retrieval-Native Multimodal Foundation Models

The first direction is to make retrieval part of the multimodal foundation
model. Current models mainly learn generation, and retrieval is added later.

A future model could use a retrieval token, route, or adapter while keeping
generation ability. The open question is how to produce compact retrieval
states without hurting generation. Both functions should be evaluated together.

## Slide 53 — Video Retrieval as Long-Term Agent Memory

The second direction is long-term visual memory for agents.

An agent may need to find where an object was last seen or retrieve a rare event
from hours of video. Semantic scaling supports different memory queries.
Observational scaling decides what enters memory. Search scaling keeps the
growing index available under latency.

Evaluation should include task success, decision time, and sparse-event recall.

## Slide 54 — Self-Evolving Data, Evaluation, and Curriculum

The third direction is a closed data and training loop.

Evaluation first finds a new capability gap. A synthesis system creates targeted
examples. The curriculum changes the training distribution, and the updated
model is evaluated again.

The goal is to adapt when query forms, video domains, and relevance conditions
change. An important open problem is retention: the model should repair new
gaps without forgetting abilities that it already learned.

## Slide 55 — Limitations and Open Questions

There are three main limitations.

The studies isolate three stages rather than test the full pipeline end to end.
UVRD and MG-LVR partly use synthesized or caption-based supervision, so stronger
human and natural-data validation is needed. GMP-GR is validated in one
industrial stack, and absolute speed may change elsewhere.

These limits define next steps for integration, validation, and system transfer.

## Slide 56 — Closing and Questions

To conclude, scalable video retrieval needs stage-specific design.

Study 1 scales capability coverage. Study 2 scales the visual evidence available
to the model. Study 3 scales learned relevance to large-corpus search.

Together, the three studies provide a path toward video retrieval systems that
are both scalable and generalizable.

Thank you very much for your time and attention. I am happy to take your
questions.

## Slide 57 — Appendix

This appendix keeps selected supporting evidence for the three studies and a
short set of prepared committee questions.

## Slide 58 — UVRB Protocol and Selected Results

This backup slide gives the common UVRB evaluation protocol and selected
ability-level results across representative models.

## Slide 59 — UVRB Radar and Correlation Findings

This backup slide shows the task-level radar view and the main correlation
findings that support the gap-targeted data design.

## Slide 60 — MG-LVR Context and 128-Frame Results

This backup slide gives the MG-LVR benchmark context and shows that the
fine-grained and coarse-grained gap remains visible even with 128 frames.

## Slide 61 — VEterfall Efficiency

This backup slide compares frame and token efficiency. It shows where
dense-to-sparse transfer helps most and where coarse retrieval stays stable.

## Slide 62 — MG-LVR Error Analysis

This backup slide separates missing temporal evidence from partial
semantic-constraint matching, so not every fine-grained error is blamed on
sampling.

## Slide 63 — GMP-GR Offline Results and Ablation

This backup slide contains the full offline results and shows that removing
either MUIRML or HiPANNS lowers the reported metrics.

## Slide 64 — Production Traffic and Latency

This backup slide shows anonymized production traffic and latency traces, with
the boundary that another platform or workload may behave differently.

## Slide 65 — Prepared Committee Questions

This final backup slide records short answers to six likely questions about
model choice, audit size, benchmark validity, method composition, SCL, and
deployment transfer.
