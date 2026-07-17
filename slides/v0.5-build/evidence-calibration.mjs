import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

// Evidence-boundary stage of the consolidated v0.5 build.
// This pass preserves the inherited slide order, layout, figures, and tables.

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) continue;
    out[arg.slice(2)] = argv[++i];
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
      "Cannot load @oai/artifact-tool. Install it locally or set NODE_PATH to the bundled node_modules directory.",
      { cause: error },
    );
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.source || !args.output) {
    throw new Error("Usage: node slides/v0.5-build/evidence-calibration.mjs --source <reviewed.pptx> --output <new-output.pptx>");
  }

  const source = path.resolve(args.source);
  const output = path.resolve(args.output);
  if (source === output) throw new Error("Source and output must use different filenames.");
  try {
    await fs.access(output);
    throw new Error(`Refusing to overwrite existing output: ${output}`);
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }

  const { FileBlob, PresentationFile } = await loadArtifactTool();
  const presentation = await PresentationFile.importPptx(await FileBlob.load(source));
  if (presentation.slides.items.length !== 79) {
    throw new Error(`Expected 79 slides, found ${presentation.slides.items.length}.`);
  }

  const snapshot = await presentation.inspect({
    kind: "slide,textbox,shape,notes",
    maxChars: 2_000_000,
  });
  const index = new Map();
  for (const record of records(snapshot.ndjson)) {
    if (!Number.isInteger(record.slide) || typeof record.text !== "string") continue;
    const key = `${record.slide}\u0000${record.text}`;
    if (!index.has(key)) index.set(key, []);
    index.get(key).push(record);
  }

  async function findExact(slideNumber, oldText, kind = null) {
    const key = `${slideNumber}\u0000${oldText}`;
    const matches = (index.get(key) || []).filter((record) => !kind || record.kind === kind);
    if (matches.length !== 1) {
      throw new Error(
        `Expected one exact ${kind || "text"} match on slide ${slideNumber}, found ${matches.length}: ${JSON.stringify(oldText)}`,
      );
    }
    return matches[0];
  }

  async function replaceExact(slideNumber, oldText, newText) {
    const record = await findExact(slideNumber, oldText);
    presentation.resolve(record.id).text.replace(oldText, newText);
  }

  async function setExact(slideNumber, oldText, newText) {
    const record = await findExact(slideNumber, oldText);
    presentation.resolve(record.id).text = newText;
  }

  async function setNoteExact(slideNumber, oldText, newText) {
    const record = await findExact(slideNumber, oldText, "notes");
    presentation.resolve(record.id).text = newText;
  }

  const edits = [
    [8,
      "•  UVRB: unified diagnosis, 16 datasets × 14 models\n•  V-SynFlow → UVRD: 1.55M capability-targeted pairs\n•  GVE: SOTA zero-shot generalization (0.573 / 0.600)",
      "•  UVRB: unified diagnosis, 16 datasets × 14 evaluated baselines\n•  V-SynFlow → UVRD: 1.55M capability-targeted pairs\n•  GVE: SOTA zero-shot generalization (0.573 / 0.600)"],
    [8,
      "•  MG-LVR: 9,971 queries over 4,844 long videos (706 s)\n•  Spatiotemporal scaling laws for frame/token budgets\n•  VEterfall: up to +20% Fine R@1 under 4–16× lower-density inference",
      "•  MG-LVR: 9,971 queries over 4,844 long videos (706 s)\n•  Spatiotemporal scaling laws for frame/token budgets\n•  VEterfall: up to +20% Fine R@1 under 4–16× lower input-token budgets"],

    [15, "95%", "95 / 100"],
    [15, "95% factual accuracy in a preliminary 100-instance human audit.",
      "95 of 100 instances were judged factually accurate in a preliminary human audit."],

    [16, "Symmetric InfoNCE uses in-batch positives and mined hard negatives in both directions (τ = 0.03).",
      "Symmetric InfoNCE uses cross-device in-batch negatives and mined hard negatives in both directions (τ = 0.03)."],

    [17, "Pyramid: easy atomic alignment → text-video → composed retrieval.",
      "Empirical difficulty spans T2T 0.68 → TV2V 0.43, motivating bottom-up ordering."],

    [22, "GVE Data Scaling Follows a Logarithmic Law",
      "GVE Shows Task-Dependent, Approximately Log-Linear Data Scaling"],
    [22, "More training data improves both model sizes, with diminishing returns.",
      "Over the evaluated range, more data improves both model sizes, but rates differ by task."],
    [22, "Takeaway   Data scaling is approximately log-linear with diminishing returns; GVE-3B has the steeper relative slope.",
      "Takeaway   Scaling is task-dependent: GVE-3B gains faster on most abilities, while GVE-7B uniquely benefits more on long context."],

    [23, "GVE-7B matches a specialist 6B video model, zero-shot.",
      "GVE-7B matches InternVideo2-6B in mean zero-shot accuracy (0.526)."],
    [23, "Mean accuracy over K700, UCF101, HMDB51, SSV2, and Breakfast: capability-guided retrieval training yields embeddings that transfer beyond retrieval.",
      "Mean accuracy over five datasets. GVE is not trained on these datasets; baseline pretraining exposure is not controlled."],

    [34, "Per-step distillation objective", "Primary MSE + auxiliary InfoNCE"],
    [34, "Knowledge for low-density inference is latent in high-density models but does not transfer automatically; VEterfall distills it step by step (λ = 0.5, K = 2, 16× fewer tokens).",
      "VEterfall progressively distills high-density embeddings into lower-density inference. MSE provides the main gain; InfoNCE adds a small, consistent regularization effect (λ = 0.5, K = 2)."],

    [35, "The +20% relative fine-grained gain is measured over the sparse baseline (V⁰) at the same 4F–100T budget: VEterfall improves sparse inference by transferring dense knowledge at 4–16× efficiency — not by outperforming the dense teacher directly.",
      "The +20% relative Fine R@1 gain is measured over V⁰ at the same 4F–100T budget. This deployment uses 16× fewer input tokens than the 16F–400T teacher; it is not a measured 16× latency gain."],
    [35, "Takeaway   Dense-trained knowledge improves Fine R@1 from 0.132 to 0.158 under a 16× smaller token budget.",
      "Takeaway   Two-stage distillation raises Fine R@1 from 0.132 to 0.158 at 4F–100T; one stage alone gives 0.130."],

    [37, "Fine-grained R@1 drops by more than 75% under sparse sampling; VEterfall improves it by up to 20% relative under 4–16× lower-density inference.",
      "Fine-grained R@1 drops by more than 75% under sparse sampling; VEterfall improves it by up to 20% relative at 4–16× lower input-token budgets."],

    [42, "A multi-relational metric, regularized to preserve graph-search regularity.",
      "A multi-relational metric, softly aligned with a distance-derived geometric ordering."],
    [42, "ρ(u,v) = Σ (δ − δ̄)(δ′ − δ̄′)\n————————————————\nVAR(δ) · VAR(δ′)",
      "ρ(δ,g) = Σ (δ − δ̄)(g − ḡ)\n———————————————\nVAR(δ) · VAR(g)"],
    [42, "ℒ  =  Σ ‖ Z − Ẑ ‖₂   +   Σ  1 / ( ρ + 1 )         ( δ = learned relevance,  δ′ = Euclidean distance )",
      "ℒ  =  Σ ‖ Z − Ẑ ‖₂   +   Σ  1 / ( ρ + 1 )       ( δ = learned relevance; g = distance-derived geometric reference )"],
    [42, "Takeaway   SCL softly aligns learned ranking with Euclidean structure, improving graph searchability.",
      "Takeaway   SCL is a soft ranking regularizer; the thesis supports its searchability effect empirically, not as a formal metric guarantee."],

    [45, "The online results show that relevance improvements can be delivered within the serving latency budget.",
      "The online results show measurable engagement gains under the reported production serving configuration."],
    [45, "A searchable learned signal delivers measurable, latency-safe engagement gains in production.",
      "A searchable learned signal delivers measurable engagement gains in two production A/B services."],

    [46, "Streaming index updates keep embeddings current under dynamic catalogs; two services supported by five servers in total sustain production-scale traffic within the serving latency budget.",
      "Streaming index updates keep embeddings current under dynamic catalogs; the reported deployment covers two services supported by five servers in total."],

    [50, "+20% Fine R@1 over the sparse baseline\nunder 4–16× lower-density inference",
      "+20% Fine R@1 over the sparse baseline\nunder 4–16× lower input-token budgets"],

    [58, "Frozen embeddings, one protocol, 14 models across two families.",
      "Frozen embeddings, one protocol, 14 evaluated baselines across two families."],
    [59, "Each spoke is one retrieval task; gaps reveal which capabilities models structurally miss.",
      "Each spoke is one retrieval task; gaps show which capabilities remain weak across evaluated baselines."],
    [59, "Per-task radar: 14 models across TXT/CMP/VIS × CG/FG/LC × PR.",
      "Per-task radar: 14 evaluated baselines across TXT/CMP/VIS × CG/FG/LC × PR."],

    [61, "Four metrics tracked across training; curriculum mitigates gradient submergence.",
      "Four diagnostics track optimization behavior for both GVE model sizes."],
    [61, "Without the Modality Pyramid, complex temporal and composed tasks are submerged by simpler spatial alignment tasks in early epochs. The curriculum stabilizes multi-task training by ordering tasks from atomic to composite.",
      "These traces monitor loss and positive/negative alignment during training. They do not isolate the curriculum effect; schedule evidence is reported separately in the thesis appendix."],

    [63, "Each capability scales at its own rate; temporal and composed gain most per data decade.",
      "Each UVRB ability has a distinct data-scaling profile across the evaluated range."],
    [63, "Fast-scaling abilities", "Most abilities favor GVE-3B"],
    [63, "Temporal (T) and Composed (CMP) show steep log-linear gains — they benefit most from the targeted synthesis in UVRD.",
      "CMP gains 14.7% per data decade for GVE-3B vs. 8.7% for GVE-7B; CG, TXT, and FG show the same smaller-model advantage."],
    [63, "Saturation signal", "Exception and limit"],
    [63, "Visual-only (VIS) and Coarse (CG) plateau earliest, consistent with the parameter-scaling limitation: parameter count matters less than capability diversity.",
      "VIS scales weakly for both sizes. Only long-context retrieval favors GVE-7B in both absolute and relative gain."],

    [66, "Even with 16× more frames, the coarse–fine gap persists across 23 models.",
      "At 128-frame inference, the coarse–fine gap remains across 23 evaluated models."],
    [66, "Best fine R@1 is still 0.287 vs 0.903 coarse — the observation bottleneck is structural, not a capacity issue.",
      "Best Fine R@1 is 0.287 vs. 0.903 Coarse; the gap is not removed by the evaluated model scales or families."],
    [66, "Temporal ability peaks when inference frames match training; a train-32 / test-4 mismatch measurably lowers fine-grained recall — see Chapter 4 scaling tables.",
      "Temporal performance generally peaks at matched or nearby train–test frame counts; a train-32 / test-4 mismatch lowers Fine R@1 relative to train-4 / test-4."],

    [67, "Distillation gains hold under both frame and token compression.",
      "Distillation mainly improves Overall and Fine retrieval in the sparse regime."],
    [67, "Reducing frames or tokens with VEterfall beats the un-distilled model at the same budget; the advantage widens as the budget tightens (λ = 0.5, K = 2 distillation rounds).",
      "At 8F and 4F, and at 400T and 100T, distillation improves Overall and Fine R@1. Coarse is nearly stable, with small declines in the token sweep."],

    [70, "Fine-grained needle-in-a-haystack and partial semantic satisfaction under sparse frames.",
      "Temporal misses and partial semantic matches expose related but distinct limitations."],
    [70, "Shared root cause", "Interpretation boundary"],
    [70, "Both failure modes stem from the same observation bottleneck: no model can reliably recover visual evidence that was never observed. This motivates VEterfall's dense-to-sparse distillation strategy.",
      "Type 2 directly reflects an observation gap. Type 3 can combine missing evidence with incomplete semantic-constraint matching; it should not be attributed to sampling alone."],

    [73, "Coverage vs. time frontier — GMP-GR lies above NANN across evaluated operating points.",
      "GMP-GR shows the strongest observed Coverage–time trade-off among evaluated method configurations."],
    [73, "Efficient frontier", "Observed trade-off"],
    [73, "Across evaluated operating points on all four corpora, GMP-GR consistently achieves higher Coverage than NANN.",
      "Each plotted method is one reported configuration. Across four corpora, GMP-GR occupies a favorable Coverage–time position relative to NANN."],

    [78, "The gap persists across all 23 evaluated models and both continuity types. This consistency supports a structural observation-bottleneck interpretation: sparse sampling frequently misses brief evidence.",
      "The gap persists across all 23 evaluated models and both continuity types, supporting an observation-bottleneck interpretation within MG-LVR. Its magnitude may still depend on benchmark construction and relevance annotation."],

    [79, "Q5 · Does SCL hurt DNN metric expressiveness? — Soft rank regularizer",
      "Q5 · What does SCL guarantee? — Soft ranking regularizer, empirical evidence"],
    [79, "SCL regularizes ranking order, not raw score magnitudes. It softly aligns learned ranking with Euclidean distance to discourage graph-navigation failures while preserving fine-grained relevance.",
      "SCL aligns learned ordering with a distance-derived geometric reference. The thesis reports empirical search gains; it does not establish a formal triangle-inequality guarantee for the learned DNN score."],
  ];

  for (const [slideNumber, oldText, newText] of edits) {
    await replaceExact(slideNumber, oldText, newText);
  }

  // Preserve the rich-text bullet styling on the roadmap while replacing the
  // complete bullet box, which is more reliable than run-level replacement.
  await setExact(8,
    "•  UVRB: unified diagnosis, 16 datasets × 14 models\n•  V-SynFlow → UVRD: 1.55M capability-targeted pairs\n•  GVE: SOTA zero-shot generalization (0.573 / 0.600)",
    "•  UVRB: unified diagnosis, 16 datasets × 14 evaluated baselines\n•  V-SynFlow → UVRD: 1.55M capability-targeted pairs\n•  GVE: SOTA zero-shot generalization (0.573 / 0.600)");
  await setExact(8,
    "•  MG-LVR: 9,971 queries over 4,844 long videos (706 s)\n•  Spatiotemporal scaling laws for frame/token budgets\n•  VEterfall: up to +20% Fine R@1 under 4–16× lower-density inference",
    "•  MG-LVR: 9,971 queries over 4,844 long videos (706 s)\n•  Spatiotemporal scaling laws for frame/token budgets\n•  VEterfall: up to +20% Fine R@1 under 4–16× lower input-token budgets");

  const noteEdits = [
    [16, "GVE is one unified embedding model. Training is symmetric InfoNCE with hard negatives.",
      "GVE is one unified embedding model. Training uses symmetric InfoNCE with cross-device in-batch negatives and mined hard negatives."],
    [23, "GVE's embedding transfers to classification, matching InternVideo2-6B zero-shot.",
      "GVE-7B matches InternVideo2-6B in mean zero-shot classification accuracy. GVE is not trained on these datasets; baseline pretraining exposure is not controlled."],
    [34, "VEterfall is cascaded self-distillation: MSE to the denser teacher plus an InfoNCE anchor.",
      "VEterfall is cascaded self-distillation. MSE provides the primary signal; InfoNCE adds a small auxiliary regularization effect."],
    [35, "VEterfall lifts fine-grained R@1 ~20% over the sparse baseline at 4–16× efficiency.",
      "At 4F–100T, two-stage VEterfall raises Fine R@1 from 0.132 to 0.158 over the same-budget sparse baseline. The input-token budget is 16× lower than the 16F–400T teacher."],
    [45, "Two-service A/B: +1.13%/+1.19% time-on-page. Later deployed across 20+ apps. No p-values in source.",
      "Two-service A/B: +1.13%/+1.19% time-on-page under the reported production configuration. The broader system later served 20+ applications. No p-values or explicit latency threshold are reported."],
    [46, "System optimizations (compilation, quantization, streaming) make GMP-GR production-ready.",
      "Compilation, quantization, and streaming updates support the reported production deployment; the thesis does not state a numerical latency guarantee."],
    [58, "UVRB: one protocol, 14 models, two families. Gaps persist at 8.3B — scale alone is not enough.",
      "UVRB: one protocol, 14 evaluated baselines, two families. Gaps persist at 8.3B; parameter scaling alone does not remove them."],
    [59, "Per-task radar: task-level blind spots — no single model covers all. PR proxy validates capability diagnosis.",
      "Per-task radar: no evaluated model covers every task. PR's correlation with overall UVR supports the capability diagnosis."],
    [61, "Training dynamics: Modality Pyramid prevents gradient interference. Both model sizes benefit.",
      "Training diagnostics track optimization behavior for GVE-3B and GVE-7B. These traces alone are not a curriculum ablation."],
    [63, "Per-ability scaling: temporal/composed scale fastest. VIS/CG plateau — targeted data design confirmed.",
      "Per-ability scaling is task-dependent: GVE-3B gains faster on CMP, CG, TXT, FG, and VIS; GVE-7B uniquely gains more on LC. VIS scales weakly for both."],
    [66, "128F results: coarse–fine gap persists at 0.287 vs 0.903 — structural, not a capacity issue.",
      "At 128-frame inference, the best Fine R@1 remains 0.287 versus 0.903 Coarse. The gap is not removed by evaluated scales or model families."],
    [67, "VEterfall efficiency: distilled model beats baseline at every frame/token budget tested.",
      "VEterfall improves Overall and Fine R@1 in the sparse frame/token settings shown. Coarse remains close, with small declines in the token sweep."],
    [70, "Error Types 2+3: fine-grained miss and incomplete constraints — both caused by sparse observation.",
      "Type 2 is an observation miss. Type 3 also involves semantic-constraint matching and should not be attributed to sampling alone."],
    [73, "Efficiency on all 4 datasets: GMP-GR Pareto-dominates NANN on every corpus.",
      "Each method is shown as one evaluated configuration. GMP-GR has the strongest observed Coverage–time trade-off across the four corpora."],
    [78, "The gap persists across all 23 evaluated models and both continuity types. Its cause is structural — sparse sampling misses brief frame-level evidence — and short-clip benchmarks simply mask it. · Open future work. Hypothesis: a stronger dense teacher (GVE) yields higher-quality sparse distillation signals for VEterfall, improving fine-grained efficiency — a concrete cross-study experiment.",
      "The gap persists across all 23 evaluated models and both continuity types, supporting an observation-bottleneck interpretation within MG-LVR. Benchmark construction may still affect the magnitude. · GVE plus VEterfall remains an untested future hypothesis, not a demonstrated composition."],
    [79, "SCL constrains ranking order, not raw score magnitudes. It aligns output ranking with Euclidean distance to remove degenerate graph-navigation cases while preserving fine-grained relevance — regularizing relative order, not absolute expressiveness. · The core logic is HNSW-compatible and architecture-agnostic, so accuracy gains transfer. Absolute throughput depends on hardware and traffic — we separate universal algorithmic value from platform-specific engineering numbers.",
      "SCL is a soft ordering regularizer against a distance-derived geometric reference. The reported evidence is empirical and does not establish a formal metric guarantee. · The co-design is portable in principle, but accuracy and throughput must be revalidated for each platform's data, hardware, and traffic."],
  ];

  for (const [slideNumber, oldText, newText] of noteEdits) {
    await setNoteExact(slideNumber, oldText, newText);
  }

  const tableInspection = await presentation.inspect({
    kind: "table",
    search: "Representative models",
    maxChars: 10_000,
  });
  const modelFamilyTables = records(tableInspection.ndjson).filter(
    (record) => record.slide === 58 && record.kind === "table",
  );
  if (modelFamilyTables.length !== 1) {
    throw new Error(`Expected the model-family table on slide 58, found ${modelFamilyTables.length}.`);
  }
  presentation.resolve(modelFamilyTables[0].id).cells.set(
    2,
    1,
    "GME, Unite, VLM2Vec-V2, B3, UniME",
  );

  await fs.mkdir(path.dirname(output), { recursive: true });
  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(output);
  console.log(JSON.stringify({
    source,
    output,
    slides: presentation.slides.items.length,
    visibleEdits: edits.length,
    noteEdits: noteEdits.length,
  }));
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exitCode = 1;
});
