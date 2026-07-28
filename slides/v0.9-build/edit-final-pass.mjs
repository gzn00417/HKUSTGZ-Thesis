import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

// Historical exact editor for the V0.87 final pass promoted unchanged to V0.9.
// Restore the author-edited V0.86 source from Trash and provide SOURCE_PPTX
// explicitly if this transformation must be replayed.
const mode = process.env.MODE || "edit";
const workspace = path.resolve(
  process.env.WORKSPACE || "/private/tmp/thesis-v087.F3eMGx",
);
if (!process.env.SOURCE_PPTX) {
  throw new Error(
    "Set SOURCE_PPTX to the restored author-edited V0.86 source deck.",
  );
}
const sourcePptx = path.resolve(process.env.SOURCE_PPTX);
const starterPptx = path.resolve(
  process.env.STARTER_PPTX ||
    path.join(workspace, "template-starter.pptx"),
);
const outputPptx = path.resolve(
  process.env.OUTPUT_PPTX || "slides/thesis-slides-v0.9.pptx",
);
const frameMapPath = path.join(workspace, "template-frame-map.json");
const renderDir = path.join(workspace, "final-render");

const TNR = "Times New Roman";

const edits = [];

function edit(slide, name, newText, options = {}) {
  edits.push({ slide, name, newText, ...options });
}

function move(slide, name, position, reason) {
  edits.push({ slide, name, position, reason });
}

// Slide 5: make retrieval, corpus ranking, and the role of embeddings explicit.
edit(
  5,
  "TextBox 7",
  "Problem Formulation: Embedding-Based Video Retrieval",
  { reason: "Keep the page centered on the formal retrieval problem." },
);
edit(
  5,
  "TextBox 9",
  "Retrieval embeds the query and corpus, ranks candidates by similarity, and returns the top-K videos.",
  { reason: "State the full retrieval process before introducing secondary taxonomy." },
);

const slide5Geometry = [
  ["Rounded Rectangle 13", { left: 52.8, top: 190.08, width: 580.8, height: 147.63 }],
  ["Rectangle 14", { left: 54.72, top: 200.64, width: 8.64, height: 132.52 }],
  ["Rounded Rectangle 17", { left: 52.8, top: 361.51, width: 580.8, height: 110.4 }],
  ["Rectangle 18", { left: 54.72, top: 371.11, width: 8.64, height: 91.2 }],
  ["Rounded Rectangle 21", { left: 648, top: 190.08, width: 578.88, height: 281.83 }],
  ["Rectangle 22", { left: 649.92, top: 200.64, width: 8.64, height: 263.86 }],
  ["Rounded Rectangle 25", { left: 648, top: 499.29, width: 578.88, height: 139.2 }],
  ["Rectangle 26", { left: 649.92, top: 509.85, width: 8.64, height: 118.08 }],
  ["Rounded Rectangle 29", { left: 52.8, top: 499.29, width: 580.8, height: 139.2 }],
  ["Rectangle 30", { left: 54.72, top: 509.85, width: 8.64, height: 118.08 }],
];
for (const [name, position] of slide5Geometry) {
  move(
    5,
    name,
    position,
    "Retain the inherited V0.86 card geometry while repurposing its content.",
  );
}
edit(5, "TextBox 15", "1 · Embed the query", {
  position: { left: 77.76, top: 200.64, width: 544.32, height: 32.64 },
  reason: "Introduce query embedding as the first operation.",
});
edit(
  5,
  "TextBox 16",
  "q may be text, an image, a clip, or a composed query. The encoder maps it to zq = Eθ(q).",
  {
    position: { left: 77.76, top: 238.08, width: 536.64, height: 80.26 },
    reason: "Define the query and its embedding in one concise card.",
  },
);
edit(5, "TextBox 19", "2 · Compare embeddings", {
  position: { left: 77.76, top: 371.11, width: 542.4, height: 28.8 },
  reason: "Name the similarity operation.",
});
edit(
  5,
  "TextBox 20",
  "s(q, vᵢ) = cos(Eθ(q), Eθ(vᵢ))",
  {
    position: { left: 77.76, top: 419.27, width: 530.88, height: 27.52 },
    reason: "Show the relevance score used for ranking.",
  },
);
edit(5, "TextBox 23", "3 · Rank the video corpus", {
  position: { left: 672.96, top: 200.64, width: 542.4, height: 32.64 },
  reason: "Make corpus retrieval the dominant step on the page.",
});
edit(
  5,
  "TextBox 24",
  "Encode candidates offline: zᵢ = Eθ(vᵢ), i = 1…N.\n\nCompare the query with every candidate embedding.\n\nSort by similarity and return the top-K videos.",
  {
    position: { left: 672.96, top: 238.08, width: 534.72, height: 179.83 },
    reason: "Explain corpus encoding, matching, ranking, and return.",
  },
);
edit(5, "TextBox 27", "Retrieval output", {
  position: { left: 672.96, top: 509.85, width: 542.4, height: 32.64 },
  reason: "State what the retrieval system returns.",
});
edit(
  5,
  "TextBox 28",
  "The top-K highest-scoring candidates are the retrieved videos.",
  {
    position: { left: 672.96, top: 547.29, width: 534.72, height: 81 },
    reason: "Conclude the problem definition with the retrieval result.",
  },
);
edit(5, "TextBox 31", "Learning objective", {
  position: { left: 77.76, top: 509.85, width: 544.32, height: 27.52 },
  reason: "Replace secondary scope content with the objective that creates the retrieval space.",
});
edit(
  5,
  "TextBox 32",
  "For every relevant pair (q, v⁺), learn s(q, v⁺) > s(q, v⁻) for irrelevant candidates v⁻. Retrieval is therefore corpus ranking in the learned embedding space.",
  {
    position: { left: 77.76, top: 547.29, width: 536.64, height: 81.6 },
    reason: "State how training produces the ranking behavior used at retrieval time.",
  },
);

// Slide 6: establish the dependency relation among the three stages.
edit(6, "TextBox 7", "Why Scaling Splits into Three Successive Decisions", {
  reason: "Make the page answer why the three scaling problems exist.",
});
edit(
  6,
  "TextBox 9",
  "Retrieval must scale representation, visual evidence, and corpus search in sequence; each stage adds a new constraint.",
  { reason: "Explain the dependency chain in plain language." },
);
edit(6, "TextBox 14", "Semantic Scaling", {
  reason: "Retain the thesis stage terminology.",
});
edit(
  6,
  "TextBox 15",
  "Representation: cover query formats, domains, and relevance conditions.",
  { reason: "Define what semantic scaling changes." },
);
edit(6, "TextBox 16", "Observational Scaling", {
  reason: "Retain the thesis stage terminology.",
});
edit(
  6,
  "TextBox 17",
  "Observation: capture the query-relevant moment under a limited input budget.",
  { reason: "Define what observational scaling changes." },
);
edit(6, "TextBox 18", "Search Scaling", {
  reason: "Retain the thesis stage terminology.",
});
edit(
  6,
  "TextBox 19",
  "Retrieval: preserve learned relevance in billion-scale graph search and GPU serving.",
  { reason: "Define what search scaling changes." },
);
edit(
  6,
  "TextBox 23",
  "Research order   comprehensive representation → sufficient visual evidence → deployable large-corpus search.",
  { reason: "State why the three studies appear in this order." },
);

// Slide 7: keep only stage meaning, challenge, and high-level direction.
edit(7, "TextBox 7", "What Each Scaling Stage Means and Why It Is Hard", {
  reason: "Orient the committee to the methodological role of the page.",
});
edit(
  7,
  "TextBox 9",
  "Each stage scales a different object, fails for a different reason, and needs a different research direction.",
  { reason: "Summarize the comparison without prematurely naming detailed methods." },
);
edit(7, "TextBox 13", "Stage", {
  reason: "Retain the table row key.",
});
edit(7, "TextBox 14", "What is scaled?", {
  reason: "Replace the naive-scaling column with a direct definition.",
});
edit(7, "TextBox 15", "Core difficulty", {
  reason: "Focus the page on the challenge.",
});
edit(7, "TextBox 16", "Research direction", {
  reason: "Keep solutions high-level and defer method detail.",
});
edit(7, "Rounded Rectangle 17", "Semantic", {
  reason: "Use the concise stage label.",
});
edit(
  7,
  "Rounded Rectangle 18",
  "Query formats, domains,\nand relevance conditions",
  { reason: "Define the object of semantic scaling." },
);
edit(
  7,
  "Rounded Rectangle 19",
  "Generic model or data growth does not guarantee balanced capability coverage",
  { reason: "State the semantic-scaling difficulty at a general level." },
);
edit(
  7,
  "Rounded Rectangle 20",
  "Measure capabilities, then guide data and learning",
  { reason: "Give a direction without revealing the detailed Study 1 mechanism." },
);
edit(7, "Rounded Rectangle 21", "Observation", {
  reason: "Use the concise stage label.",
});
edit(
  7,
  "Rounded Rectangle 22",
  "Frames and spatial tokens\nprovided to the encoder",
  { reason: "Define the object of observational scaling." },
);
edit(
  7,
  "Rounded Rectangle 23",
  "Useful evidence depends on video length, query granularity, and architecture",
  { reason: "State the observational-scaling difficulty." },
);
edit(
  7,
  "Rounded Rectangle 24",
  "Analyze allocation, then transfer dense knowledge to sparse inputs",
  { reason: "Give the Study 2 direction while preserving later method detail." },
);
edit(7, "Rounded Rectangle 25", "Search", {
  reason: "Use the concise stage label.",
});
edit(
  7,
  "Rounded Rectangle 26",
  "Candidate-set size and\nserving concurrency",
  { reason: "Define the object of search scaling." },
);
edit(
  7,
  "Rounded Rectangle 27",
  "Accurate relevance may still be hard to traverse and execute efficiently",
  { reason: "State the search-scaling difficulty." },
);
edit(
  7,
  "Rounded Rectangle 28",
  "Co-design relevance, graph traversal, and GPU execution",
  { reason: "Give the Study 3 direction without low-level method detail." },
);

// Slide 8: overview the three studies and make their dependency explicit.
edit(8, "TextBox 7", "Thesis Overview: Three Studies, One Dependency Chain", {
  reason: "Make the cross-study relationship the page's primary message.",
});
edit(
  8,
  "TextBox 9",
  "Representation enables observation analysis; reliable visual evidence enables deployment-scale search.",
  { reason: "Explain the research order before listing the studies." },
);
edit(
  8,
  "TextBox 16",
  "•  Question: Can one embedding cover heterogeneous query formats, domains, and relevance conditions?\n\n•  Study response: unified evaluation → targeted synthesis → curriculum-trained GVE\n\n•  Enables next: a representation worth testing when visual observation is limited",
  { reason: "Frame Study 1 by question, response, and dependency." },
);
edit(
  8,
  "TextBox 20",
  "•  Question: Which visual evidence must be observed for long, multi-granular retrieval?\n\n•  Study response: controlled scaling analysis → dense-to-sparse transfer\n\n•  Enables next: reliable relevance signals under deployable input budgets",
  { reason: "Frame Study 2 by question, response, and dependency." },
);
edit(
  8,
  "TextBox 24",
  "•  Question: Can those relevance signals be searched over billion-scale corpora?\n\n•  Study response: co-design metric learning, graph traversal, and GPU execution\n\n•  Completes the chain: accurate and deployable large-corpus retrieval",
  { reason: "Frame Study 3 as the final retrieval stage." },
);

// Slide 13: categorize the synthesized corpus by query format and domain coverage.
edit(13, "TextBox 7", "UVRD: Cross-Domain Data for Three Query Formats", {
  reason: "Make the taxonomy, rather than the raw size, the page's organizing idea.",
});
edit(
  13,
  "TextBox 9",
  "The 1.55M pairs vary both query format and the video evidence to be matched.",
  { reason: "Summarize the two coverage axes for a fast presentation pass." },
);
edit(13, "TextBox 14", "TXT", {
  reason: "Use the thesis query-format taxonomy.",
});
edit(13, "TextBox 15", "Textual query", {
  reason: "Label the first query format.",
});
edit(
  13,
  "TextBox 16",
  "Natural-language text retrieves a video or image.\nTasks: T2V · T2I · T2T",
  { reason: "Explain the textual-query supervision contained in UVRD." },
);
edit(13, "TextBox 18", "VIS", {
  reason: "Use the thesis query-format taxonomy.",
});
edit(13, "TextBox 19", "Visual query", {
  reason: "Label the second query format.",
});
edit(
  13,
  "TextBox 20",
  "A reference frame or clip retrieves a target video.\nTasks: I2V · V2V",
  { reason: "Explain the visual-query supervision contained in UVRD." },
);
edit(13, "TextBox 22", "CMP", {
  reason: "Use the thesis query-format taxonomy.",
});
edit(13, "TextBox 23", "Composed query", {
  reason: "Label the third query format.",
});
edit(
  13,
  "TextBox 24",
  "Text plus an image or video specifies the target.\nTasks: TI2V · TV2V",
  { reason: "Explain the composed-query supervision contained in UVRD." },
);
edit(13, "TextBox 28", "Coverage at a glance", {
  reason: "Merge the former design-principle aside into a compact coverage summary.",
});
edit(
  13,
  "TextBox 29",
  "Domains: coarse-grained · fine-grained · long-context. Fine-grained cases include spatial, temporal, and partially relevant evidence. Scale: 1.55M multi-task pairs.",
  { reason: "State domain coverage and corpus scale without a separate underfilled section." },
);

// Slide 15: add the motivation, measured difficulty, adaptive schedule, and novelty.
edit(15, "TextBox 7", "Modality Pyramid: Alignment-Aware Curriculum", {
  reason: "Name the technical mechanism directly.",
});
edit(
  15,
  "TextBox 9",
  "Alignment-aware scheduling prevents interference and moves from foundational to harder tasks.",
  { reason: "Make the optimization motivation explicit." },
);
edit(
  15,
  "TextBox 14",
  "Evidence & novelty\nOne-epoch alignment reveals a hierarchy (T2I 0.65 > T2V 0.46 > TV2V 0.43). Re-estimating task alignment from the evolving GVE checkpoint makes the curriculum adaptive rather than fixed.",
  {
    position: { left: 70.08, top: 528, width: 544.32, height: 124.8 },
    reason: "Use the lower-left region for evidence and the method's adaptive novelty.",
    boldRanges: ["Evidence & novelty"],
  },
);
move(
  15,
  "Rounded Rectangle 15",
  { left: 639.83, top: 205.94, width: 580.8, height: 124.88 },
  "Retain the inherited first method card for the alignment estimator.",
);
move(
  15,
  "Rectangle 16",
  { left: 641.75, top: 216.5, width: 8.64, height: 98.71 },
  "Align the inherited accent with the estimator card.",
);
edit(15, "TextBox 17", "1 · Estimate task alignment", {
  position: { left: 664.79, top: 216.5, width: 544.32, height: 32.64 },
  reason: "Expose the first technical step.",
});
edit(
  15,
  "TextBox 18",
  "Prober Ψt scores 1,000 positive pairs per task.\nRₖ⁽ᵗ⁾ = meanᵢ cos(Ψt(xᵢ), Ψt(yᵢ))",
  {
    position: { left: 664.79, top: 253.94, width: 536.64, height: 54.89 },
    reason: "Show how task alignment is measured.",
    style: { typeface: TNR, fontSize: 16.5 },
  },
);
move(
  15,
  "Rounded Rectangle 19",
  { left: 639.83, top: 360, width: 580.8, height: 111.77 },
  "Retain the inherited second method card for the adaptive scheduler.",
);
move(
  15,
  "Rectangle 20",
  { left: 641.75, top: 369.6, width: 8.64, height: 90.48 },
  "Align the inherited accent with the scheduler card.",
);
edit(15, "TextBox 21", "2 · Broaden sampling progressively", {
  position: { left: 664.79, top: 369.6, width: 542.4, height: 54.89 },
  reason: "Expose the second technical step.",
});
edit(
  15,
  "TextBox 22",
  "P⁽ᵗ⁾(k) ∝ exp(Rₖ⁽ᵗ⁾ / σ(t));   σ(t): 0.1 → 1.0",
  {
    position: { left: 664.79, top: 427.26, width: 530.88, height: 28.06 },
    reason: "Explain the schedule and the role of the rising temperature.",
  },
);

// Slide 16: establish a visible experiments boundary.
edit(16, "TextBox 7", "Experiments · Capability Analysis on UVRB", {
  reason: "Make the start of the experimental section unmistakable.",
});
edit(
  16,
  "TextBox 9",
  "Experiments: UVRB analysis → GVE results → ablations → correlations → data scaling.",
  { reason: "Preview the experimental sequence." },
);
edit(
  16,
  "TextBox 14",
  "Readout: UVRB identifies recurring weak axes that guide synthesis and training.",
  { reason: "Turn the existing figure caption into an experiment-oriented reading cue." },
);

// Slide 22: explain the challenge, content, role, and progression of every module.
edit(22, "TextBox 7", "Study 1 Summary: A Causal Chain from Evaluation to GVE", {
  reason: "Make the research reasoning, rather than a flat module list, the page title.",
});
edit(
  22,
  "TextBox 9",
  "Each module solves a different challenge, and each output becomes the input to the next.",
  { reason: "State the progression before the four modules." },
);

const summaryCards = [
  {
    name: "Rounded Rectangle 13",
    position: { left: 59.52, top: 190.08, width: 274.56, height: 160 },
    text:
      "EVALUATE · UVRB\n\nChallenge: fragmented datasets hide capability.\n\nRole: unify 16 datasets to identify weak axes.",
    boldRanges: ["EVALUATE · UVRB", "Challenge:", "Role:"],
  },
  {
    name: "Rounded Rectangle 15",
    position: { left: 362.88, top: 190.08, width: 274.56, height: 160 },
    text:
      "SYNTHESIZE · UVRD\n\nChallenge: public data is noisy and uneven.\n\nRole: V-SynFlow builds 1.55M targeted pairs.",
    boldRanges: ["SYNTHESIZE · UVRD", "Challenge:", "Role:"],
  },
  {
    name: "Rounded Rectangle 17",
    position: { left: 666.24, top: 190.08, width: 274.56, height: 160 },
    text:
      "TRAIN · Modality Pyramid\n\nChallenge: tasks interfere under random mixing.\n\nRole: schedule atomic → composite tasks by alignment.",
    boldRanges: ["TRAIN · Modality Pyramid", "Challenge:", "Role:"],
  },
  {
    name: "Rounded Rectangle 19",
    position: { left: 969.6, top: 190.08, width: 274.56, height: 160 },
    text:
      "MODEL · GVE\n\nOutcome: cross-domain, multi-task embeddings.\n\nEvidence: best UVRB averages; ablations separate data and curriculum gains.",
    boldRanges: ["MODEL · GVE", "Outcome:", "Evidence:"],
  },
];

for (const card of summaryCards) {
  edit(22, card.name, card.text, {
    position: card.position,
    reason: "Give this Study 1 module its challenge, role, and research meaning.",
    style: {
      typeface: TNR,
      fontSize: 16,
      bold: false,
      color: "#FFFFFF",
      alignment: "left",
      verticalAlignment: "middle",
      autoFit: "none",
      wrap: "square",
      lineSpacing: 0.95,
      insets: { top: 9, right: 12, bottom: 9, left: 12 },
    },
    boldRanges: card.boldRanges,
  });
}

for (const [name, left] of [
  ["TextBox 14", 326.4],
  ["TextBox 16", 629.76],
  ["TextBox 18", 933.12],
]) {
  edit(22, name, "→", {
    position: { left, top: 244.8, width: 38.4, height: 48 },
    reason: "Keep the causal progression visible between the expanded module cards.",
  });
}

move(
  22,
  "Rounded Rectangle 20",
  { left: 52.8, top: 360, width: 1174.08, height: 139.2 },
  "Retain the inherited explanation card for the cross-module reasoning.",
);
move(
  22,
  "Rectangle 21",
  { left: 54.72, top: 370.56, width: 8.64, height: 118.08 },
  "Align the inherited accent with the reasoning card.",
);
edit(22, "TextBox 22", "How the reasoning progresses", {
  position: { left: 77.76, top: 370.56, width: 1137.6, height: 32.64 },
  reason: "Replace the generic validation label with a causal explanation.",
});
edit(
  22,
  "TextBox 23",
  "Evaluation defines what is missing. The unified synthesis pipeline builds supervision for those gaps. The curriculum then resolves heterogeneous multi-task optimization, producing GVE for cross-domain, zero-shot retrieval.",
  {
    position: { left: 77.76, top: 408, width: 1129.92, height: 81.6 },
    reason: "Explain why the four modules appear in this order.",
  },
);
move(
  22,
  "Rounded Rectangle 24",
  { left: 52.8, top: 532.8, width: 1174.08, height: 51.84 },
  "Retain the inherited takeaway bar below the expanded reasoning.",
);
edit(
  22,
  "TextBox 25",
  "Takeaway   Study 1 builds a cross-domain, multi-task video model through one causal chain: evaluate → synthesize → train → model.",
  {
    position: { left: 76.8, top: 534.72, width: 1132.8, height: 48 },
    reason: "Close with the cross-domain, multi-task research objective.",
  },
);

const tableEdit = {
  slide: 13,
  name: "Table 25",
  cells: [
    ["Synthesis focus", "Share"],
    ["Temporal evidence", "60%"],
    ["Spatial evidence", "30%"],
    ["PR / abstract", "10%"],
    ["Human audit", "95 / 100"],
  ],
  reason:
    "Use the compact table for the synthesized evidence distribution and audit boundary.",
};

const noteTexts = new Map([
  [
    5,
    "Define retrieval before the thesis taxonomy: encode the query and every candidate video, rank the corpus by cosine similarity, and learn relevant pairs above irrelevant ones.\n\n[Sources]\n- chapters/01-introduction.tex, Background and Motivation.\n- chapters/03-universal-video-retrieval.tex, Universal Video Retrieval formulation.",
  ],
  [
    6,
    "The three scaling problems follow the information flow of retrieval. Representation is necessary but does not determine observation, and observation does not make a relevance signal searchable at corpus scale.\n\n[Sources]\n- chapters/01-introduction.tex, three sequential scaling decisions.",
  ],
  [
    7,
    "Keep this page at the methodological level: what is scaled, why the stage is difficult, and the broad research direction. Detailed method names follow later.\n\n[Sources]\n- chapters/01-introduction.tex, semantic, observational, and search scaling challenges.\n- chapters/03-universal-video-retrieval.tex.\n- chapters/04-spatiotemporal-scaling.tex.\n- chapters/05-scale-efficient-retrieval.tex.",
  ],
  [
    8,
    "The studies are ordered by dependency: Study 1 establishes representation, Study 2 studies the evidence available to that representation, and Study 3 preserves learned relevance in deployment-scale search.\n\n[Sources]\n- chapters/01-introduction.tex, thesis framework and organization.",
  ],
  [
    13,
    "UVRD spans textual, visual, and composed queries across coarse-grained, fine-grained, and long-context retrieval. Its synthesis distribution emphasizes temporal evidence while retaining spatial and partially relevant or abstract cases.\n\n[Sources]\n- chapters/03-universal-video-retrieval.tex, V-SynFlow data synthesis and human validation.",
  ],
  [
    15,
    "The Modality Pyramid addresses gradient submergence in heterogeneous task mixing. A prober estimates per-task alignment, and a rising temperature broadens sampling toward harder tasks as training progresses.\n\n[Sources]\n- chapters/03-universal-video-retrieval.tex, Modality Pyramid and alignment-aware dynamic scheduling.",
  ],
  [
    16,
    "Experiments begin here. UVRB first reveals recurring weak axes, followed by overall GVE results, ability-level results, ablations, correlation analysis, and data scaling.\n\n[Sources]\n- chapters/03-universal-video-retrieval.tex, Experiments and capability analysis.",
  ],
  [
    22,
    "Study 1 follows one causal research chain: unified evaluation identifies missing capabilities, synthesis builds targeted supervision, curriculum learning addresses heterogeneous-task optimization, and GVE is evaluated under zero-shot retrieval.\n\n[Sources]\n- chapters/03-universal-video-retrieval.tex, Introduction, Methodology, Experiments, and Conclusion.",
  ],
]);

function parseNdjson(ndjson) {
  return ndjson
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line))
    .filter((record) => record.kind !== "notice");
}

async function inspectPresentation(presentation, kind, maxChars = 1000000) {
  const snapshot = await presentation.inspect({ kind, maxChars });
  return parseNdjson(snapshot.ndjson);
}

function findRecord(records, slide, name, kind) {
  const matches = records.filter(
    (record) =>
      record.slide === slide &&
      record.name === name &&
      (!kind || record.kind === kind),
  );
  if (matches.length !== 1) {
    throw new Error(
      `Expected one ${kind || "element"} on slide ${slide} named ${name}; found ${matches.length}`,
    );
  }
  return matches[0];
}

async function writeMapAndAudit() {
  const presentation = await PresentationFile.importPptx(
    await FileBlob.load(sourcePptx),
  );
  const records = await inspectPresentation(
    presentation,
    "slide,textbox,shape,table,notes",
  );
  const templateInspectRecords = parseNdjson(
    await fs.readFile(
      path.join(workspace, "template-inspect", "template-inspect.ndjson"),
      "utf8",
    ),
  );
  const augmentedInspectRecords = [...templateInspectRecords];
  const outputSlides = [];

  for (let slide = 1; slide <= presentation.slides.items.length; slide += 1) {
    const editTargets = [];
    const sourceLayout = JSON.parse(
      await fs.readFile(
        path.join(
          workspace,
          "template-inspect",
          "layouts",
          `source-slide-${String(slide).padStart(2, "0")}.layout.json`,
        ),
        "utf8",
      ),
    );
    for (const element of sourceLayout.elements) {
      if (
        element.aid &&
        !augmentedInspectRecords.some(
          (candidate) =>
            candidate.slide === slide && candidate.id === element.aid,
        )
      ) {
        augmentedInspectRecords.push({
          kind: element.kind || "shape",
          id: element.aid,
          slide,
          name: element.name,
          bbox: element.bbox,
          text: element.text,
          textPreview: element.textPreview,
        });
      }
    }
    for (const item of edits.filter((candidate) => candidate.slide === slide)) {
      const record = findRecord(records, slide, item.name);
      const target = {
        action: item.position ? "rewrite-and-reposition" : "rewrite",
        reason: item.reason,
      };
      const inspectHasElement = templateInspectRecords.some(
        (candidate) =>
          candidate.slide === slide && candidate.id === record.id,
      );
      if (inspectHasElement) {
        target.sourceElementId = record.id;
      } else {
        const layoutMatches = sourceLayout.elements.filter(
          (candidate) => candidate.name === item.name,
        );
        if (layoutMatches.length !== 1) {
          throw new Error(
            `Expected one layout element on slide ${slide} named ${item.name}; found ${layoutMatches.length}`,
          );
        }
        target.sourceElementId = layoutMatches[0].aid;
        if (
          !augmentedInspectRecords.some(
            (candidate) =>
              candidate.slide === slide &&
              candidate.id === layoutMatches[0].aid,
          )
        ) {
          augmentedInspectRecords.push({
            kind: layoutMatches[0].kind || "shape",
            id: layoutMatches[0].aid,
            slide,
            name: layoutMatches[0].name,
            bbox: layoutMatches[0].bbox,
            text: layoutMatches[0].text,
            textPreview: layoutMatches[0].textPreview,
          });
        }
      }
      editTargets.push(target);
    }
    if (tableEdit.slide === slide) {
      const record = findRecord(records, slide, tableEdit.name, "table");
      editTargets.push({
        sourceElementId: record.id,
        action: "rewrite",
        reason: tableEdit.reason,
      });
    }
    const uniqueTargets = [
      ...new Map(
        editTargets.map((target) => [
          target.sourceElementId || `shape:${target.shapeId}`,
          target,
        ]),
      ).values(),
    ];
    outputSlides.push({
      outputSlide: slide,
      sourceSlide: slide,
      narrativeRole: uniqueTargets.length ? "revision" : "preserve",
      reuseMode: "duplicate-slide",
      editTargets: uniqueTargets,
    });
  }

  await fs.writeFile(
    frameMapPath,
    `${JSON.stringify({ outputSlides, omittedSourceSlides: [] }, null, 2)}\n`,
  );
  await fs.writeFile(
    path.join(workspace, "template-inspect-augmented.ndjson"),
    `${augmentedInspectRecords.map((record) => JSON.stringify(record)).join("\n")}\n`,
  );
  await fs.writeFile(
    path.join(workspace, "template-audit-v0.9-final-pass.txt"),
    [
      "Source: the author-edited slides/thesis-slides-v0.86.pptx, 69 slides, 16:9.",
      "Visual contract: preserve the inherited navy/gold thesis design, Times New Roman typography, navigation, footer, figures, appendix, and all unchanged slides.",
      "Revision scope: slides 5-8, 13, 15-16, and 22, plus their speaker notes.",
      "No slide is added, removed, or reordered. No thesis figure is cropped, regenerated, or replaced.",
      "All revised compositions reuse inherited slide elements; no new primitive is added.",
    ].join("\n"),
  );
  await fs.writeFile(
    path.join(workspace, "source-notes-v0.9-final-pass.txt"),
    [
      "Primary artifact source: the author's current thesis-slides-v0.86.pptx.",
      "Primary content sources: chapters/01-introduction.tex and chapters/03-universal-video-retrieval.tex.",
      "Chapter 1 supplies the retrieval definition, three sequential scaling decisions, and cross-study dependency.",
      "Chapter 3 supplies the UVR taxonomy, UVRD query/domain coverage, 60/30/10 synthesis distribution, Modality Pyramid mechanism, experiment order, and Study 1 causal chain.",
      "No external web source or new empirical claim is used.",
    ].join("\n"),
  );
  await fs.writeFile(
    path.join(workspace, "deviation-log-v0.9-final-pass.txt"),
    [
      "Slides 5 and 22 substantially recompose inherited cards to clarify process and research logic.",
      "Slides 6-8 rewrite the introduction sequence around definitions, challenges, and dependency.",
      "Slide 13 replaces the former design-principle aside with compact query/domain coverage.",
      "Slide 15 expands the technical motivation and adaptive scheduling mechanism.",
      "Slide 16 explicitly marks the beginning of experiments.",
      "All other slides and all embedded figures are preserved.",
    ].join("\n"),
  );
  console.log(frameMapPath);
}

async function writeBlob(filePath, blob) {
  await fs.writeFile(
    filePath,
    new Uint8Array(await blob.arrayBuffer()),
  );
}

async function editDeck() {
  const presentation = await PresentationFile.importPptx(
    await FileBlob.load(starterPptx),
  );
  const records = await inspectPresentation(
    presentation,
    "textbox,shape,table,notes",
  );

  for (const item of edits) {
    const record = findRecord(records, item.slide, item.name);
    const element = presentation.resolve(record.id);
    if (item.position) {
      element.position = item.position;
    }
    if (item.newText !== undefined) {
      element.text = item.newText;
    }
    if (item.style) {
      element.text.style = item.style;
    }
    for (const phrase of item.boldRanges || []) {
      element.text.get(phrase).bold = true;
    }
  }

  const tableRecord = findRecord(
    records,
    tableEdit.slide,
    tableEdit.name,
    "table",
  );
  const table = presentation.resolve(tableRecord.id);
  for (let row = 0; row < tableEdit.cells.length; row += 1) {
    for (let column = 0; column < tableEdit.cells[row].length; column += 1) {
      table.cells.set(row, column, tableEdit.cells[row][column]);
    }
  }

  for (const [slide, noteText] of noteTexts.entries()) {
    const matches = records.filter(
      (record) => record.kind === "notes" && record.slide === slide,
    );
    if (matches.length !== 1) {
      throw new Error(
        `Expected one notes block on slide ${slide}; found ${matches.length}`,
      );
    }
    presentation.resolve(matches[0].id).setText(noteText);
  }

  await fs.mkdir(renderDir, { recursive: true });
  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    await writeBlob(
      path.join(renderDir, `${stem}.png`),
      await presentation.export({ slide, format: "png", scale: 1 }),
    );
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(
      path.join(renderDir, `${stem}.layout.json`),
      await layout.text(),
    );
  }

  await writeBlob(
    path.join(renderDir, "montage.webp"),
    await presentation.export({
      format: "webp",
      montage: { format: "webp", columns: 4, slideWidth: 480 },
      scale: 1,
    }),
  );

  const finalInspect = await presentation.inspect({
    kind: "slide,textbox,shape,table,notes",
    maxChars: 1000000,
  });
  await fs.writeFile(
    path.join(workspace, "thesis-slides-v0.9.inspect.ndjson"),
    finalInspect.ndjson,
  );

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(outputPptx);
  console.log(outputPptx);
}

if (mode === "map") {
  await writeMapAndAudit();
} else if (mode === "edit") {
  await editDeck();
} else {
  throw new Error(`Unsupported MODE: ${mode}`);
}
