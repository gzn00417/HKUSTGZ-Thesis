import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

// Committee-review stage of the consolidated v0.5 build. The script preserves the
// existing template and figures, moves one correlation slide to backup, and
// applies exact-match text edits so source-deck drift fails loudly.

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) continue;
    const key = arg.slice(2);
    if (key === "ordered") out.ordered = true;
    else out[key] = argv[++i];
  }
  return out;
}

function records(ndjson) {
  return String(ndjson || "")
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

async function loadArtifactTool() {
  try {
    return await import("@oai/artifact-tool");
  } catch (error) {
    const roots = String(process.env.NODE_PATH || "")
      .split(path.delimiter)
      .filter(Boolean);
    for (const root of roots) {
      const entry = path.join(root, "@oai", "artifact-tool", "dist", "artifact_tool.mjs");
      try {
        await fs.access(entry);
        return await import(pathToFileURL(entry).href);
      } catch {
        // Try the next NODE_PATH root.
      }
    }
    throw new Error(
      "Cannot load @oai/artifact-tool. Install it locally or set NODE_PATH to the Codex bundled node_modules directory.",
      { cause: error },
    );
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.source || !args.output) {
    throw new Error("Usage: node slides/v0.5-build/committee-review.mjs --source <base.pptx> --output <reviewed.pptx> [--ordered]");
  }

  const source = path.resolve(args.source);
  const output = path.resolve(args.output);
  const { FileBlob, PresentationFile } = await loadArtifactTool();
  const presentation = await PresentationFile.importPptx(await FileBlob.load(source));

  if (!args.ordered) {
    // Move v0.5 slide 21 after A1-6, preserving every source slide exactly once.
    presentation.slides.getItem(20).moveTo(63);
  }

  const baseSnapshot = await presentation.inspect({
    kind: "slide,textbox,shape",
    maxChars: 2_000_000,
  });
  const index = new Map();
  for (const record of records(baseSnapshot.ndjson)) {
    if (!Number.isInteger(record.slide) || typeof record.text !== "string") continue;
    const key = `${record.slide}\u0000${record.text}`;
    if (!index.has(key)) index.set(key, []);
    index.get(key).push(record);
  }

  async function findExact(slideNumber, oldText) {
    const key = `${slideNumber}\u0000${oldText}`;
    let matches = index.get(key) || [];
    if (matches.length === 0) {
      const focused = await presentation.inspect({
        kind: "textbox,shape,table",
        search: oldText,
        maxChars: 20_000,
      });
      matches = records(focused.ndjson).filter(
        (record) => record.slide === slideNumber && record.text === oldText,
      );
    }
    if (matches.length !== 1) {
      throw new Error(
        `Expected one exact text match on slide ${slideNumber}, found ${matches.length}: ${JSON.stringify(oldText)}`,
      );
    }
    return matches[0];
  }

  async function replaceExact(slideNumber, oldText, newText) {
    const record = await findExact(slideNumber, oldText);
    const target = presentation.resolve(record.id);
    target.text.replace(oldText, newText);
  }

  async function setExact(slideNumber, oldText, newText) {
    const record = await findExact(slideNumber, oldText);
    const target = presentation.resolve(record.id);
    target.text = newText;
  }

  async function replaceNoteExact(slideNumber, oldText, newText) {
    const focused = await presentation.inspect({
      kind: "notes",
      search: oldText,
      maxChars: 20_000,
    });
    const matches = records(focused.ndjson).filter(
      (record) => record.slide === slideNumber && record.text === oldText,
    );
    if (matches.length !== 1) {
      throw new Error(
        `Expected one exact note match on slide ${slideNumber}, found ${matches.length}: ${JSON.stringify(oldText)}`,
      );
    }
    presentation.resolve(matches[0].id).text = newText;
  }

  // Main-talk page markers shift after moving the former slide 21 to backup.
  for (let slide = 21; slide <= 55; slide += 1) {
    await replaceExact(slide, String(slide - 1), String(slide - 2));
  }
  // Existing A2/A3/Q&A slides become B8-B22 after inserting the new A1-7/B7.
  for (let slide = 65; slide <= 79; slide += 1) {
    await replaceExact(slide, `B${slide - 58}`, `B${slide - 57}`);
  }

  const edits = [
    [1,
      "“How can video retrieval stay generalizable as semantic capability, visual observation, and search scale all grow?”",
      "“How can video retrieval scale in semantic capability, visual observation, and large-corpus search without losing generalizability?”"],

    [2, "Measure granularity → derive scaling laws → distill VEterfall",
      "Measure granularity → characterize scaling laws → distill dense knowledge into sparse inference"],
    [2, "Regularize metric → parallelize graph/GPU search → deploy GMP-GR",
      "Regularize metric → parallelize graph traversal and GPU execution → deploy GMP-GR"],
    [2, "Structure-aware scaling → stage-specific evidence → future work",
      "Unify the findings → delimit the evidence → future directions"],

    [3, "Why is video retrieval a pipeline-level scaling problem, and what does structure-aware scaling look like?",
      "Why does video retrieval become a pipeline-level scaling problem, and how does structure-aware scaling address it?"],

    [4, "Search, recommendation, and discovery all reduce to matching a query to a video corpus.",
      "Search, recommendation, and discovery depend on matching information needs to relevant video."],
    [4, "Surface relevant long-form content under strict latency.",
      "Surface relevant content from large, dynamic catalogs under strict latency."],
    [4, "As corpora, query forms, and serving traffic all grow, retrieval stops being a single benchmark task and becomes a pipeline-level scaling problem — the subject of this thesis.",
      "As video corpora grow in size and duration, query forms diversify, and serving constraints tighten, retrieval becomes a pipeline-level scaling problem rather than a single benchmark task."],

    [5, "Two axes of universality", "Capability space"],
    [5, "A model may excel on one axis (e.g. text–video) yet fail on composed, visual-only, or partially-relevant retrieval — leaderboards hide this.",
      "A model may excel on one capability yet fail on composed, visual-only, or partially relevant retrieval; aggregate leaderboard scores can obscure these gaps."],
    [5, "Studies 1–2 target text/visual→video retrieval; Study 3 targets web-scale user→item retrieval under the same searchable-signal principle.",
      "Studies 1–2 examine textual, visual, and composed query-to-video retrieval. Study 3 instantiates the same search-scaling problem in production user-to-item retrieval."],

    [6, "Capability gaps across query forms/types",
      "Capability gaps across query and relevance types"],
    [6, "Evidence gaps under limited frame/token budgets",
      "Evidence gaps under limited frame/token budgets"],
    [6, "Metric–graph–GPU incompatibility at scale",
      "Metric–graph mismatch and GPU execution bottlenecks"],
    [6, "Takeaway   Generalizability is the evidence that scaling has addressed the right bottleneck.",
      "Takeaway   Generalizability is the empirical criterion for whether scaling has addressed the right bottleneck."],

    [7, "More parameters, more frames, or higher offline AUC each hit a different wall.",
      "More parameters, more frames, or a more expressive neural metric each hit a different wall."],
    [7, "Fine recall barely moves with 16× more frames",
      "Fine R@1: 0.210 → 0.287\nwith 16× more frames"],
    [7, "Higher offline\nmetric AUC", "More expressive\nneural metric"],
    [7, "Neural metrics break greedy graph traversal",
      "Neural metrics can violate graph-search regularity"],

    [8, "Each study delivers a diagnosis, a method, and generalization evidence.",
      "Each study provides a bottleneck diagnosis, a structure-aware intervention, and stage-specific evidence."],
    [8, "•  MG-LVR: 9,971 queries over 4,844 long videos (706 s)\n•  Spatiotemporal scaling laws for frame/token budgets\n•  VEterfall: +20% fine-grained at 4–16× efficiency",
      "•  MG-LVR: 9,971 queries over 4,844 long videos (706 s)\n•  Spatiotemporal scaling laws for frame/token budgets\n•  VEterfall: up to +20% Fine R@1 under 4–16× lower-density inference"],

    [10, "Takeaway   Semantic scaling means covering the capabilities that matter, not just topping one leaderboard.",
      "Takeaway   Semantic scaling broadens coverage across query formats and relevance conditions, not one benchmark."],

    [11, "UVRB: One Protocol to Diagnose 14 Models on 16 Datasets",
      "UVRB: One Protocol Across 16 Datasets and 14 Baselines"],
    [11, "UVRB unifies 16 public datasets into one evaluation space with six capability labels.",
      "UVRB organizes 16 public datasets into one unified capability space."],
    [11, "•  87M → 8.3B parameters\n•  CLIP- & MLLM-based families\n•  GME · UNITE · VLM2Vec · UniME · B3",
      "•  87M → 8.3B parameters\n•  CLIP- & MLLM-based families\n•  GME · Unite · VLM2Vec-V2 · UniME · B3"],
    [11, "Maps the capability a model is missing — not just its leaderboard rank.",
      "Maps which capabilities each model lacks, not merely its aggregate rank."],

    [12, "Weaknesses track the training distribution and cluster on the same hard skills.",
      "Capability gaps cluster on recurring hard skills rather than disappearing with model scale."],
    [12, "Temporal, composed, and partial-relevance retrieval stay weak across all 14 models — even at 8.3B parameters.",
      "Temporal, composed, and partial-relevance retrieval remain among the weakest axes across evaluated models."],
    [12, "Gaps can be diagnosed and targeted, not scaled away by size.",
      "These systematic gaps can be diagnosed and targeted; parameter scaling alone does not remove them."],

    [13, "PR predicts universality", "PR is the strongest UVR proxy"],
    [13, "Partial-relevance retrieval correlates with overall UVR far more than MSR-VTT (ρ ≈ 0.58) — a lightweight universality proxy.",
      "PR has the highest average correlation with overall UVR (ρ ≈ 0.97), compared with ρ ≈ 0.58 for MSR-VTT."],
    [13, "Spatial ⟂ Temporal", "Spatial ↔ Temporal"],
    [13, "Spatial and temporal skills are near-independent; temporal drives fine-grained recall (ρ ≈ 0.98), spatial does not (ρ ≈ 0.39).",
      "Spatial and temporal abilities correlate weakly across models (ρ ≈ 0.12); temporal ability is strongly correlated with fine-grained performance (ρ ≈ 0.98)."],

    [14, "A three-stage pipeline synthesizes exactly the skills diagnosis flagged as weak.",
      "A three-stage pipeline targets the capability gaps revealed by UVRB."],
    [14, "① Quality control", "① Annotation rectification & filtering"],
    [14, "Filter web video by quality, cross-modal consistency, and temporal dynamics.",
      "Correct annotations; remove cross-modally inconsistent or temporally static samples."],
    [14, "② Information enrichment", "② Gap-targeted enrichment"],
    [14, "MLLM captioning skewed to under-represented temporal & spatial skills.",
      "Generate captions under a 60% temporal / 30% spatial / 10% partial-or-abstract profile."],
    [14, "③ Task extension", "③ Multimodal task extension"],
    [14, "Synthesize composed and visual tasks covering all UVRB dimensions.",
      "Construct textual, visual, and composed retrieval pairs."],

    [15, "Sample audit", "Preliminary audit"],
    [15, "Factual accuracy on a 100-sample human audit; downstream gains confirm quality at scale.",
      "95% factual accuracy in a preliminary 100-instance human audit."],
    [15, "UVRD is not designed for size alone: its distribution directly targets the capability gaps UVRB diagnosed.",
      "UVRD targets diagnosed capability gaps rather than size alone; downstream gains provide complementary evidence of utility."],

    [16, "Qwen2.5-VL MLLM · LoRA fine-tuning · last-token pooling + ℓ2 norm.",
      "Qwen2.5-VL · language-module LoRA · frozen vision/token embeddings · last-token pooling + ℓ2 norm"],
    [16, "ℒ = −log  exp(s⁺/τ)\n———————————\nΣ exp(s/τ) + Σ exp(s⁻/τ)",
      "ℒ = ½ ( ℒq→v + ℒv→q )"],
    [16, "Align matched pairs against in-batch + mined hard negatives (τ = 0.03), symmetrized q↔v.",
      "Symmetric InfoNCE uses in-batch positives and mined hard negatives in both directions (τ = 0.03)."],

    [17, "A difficulty-ordered schedule prevents gradient interference across tasks.",
      "A difficulty-ordered curriculum mitigates gradient submergence across heterogeneous tasks."],
    [17, "Alignment-aware scheduling",
      "Higher Rₖ⁽ᵗ⁾ = easier task; rising σ(t) broadens sampling"],
    [17, "P⁽ᵗ⁾(k) ∝ exp( R_k / σ(t) )",
      "P⁽ᵗ⁾(k) ∝ exp( Rₖ⁽ᵗ⁾ / σ(t) )"],

    [18, "GVE Improves Zero-Shot Retrieval Generalization",
      "GVE Leads Zero-Shot Generalization Across UVRB"],
    [18, "vs Unite-7B, over 8 abilities.",
      "vs Unite-7B, averaged over six main categories."],
    [18, "Takeaway   Capability-targeted data lifts a smaller model above a larger baseline.",
      "Takeaway   Capability-targeted data and curriculum allow GVE-3B to outperform the larger Unite-7B baseline."],

    [19, "Composed, long-context, and temporal — exactly the capabilities diagnosis identified as under-served.",
      "Composed, long-context, and temporal show the largest gains among the diagnosed weak skills."],
    [19, "Targeted synthesis raises the diagnosed weak skills without sacrificing the strong ones.",
      "Targeted synthesis improves the diagnosed weak skills while keeping most other abilities competitive."],

    [20, "Targeted data and ordered training each contribute; together they compound.",
      "Targeted data and ordered training provide complementary gains."],
    [20, "UVRD lifts overall R@1 by +2.3% and composed retrieval by +27% relative; the Modality Pyramid curriculum adds further ordering gains on top — diagnosis → data → curriculum is additive.",
      "UVRD raises Dataset AVG from 0.528 to 0.537 and CMP from 0.237 to 0.301 (+27% relative). The Modality Pyramid further raises Dataset AVG to 0.544 and Ability AVG to 0.571."],
    [20, "Each component targets a distinct part of the semantic bottleneck.",
      "UVRD broadens capability coverage; the Modality Pyramid improves heterogeneous-task optimization."],
    [20, "Takeaway   Diagnosis → targeted data → curriculum: three additive levers on the semantic bottleneck.",
      "Takeaway   Targeted data and ordered training address complementary parts of the semantic bottleneck."],

    [21, "Inter-Ability Correlations Reveal Decoupled Representations",
      "Inter-Ability Correlations Reveal a Spatial–Temporal Gap"],
    [21, "Spatial and temporal skills are learned independently; temporal drives fine-grained recall.",
      "Spatial and temporal abilities are weakly correlated; temporal aligns with fine-grained retrieval."],
    [21, "Spatial ⟂ Temporal", "Spatial ↔ Temporal"],
    [21, "ρ ≈ 0.12 across both families — spatial and temporal representations are learned independently, not as a single 'fine-grained' skill.",
      "Spatial and temporal abilities are weakly correlated across evaluated models (ρ ≈ 0.12)."],
    [21, "Temporal → FG", "Temporal ↔ FG"],
    [21, "Temporal ability correlates ρ ≈ 0.98 with fine-grained recall; spatial only ρ ≈ 0.39. Current models fail to jointly model when and where.",
      "Temporal ability is strongly associated with fine-grained retrieval (ρ ≈ 0.98), whereas spatial ability is less strongly associated (ρ ≈ 0.39)."],
    [21, "Partial-relevance retrieval achieves ρ ≈ 0.97 with overall UVR — the most reliable proxy for universal capability, yet understudied.",
      "Partial-relevance retrieval has the highest correlation with overall UVR (ρ ≈ 0.97), making it the strongest evaluated proxy."],

    [22, "Per 10× data: GVE-3B gains +7.4% vs. +5.4% for GVE-7B, while GVE-7B retains higher absolute performance.",
      "Per 10× data, Dataset AVG gains +7.4% (GVE-3B) vs. +5.4% (GVE-7B); Ability AVG gains are +7.1% vs. +5.4%."],
    [22, "Takeaway   Semantic scaling depends on training data volume as well as model capacity, with diminishing returns.",
      "Takeaway   Data scaling is approximately log-linear with diminishing returns; GVE-3B has the steeper relative slope."],

    [23, "A retrieval embedding generalizes to classification with no task-specific tuning.",
      "Mean zero-shot classification accuracy provides transfer evidence beyond retrieval benchmarks."],
    [23, "Retrieval-trained geometry is genuinely general, not benchmark-specific.",
      "The learned embedding shows transfer beyond the retrieval benchmarks used for evaluation."],
    [23, "Averaged over K700, UCF101, HMDB51, SSV2, and Breakfast: capability-guided retrieval training yields embeddings that transfer beyond retrieval itself.",
      "Mean accuracy over K700, UCF101, HMDB51, SSV2, and Breakfast: capability-guided retrieval training yields embeddings that transfer beyond retrieval."],

    [24, "GVE reaches 0.573 dataset-AVG and 0.600 ability-AVG (SOTA zero-shot across 16 datasets), with GVE-3B already beating the 7B baseline.",
      "GVE reaches 0.573 Dataset AVG and 0.600 Ability AVG (SOTA zero-shot across 16 datasets), with GVE-3B outperforming the larger Unite-7B baseline."],

    [26, "one 706-second video", "average MG-LVR video: 706 seconds"],
    [26, "If the relevant moment is never sampled, retrieval fails before modeling even begins — and encoding every frame of an hour-long video is infeasible.",
      "If the relevant moment is not sampled, the required visual evidence is unavailable to the model, and exhaustive full-frame encoding is computationally prohibitive."],
    [26, "How does sampling density interact with query granularity? Standard benchmarks never isolate this, so it has stayed unmeasured — the gap MG-LVR fills.",
      "Short-clip benchmarks rarely isolate the interaction between sampling density and query granularity; MG-LVR is designed to expose it."],

    [27, "G is the fraction of a video that is relevant — from one moment to the whole clip.",
      "G is the fraction of a video that is relevant, from a brief moment to whole-video coverage."],
    [27, "several segments · G ∈ [0.1, 0.3]",
      "a moderate fraction · G ∈ [0.1, 0.3]"],

    [28, "Takeaway   MG-LVR is the first benchmark to vary query granularity across long videos: see A2-1 for statistics.",
      "Takeaway   MG-LVR is the first long-video benchmark spanning three granularities and both continuity types."],

    [29, "MG-LVR Benchmark Construction",
      "Clip Relation Graphs Discover Multi-Granular Retrieval Units"],

    [30, "Under sparse sampling, coarse queries are easy and fine queries collapse.",
      "Under sparse sampling, coarse queries remain much easier than fine-grained queries."],
    [30, "broad themes are easy to match", "broad themes remain easier to match"],
    [30, "16× more frames lifts fine R@1 by < 8 points — naive frame scaling cannot close the gap.",
      "16× more frames improve Fine R@1 by only 7.7 percentage points (0.210 → 0.287)."],
    [30, "Takeaway   Fine-grained retrieval fails under sparse sampling and barely recovers with more frames.",
      "Takeaway   Fine-grained retrieval remains strongly observation-limited under naive frame scaling."],

    [31, "MLLMs keep improving with frames; CLIP-style models saturate, then degrade.",
      "MLLM-based models generally improve with more frames; CLIP-style models often plateau or degrade."],
    [31, "Saturate near 16 frames, then degrade: mean-pooling dilutes the signal as frames grow.",
      "Often plateau near 16 frames and may degrade, consistent with signal dilution under mean pooling."],
    [31, "More frames help only architectures that can actually use them.",
      "More frames help only architectures that can effectively integrate them."],

    [32, "Spatial and temporal tokens are not interchangeable; allocation must follow granularity.",
      "At the same total token budget, coarse queries favor spatial detail, whereas fine-grained queries favor temporal coverage."],

    [33, "Training at high spatial resolution transfers to low-resolution inference — models trained at 400 tokens still lead when tested at 50 tokens.",
      "Training at 400 spatial tokens transfers to 50-token inference, improving Overall R@1 by 0.0155 over direct 50-token training."],
    [33, "Temporal ability peaks when the inference frame count matches training; a train-32 / test-4 mismatch loses fine-grained recall, and vice-versa.",
      "Temporal ability peaks near matched frame counts; train-32 / test-4 lowers Fine R@1 by 0.0104 relative to matched train-4 / test-4."],
    [33, "Sparse inference must inherit dense-trained temporal skill — not relearn it.",
      "This train–test density mismatch motivates explicit dense-to-sparse knowledge transfer."],

    [34, "Skill for low-density inference is latent in dense models but does not transfer automatically — VEterfall distills it explicitly, one step at a time (λ = 0.5, K = 2, 16× fewer tokens).",
      "Knowledge for low-density inference is latent in high-density models but does not transfer automatically; VEterfall distills it step by step (λ = 0.5, K = 2, 16× fewer tokens)."],

    [35, "VEterfall Recovers Fine-Grained Sparse Performance",
      "VEterfall Improves Fine-Grained Retrieval at the Same Sparse Budget"],
    [35, "Takeaway   Dense-trained temporal skill is recovered under a 16× smaller token budget.",
      "Takeaway   Dense-trained knowledge improves Fine R@1 from 0.132 to 0.158 under a 16× smaller token budget."],

    [36, "Extra spatial tokens add little; coarse queries can even suffer token redundancy.",
      "Additional spatial tokens yield diminishing or occasionally negative returns, especially for coarse queries."],

    [37, "Fine-grained retrieval drops > 75% under sparse sampling; VEterfall recovers +20% at 4–16× efficiency by transferring dense knowledge to sparse inference.",
      "Fine-grained R@1 drops by more than 75% under sparse sampling; VEterfall improves it by up to 20% relative under 4–16× lower-density inference."],

    [38, "Chapter 5 · published at ACM Web Conference 2026",
      "Chapter 5 · published at The Web Conference 2026"],

    [39, "Web-Scale Retrieval: Reduce Billions to Candidates",
      "Web-Scale Retrieval: Reduce Billions to a Candidate Set"],
    [39, "GPU serving\n< 10 ms", "GPU-parallel\nserving"],
    [39, "Study 3 tests the deployment layer shared by embedding-based retrieval: making a learned signal compatible with graph and GPU execution, using user-item retrieval as the production setting.",
      "Study 3 instantiates search scaling in a production recommendation setting, where users serve as queries and content items as candidates."],

    [40, "Ranking can be inconsistent with distance, so greedy traversal stalls in local optima and misses relevant items — accuracy gains are lost at search time.",
      "Ranking can be inconsistent with distance, so greedy traversal can stall in local optima and miss relevant items; accuracy gains may be lost at search time."],
    [40, "Transplant Euclidean ranking regularity into the learned metric — accuracy and searchability hold together.",
      "Regularize the learned metric toward Euclidean ranking consistency so relevance and searchability improve together."],

    [41, "Accurate and searchable: SCL enforces rank–distance consistency.",
      "SCL encourages rank–distance consistency."],
    [41, "Multi-seed parallel traversal widens the search space, escaping traps.",
      "Multi-seed traversal broadens exploration and reduces local traps."],
    [41, "Query batching, compilation, and quantization cut latency.",
      "Batched queries, compilation, and quantization increase throughput."],

    [42, "A lightweight DNN predicts a multi-interaction relevance δ(u, v) from concatenated user/item features (with a serendipity term), capturing behaviors a single dot-product cannot.",
      "A lightweight DNN predicts multi-relational user–item relevance from the joint interaction vector, including a serendipity component."],
    [42, "Takeaway   SCL transfers Euclidean ranking regularity to the learned metric for more efficient graph navigation.",
      "Takeaway   SCL softly aligns learned ranking with Euclidean structure, improving graph searchability."],

    [43, "•  k parallel searches per query with different seeds\n•  Share one K-size max-heap across processes\n•  k-fold search-space expansion escapes local optima → higher recall",
      "•  k parallel searches per query with different seeds\n•  Share one K-size max-heap across processes\n•  k-fold expansion reduces local-trap risk → higher recall"],
    [43, "C-HiPANNS broadens the search for accuracy while Q-HiPANNS batches computation for speed — the graph and GPU layers reinforce, rather than trade off against, each other.",
      "C-HiPANNS broadens graph exploration for recall; Q-HiPANNS batches irregular neural computation for throughput."],

    [44, "Recall vs. latency — GMP-GR sits on the efficient frontier.",
      "Coverage vs. time cost — GMP-GR lies on the efficient frontier."],
    [44, "Takeaway   Consistent coverage gains across all four Baidu recommendation datasets.",
      "Takeaway   GMP-GR improves Coverage consistently across all four evaluated Baidu recommendation datasets."],

    [45, "Two live services show consistent, significant engagement gains.",
      "Two online A/B services show consistent engagement gains."],
    [45, "Retrieval gains matter only when relevance improves without latency regression — which these online tests confirm.",
      "The online results show that relevance improvements can be delivered within the serving latency budget."],

    [46, "Streaming index updates keep embeddings current under dynamic catalogs; two services supported by five servers in total sustain production-scale traffic within the P99 latency budget.",
      "Streaming index updates keep embeddings current under dynamic catalogs; two services supported by five servers in total sustain production-scale traffic within the serving latency budget."],

    [47, "GMP-GR raises coverage +20.9% and Recall@10 +22.7% while improving throughput, and lifts engagement +1.13%/+1.19% time-on-page in two online A/B services.",
      "GMP-GR improves Coverage by 12.7–24.9% across four datasets and Recall@10 by 22.7% on Video while increasing throughput, then lifts time-on-page by +1.13%/+1.19% in two online A/B services."],

    [49, "Takeaway   Scalable and generalizable video retrieval requires structure-aware scaling across semantic capability, visual observation, and search execution.",
      "Takeaway   Scalable, generalizable retrieval needs structure-aware scaling across semantic, observation, and search stages."],

    [50, "The three studies test transfer under different but complementary conditions.",
      "The three studies evaluate whether gains persist beyond the narrow condition directly optimized."],
    [50, "+20% fine-grained recall over the\nsparse baseline at 4–16× efficiency",
      "+20% Fine R@1 over the sparse baseline\nunder 4–16× lower-density inference"],

    [51, "These boundaries define where structure-aware scaling should be extended next — the frontier, not weaknesses.",
      "These boundaries define the next research steps for extending structure-aware scaling."],

    [52, "Retrieval should be built into the model, not extracted from generation states.",
      "Retrieval objectives should be integrated into multimodal models rather than added only after generative pretraining."],
    [52, "Generative objective\n(today's MLLM)", "Generative objective\n(current MLLMs)"],

    [53, "Agents need memory that spans long visual histories. Casting retrieval as the memory interface — over past observations, object locations, and event context — turns the embedding and search machinery of this thesis into the substrate for embodied and multimodal agents.",
      "Agents need memory that spans long visual histories. Casting retrieval as the memory interface over past observations, object locations, and event context would turn video retrieval into a long-term memory layer for embodied and multimodal agents."],

    [54, "↺   re-evaluate on new evidence", "↺   Re-evaluate on new evidence"],

    [55, "The three studies correspond to three papers and reusable research artifacts.",
      "The three thesis studies are associated with three research papers and reusable artifacts."],
    [55, "Universal Video Retrieval via\nGeneral Video Embedding",
      "Towards Universal Video Retrieval"],
    [55, "Multi-Granularity Long-Video\nRetrieval & Scaling Laws",
      "Demystifying Spatiotemporal\nScaling Laws"],
    [55, "Searchable Learned Metrics for\nWeb-Scale Retrieval",
      "GPU-accelerated Multi-relational\nParallel Graph Retrieval"],
    [55, "Published · ACM WebConf 2026",
      "Published · The Web Conference 2026"],

    [57, "A1  Study 1 · GVE\n       Protocol · radar · full results · training dynamics · test-time scaling · data scaling\n\nA2  Study 2 · MG-LVR\n       Construction · 128-frame results · VEterfall efficiency · spatial @32F · error analysis\n\nA3  Study 3 · GMP-GR\n       Full offline results · ablation (4 metrics) · efficiency curves · deployment evidence\n\nA4  Q&A\n       Six prepared committee questions",
      "A1  Study 1 · GVE\n       Protocol · radar · full results · training dynamics · test/data scaling · correlations\n\nA2  Study 2 · MG-LVR\n       Construction · 128-frame results · VEterfall efficiency · spatial @32F · error analysis\n\nA3  Study 3 · GMP-GR\n       Full offline results · ablation (4 metrics) · efficiency curves · deployment evidence\n\nA4  Q&A\n       Six prepared committee questions"],

    [59, "No single model covers all tasks. The radar surface area correlates with UVR generalizability (ρ ≈ 0.97 for PR as proxy). Targeted data closes specific spokes.",
      "No model dominates every task. PR has the highest correlation with overall UVR (ρ ≈ 0.97), making it the strongest single proxy among evaluated abilities. Targeted data improves several diagnosed weak spokes."],

    [60, "By-ability averages across six UVRB dimensions; GVE-7B leads the overall ability average.",
      "Three query formats, three main domains, and three subdomains; AVG averages the six main categories."],

    [61, "Four metrics tracked across training; curriculum prevents gradient submergence.",
      "Four metrics tracked across training; curriculum mitigates gradient submergence."],

    [62, "Temporal scaling is a robust strategy; naive spatial scaling is not. Performance depends on effective token composition, not merely total input volume — motivating adaptive token selection.",
      "For GVE, temporal scaling benefits long-context retrieval more consistently, while spatial scaling shows an architecture- and budget-dependent optimum."],

    [64, "Introduction", "APPENDIX"],
    [64, "Semantic Scaling", "A1 · GVE"],
    [64, "Observational", "CORRELATION"],
    [64, "Search Scaling", "EVIDENCE"],
    [64, "Conclusion", "BACKUP"],
    [64, "19", "B7"],
    [64, "Correlation Analysis Explains the Capability Structure",
      "A1-7  UVRB Correlations with Overall Performance"],
    [64, "Partial relevance predicts universality; spatial and temporal skills are decoupled.",
      "PR is the strongest overall proxy; spatial and temporal abilities are weakly correlated."],
    [64, "Correlation of each ability with overall UVR performance (and with training-data mix).",
      "Correlation of each ability and dataset with overall UVR performance."],
    [64, "PR ↔ universality", "PR ↔ overall UVR"],
    [64, "Partial-relevance retrieval has the highest correlation with overall UVR (ρ ≈ 0.97).",
      "PR has the highest average correlation with overall UVR performance (ρ ≈ 0.97)."],
    [64, "Spatial ⟂ Temporal", "Spatial ↔ Temporal"],
    [64, "Spatial and temporal abilities correlate only ρ ≈ 0.12 — learned separately.",
      "Spatial and temporal abilities are weakly correlated across evaluated models (ρ ≈ 0.12)."],
    [64, "Temporal → fine-grained", "Temporal ↔ fine-grained"],
    [64, "Temporal ability drives fine-grained recall (ρ ≈ 0.98); spatial does not (ρ ≈ 0.39).",
      "Temporal is strongly associated with fine-grained retrieval (ρ ≈ 0.98); spatial is weaker (ρ ≈ 0.39)."],

    [65, "Prior long-video work either fixes one granularity (LoVR/MSR-VTT) or covers only short clips (ActivityNet). MG-LVR spans all granularities across 706-second videos, making the coarse–fine gap measurable rather than assumed.",
      "Prior benchmarks use shorter videos or a single long-video granularity. MG-LVR spans all granularities across 706-second videos."],
    [65, "Low-connection nodes and Louvain communities discover single- and multi-clip units; G and C then categorize granularity and continuity.",
      "Low-connection nodes and Louvain communities discover single- and multi-clip units; G and C label granularity and continuity."],

    [68, "MLLMs degrade beyond their training token distribution — extra spatial tokens exceed the context window the model was distilled on, hurting performance.",
      "The degradation likely reflects mismatch with the spatial-token distribution seen during training."],

    [69, "Sparse sampling fragments the temporal chain — the model never sees enough of any single continuous event.",
      "Sparse sampling fragments the temporal chain; required visual evidence may never be observed."],

    [70, "Both failure modes stem from the same observation bottleneck: sparse sampling creates evidence gaps that no model architecture can compensate for at inference time. This motivates VEterfall's dense-to-sparse distillation strategy.",
      "Both failure modes stem from the same observation bottleneck: no model can reliably recover visual evidence that was never observed. This motivates VEterfall's dense-to-sparse distillation strategy."],

    [71, "GMP-GR retrieves 321K items/s on Video — fastest among DNN-based methods. C-NSW is faster only by dropping to a lightweight cosine metric with far lower coverage.",
      "GMP-GR retrieves 321K items/s on Video, fastest among DNN-based methods. C-NSW is faster only with a lower-coverage cosine metric."],

    [72, "All four metrics degrade when either MUIRML (metric) or HiPANNS (graph/GPU) is removed — joint co-design is necessary. Recall@100 confirms the coverage trend at looser recall targets; ItemPerS confirms that HiPANNS graph-parallelism is the throughput bottleneck, not just the metric.",
      "All four metrics degrade when either MUIRML or HiPANNS is removed. Recall@100 follows the coverage trend; ItemPerS shows that replacing HiPANNS with HNSW substantially reduces retrieval speed."],

    [73, "QPS vs. Coverage frontier — GMP-GR Pareto-dominates NANN on every corpus.",
      "Coverage vs. time frontier — GMP-GR lies above NANN across evaluated operating points."],
    [73, "Pareto dominance", "Efficient frontier"],
    [73, "Across all four corpora and all QPS operating points, GMP-GR achieves higher coverage than NANN — with equal or greater throughput. The improvement is universal, not dataset-specific.",
      "Across evaluated operating points on all four corpora, GMP-GR consistently achieves higher Coverage than NANN."],

    [74, "Per-service traces confirm P99 compliance and stable throughput under real load.",
      "Per-service traces show how latency varies with real production traffic."],
    [74, "Service 1: arrival rate + P99 latency (24 h).",
      "Service 1: traffic–latency distribution."],
    [74, "Service 2: same metrics, independent service.",
      "Service 2: same metrics, independent service."],
    [74, "Both services: diurnal 3–5× load swing; HiPANNS holds P99 < 10 ms throughout.",
      "Both services show changing load; latency rises with traffic, with server-specific patterns."],

    [75, "Server traces split latency into graph-traversal and scoring stages.",
      "Server-level distributions reveal heterogeneous load and latency across five servers."],
    [75, "Server-level latency breakdown: graph traversal vs. scoring stage.",
      "Server-level latency distributions for two production services."],
    [75, "Graph traversal is the dominant latency contributor; HiPANNS's GPU parallelism reduces it to < 4 ms, leaving scoring as the secondary component.",
      "Traffic and latency vary across servers and services, reflecting heterogeneous resources and workload allocation."],

    [76, "A3-6  Production Query-Level Traffic and P99 Latency",
      "A3-6  Production Query-Level Traffic and Latency"],
    [76, "Anonymized query traces validate sustained P99 compliance across an extended window.",
      "Anonymized query traces show traffic and latency over an extended production window."],
    [76, "End-to-end P99 latency; SLA of < 10 ms is met throughout.",
      "End-to-end latency over one day under real query traffic."],
    [76, "Traffic follows a diurnal pattern with a 3–5× peak-to-trough ratio; HiPANNS maintains stable P99 latency throughout the window, validating GPU-parallel throughput under real production load.",
      "Traffic follows a clear diurnal pattern, while latency varies with load across the day. Together, the traces provide deployment evidence under real production traffic."],
    [76, "Service-level traces (A3-4) show per-service breakdown. This slide shows the query-level view — same P99 guarantee, coarser aggregation.",
      "Service-level traces (A3-4) show per-service latency–traffic relations; this slide provides the temporal view over a longer window."],

    [77, "A 100-sample audit has a wide confidence interval, which we acknowledge. The functional proof is downstream: consistent zero-shot gains across 16 UVRB datasets — systematic noise would not produce broad, cross-dataset improvements.",
      "A 100-sample audit has a wide confidence interval, which we acknowledge. Broad zero-shot gains across 16 UVRB datasets provide complementary evidence of usefulness, but they do not replace a larger human audit."],

    [78, "The gap persists across all 23 evaluated models and both continuity types. Its cause is structural — sparse sampling misses brief frame-level evidence — and short-clip benchmarks simply mask it.",
      "The gap persists across all 23 evaluated models and both continuity types. This consistency supports a structural observation-bottleneck interpretation: sparse sampling frequently misses brief evidence."],
    [78, "Q3 · Is the granularity gap a benchmark artifact? — Universal across 23 models",
      "Q3 · Is the granularity gap a benchmark artifact? — Consistent across 23 models"],

    [79, "SCL constrains ranking order, not raw score magnitudes. It aligns output ranking with Euclidean distance to remove degenerate graph-navigation cases while preserving fine-grained relevance — regularizing relative order, not absolute expressiveness.",
      "SCL regularizes ranking order, not raw score magnitudes. It softly aligns learned ranking with Euclidean distance to discourage graph-navigation failures while preserving fine-grained relevance."],

    [79, "The core logic is HNSW-compatible and architecture-agnostic, so accuracy gains transfer. Absolute throughput depends on hardware and traffic — we separate universal algorithmic value from platform-specific engineering numbers.",
      "The metric–graph co-design is portable in principle to other HNSW-based systems, but both accuracy and throughput must be revalidated under each platform's data, hardware, and traffic distribution."],
  ];

  for (const [slideNumber, oldText, newText] of edits) {
    await replaceExact(slideNumber, oldText, newText);
  }

  // Rich-text bullet boxes do not reliably persist text.replace() on export.
  await setExact(8,
    "•  MG-LVR: 9,971 queries over 4,844 long videos (706 s)\n•  Spatiotemporal scaling laws for frame/token budgets\n•  VEterfall: +20% fine-grained at 4–16× efficiency",
    "•  MG-LVR: 9,971 queries over 4,844 long videos (706 s)\n•  Spatiotemporal scaling laws for frame/token budgets\n•  VEterfall: up to +20% Fine R@1 under 4–16× lower-density inference");
  await setExact(11,
    "•  87M → 8.3B parameters\n•  CLIP- & MLLM-based families\n•  GME · UNITE · VLM2Vec · UniME · B3",
    "•  87M → 8.3B parameters\n•  CLIP- & MLLM-based families\n•  GME · Unite · VLM2Vec-V2 · UniME · B3");

  // The complete notes pass is deferred, but remove three known unsupported
  // production guarantees so no factual error remains in the delivered file.
  await replaceNoteExact(74,
    "Service-level traces: both services meet P99 < 10 ms SLA under real diurnal load.",
    "Service-level traces show latency–traffic relations for two services supported by five servers.");
  await replaceNoteExact(75,
    "Server-level breakdown: graph traversal dominates. HiPANNS reduces it to < 4 ms.",
    "Server-level distributions show heterogeneous traffic and latency across five servers and two services.");
  await replaceNoteExact(76,
    "Query-level trace: diurnal pattern, 3-5x peak ratio. HiPANNS holds P99 < 10 ms throughout.",
    "Query-level traces show diurnal traffic and time-varying latency under production load.");

  const tableInspection = await presentation.inspect({
    kind: "table",
    search: "Stage",
    maxChars: 10_000,
  });
  const synthesisTables = records(tableInspection.ndjson).filter(
    (record) => record.slide === 49 && record.kind === "table",
  );
  if (synthesisTables.length !== 1) {
    throw new Error(`Expected the synthesis table on slide 49, found ${synthesisTables.length}.`);
  }
  const synthesisTable = presentation.resolve(synthesisTables[0].id);
  synthesisTable.cells.set(3, 1, "More expressive neural relevance metric");

  const appendixTableInspection = await presentation.inspect({
    kind: "table",
    search: "Family",
    maxChars: 10_000,
  });
  const appendixTables = records(appendixTableInspection.ndjson).filter(
    (record) => record.slide === 58 && record.kind === "table",
  );
  if (appendixTables.length !== 1) {
    throw new Error(`Expected the model-family table on slide 58, found ${appendixTables.length}.`);
  }
  const appendixTable = presentation.resolve(appendixTables[0].id);
  appendixTable.cells.set(3, 2, "Broadest overall capability coverage");
  appendixTable.cells.set(3, 3, "Depends on high-quality synthesis and curriculum design");

  await fs.mkdir(path.dirname(output), { recursive: true });
  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(output);
  console.log(JSON.stringify({ source, output, slides: presentation.slides.items.length, edits: edits.length }));
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exitCode = 1;
});
