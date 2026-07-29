# Defense Slides: Consolidated History

This document preserves the durable information from the earlier slide plans,
speaker-note drafts, changelogs, and QA records. The active slide directory now
contains four retained milestones:

- `thesis-slides-v1.pptx` with `NOTE-V1.md`
- `thesis-slides-v1.4.pptx` with `NOTE-V1.4.md`
- `thesis-slides-v2.pptx` with `NOTE-V2.md`
- `thesis-slides-v3.pptx` with `NOTE-V3.md`

Earlier source files remain recoverable through prior Git commits. Local
recovery copies are also retained.

## 1. Version lineage

| Version | Slides | SHA-256 | Durable role |
|---|---:|---|---|
| V0.1 | 47 | `3b573ede345926c2785fa848a308382ca36b9ceaeb0696f7457c7d8111a9cce3` | Initial complete structure |
| V0.2 | 76 | `a8877724c7f93d8aaad37e02ead59b089ac49128ad9b492ab0472199e9895c30` | Factual and visual-hierarchy expansion |
| V0.3 | 72 | `e34ffb963dfff8c43ed4694bb825999cef1e00b77c2cea00f0e62b13a647db9d` | Aesthetic and source-faithfulness pass |
| V0.4 | 85 | `07bfa9cb5639ccbd7f4469c3b761b936cecb0736f5cbb5f7a383e061da5a6527` | Design-system and OOXML stabilization |
| V0.5 | 79 | `24f1898e9bd1c6e6c38ce8ef11c6d280f0911cd4f5ecf857172b5e69731946c2` | Thesis-level restructuring and evidence calibration |
| V0.6 | 79 | `bd856ec48c1b6cfb7ed63b656322a64885148cb9c15b1bdd2ee23147ee547c21` | Stable classical baseline |
| V0.7 | 69 | `1feb4ea7eda31f2449ef285608d5a8b21d64fdc61406439c1bec0d897e92df97` | Compressed baseline |
| V0.8 | 69 | `45e8070682ee4e5d166f47301e9c62c057c84b11041e57a57e45f972e39b0b56` | Pre-review baseline |
| V0.9 | 69 | `467fc283fed0cca02fa4490f48fb17b6340165919141fbc094edfac96b8b4e86` | Reviewed formal baseline |
| V0.91 | 69 | `29f2c9fd7443d218a3831336a9bda880c2216dc0acf88d051771fb0ab8cf7381` | Author/review milestone |
| V0.92 | 69 | `57305f418d85c3862832489b0cd13412574a724f70daf04262faabbcc8e79c78` | Author/review milestone |
| V0.93 | 68 | `b5bc93fd3bf0adc6d8c3d372d845fea5b497701c0bee400f4628053a746019ee` | Final author-edited source for V1 |
| V1 | 65 | `df9f29705913a6441e5d9bf6355c0f36491f33a3645331951e7f004462a636a7` | Retained stable defense deck |
| V1.1 | 65 | `df9f29705913a6441e5d9bf6355c0f36491f33a3645331951e7f004462a636a7` | Byte-identical historical duplicate of V1 |
| V1.2 | 66 | `55d4d6a52db2911854a5615ffac58fd1b6799c25eae8ca3b6a6b4f2759000067` | Author/review expansion |
| V1.3 | 67 | `8637d81aa19601bd9162762c03c81b008318aa67dd120c505f764b953fd85425` | Author-edited source for V2 review |
| V1.4 | 67 | `51b24ce673f2f5d49f5ae44f4ab9a7a6e960ba218f3b6382fdeaa150f7c2c239` | Retained author-reviewed intermediate version |
| V2 | 70 | `ce4fb20ad7fa4893107aef8b7c4a0fa7f8b2bc79a084daef82063c14ad6be7c2` | Coordinated deck with three study-level related-work reviews |
| V3 | 69 | `48ab9b0fc09614801cebcd4bc89ab893b31d119946f632c2ac6f72cee5e47876` | Current deck with a two-page contribution synthesis and revised oral script |

V1.1 is not a retained active milestone because it is byte-identical to V1.
V1.4 is kept because it contains the author's intermediate review state.

## 2. Narrative decisions that must survive future edits

The defense is one thesis rather than three independent paper talks. The
introduction and conclusion use one connected retrieval chain:

1. **Semantic scaling:** learn a relevance representation with broad capability
   coverage.
2. **Observational scaling:** preserve the visual evidence needed to form that
   representation.
3. **Search scaling:** make the learned relevance searchable and executable over
   a very large corpus.

The causal relationship is:

> representation defines the relevance signal; observation determines whether
> its evidence enters the signal; search determines whether the signal remains
> usable at scale.

The first-to-second and second-to-third transitions must appear immediately
after the corresponding work. The deck should not postpone all cross-work
connections until the conclusion.

For every study, the audience should be able to identify:

- the core research problem and unique challenge;
- the motivation for the method;
- the methodological contribution and novelty;
- the research insight supported by the evidence;
- how the result motivates the next stage.

## 3. Study-specific durable structure

### Study 1: semantic scaling

The stable research order is:

1. diagnose fragmentation across separately prepared data, task-specific models,
   and isolated evaluation;
2. use UVRB to identify capability gaps;
3. use V-SynFlow and UVRD to construct targeted, quality-controlled supervision;
4. train GVE with the adaptive Modality Pyramid curriculum;
5. validate overall capability, ability-level behavior, ablations, correlations,
   and data scaling;
6. conclude that evaluation should guide data construction and training.

The Modality Pyramid is adaptive rather than a permanently fixed task order. A
prober estimates current alignment, foundational tasks receive stronger early
emphasis, and the distribution becomes flatter as training proceeds.

### Study 2: observational scaling

The stable research order is:

**Benchmark → Analysis → Methodology**

MG-LVR first defines temporal granularity and continuity for long, multi-granular
retrieval. The analysis then separates:

- test-time spatial density;
- test-time temporal density;
- the spatial-temporal trade-off;
- training-time spatial robustness;
- training-time temporal frame-count anchoring.

VEterfall follows from the observation that dense temporal knowledge does not
automatically transfer to sparse inference. It progressively transfers knowledge
from dense to sparse sampling through self-distillation.

The correct test-time spatial-scaling figure is
`figures/mglvr/mglvr_testtime_spatial_scaling_2.png`.

### Study 3: search scaling

The stable research order is:

1. multi-relational relevance;
2. search-compatible graph traversal at billion scale;
3. irregular GPU computation under high concurrency;
4. MUIRML and SCL for relevance learning;
5. C-HiPANNS for within-query traversal;
6. Q-HiPANNS for cross-query GPU batching;
7. offline retrieval, system efficiency, and production A/B evidence.

The main insight is that relevance must be accurate, searchable, and executable
at the same time. SCL is a soft ordering regularizer with empirical support. It
must not be presented as a formal triangle-inequality guarantee.

## 4. Evidence and formula boundaries

The following earlier corrections remain binding:

- Preserve the exact paper/thesis notation for all equations.
- UVRB evaluates the model set under a unified protocol. Do not casually inflate
  the number of baselines.
- Keep the audit sample size visible with the result, for example `95 / 100`
  rather than an unsupported universal percentage.
- Distinguish input-token reduction from measured latency, throughput, or
  end-to-end efficiency.
- Present MSE as VEterfall's primary transfer signal and InfoNCE as the auxiliary
  video-text alignment term.
- Treat single reported operating points as evaluated configurations, not proof
  of universal Pareto dominance.
- Distinguish direct evidence misses from partial semantic-constraint matches in
  the MG-LVR error analysis.
- Separate the two-service controlled A/B table from the wider deployment-scope
  statement.
- Do not infer a latency SLA, cross-platform guarantee, or formal metric property
  that the source does not report.
- Preserve limitations, benchmark boundaries, and revalidation requirements.

The V2 formula pass checked the embedding formulation, symmetric InfoNCE,
Modality Pyramid sampling, temporal granularity, temporal continuity, and the
VEterfall cascade against the frozen thesis chapters.

## 5. Speaker-note evolution

### V1

The retained V1 script is the stable English script for the 65-slide deck. It
prioritized a safe oral structure, English-only notes, evidence-calibrated
claims, and a conservative delivery range.

### V1.2 and V1.3 drafts

These drafts expanded the introduction, clarified the retrieval pipeline, added
direct transitions between studies, and introduced the first-author publication
page. They also exposed several issues that V2 resolved:

- some scripts became too short and lost the intended 40–50 minute pacing;
- slide text and spoken text occasionally diverged too much;
- methods and study summaries did not always make novelty and insight explicit;
- some cross-study connections were deferred until all three works were finished.

### V1.4 review drafts

The English `NOTE-V1.4.md` and Chinese `VNOTE-V1.4.md` were review artifacts.
They contained both proposed scripts and author comments. Their durable feedback
was incorporated into V2:

- use short, natural sentences suitable for a Chinese native speaker with IELTS
  6.5 and speaking 5;
- allow direct reading of selected slide phrases without making the script a
  verbatim transcript;
- provide clear restart points and smooth transitions;
- give the introduction enough space to establish search, recommendation, and
  data-processing applications;
- emphasize pipeline and challenge before method;
- expand method explanation where novelty matters;
- keep the final delivery below 50 minutes;
- add brief appendix notes rather than leaving backup pages unsupported.

### V2

`NOTE-V2.md` contains 70 slide sections and approximately 4,619 spoken words.
The target delivery remains within 40–50 minutes with short pauses and slide changes.
The complete script is embedded in the V2 PPTX notes.

### V3

`NOTE-V3.md` contains 69 slide sections and approximately 4,519 spoken words.
The former three-page conclusion synthesis is compressed into two pages. The
first explains why semantic, observational, and search scaling form one research
chain. The second distinguishes the technical novelty and contribution of all
three studies.

The full script removes repeated capability-list wording, gives plainer
explanations of the Modality Pyramid, VEterfall, MUIRML/SCL, and HiPANNS, and
keeps the main delivery near the upper end of the 40–50 minute range. All 69
speaker-note sections are embedded in the V3 PPTX and match `NOTE-V3.md`.

## 6. Committee, acknowledgement, and publication decisions

- Use respectful and modest language throughout.
- Thank the advisors before the committee.
- Give the committee appropriate recognition for their time and guidance.
- Thank HKUST(GZ) and AI Thrust administrative staff.
- Thank Ms. Claire Ying Luo from AS on the title slide and acknowledgement slide.
- Keep the final thanks concise so it remains natural when spoken.

The publication page appears after acknowledgements and contains nine
first-author papers:

1. the three thesis publications, in thesis order;
2. six other first-author publications.

Each entry begins with a venue label. `Zhuoning Guo` and the venue label use
16-point bold text. Oral labels are retained for SIGKDD 2024, SIGKDD 2022, and
PAKDD 2025.

## 7. Visual and oral-delivery rules

- The visual reading order must match the speaking order.
- Titles should state the page's function clearly. Avoid vague questions unless
  a section divider genuinely needs one.
- Slide keywords and spoken keywords should come from the paper or thesis.
- Keep sentences short and avoid difficult spoken vocabulary.
- Do not use automatic font shrinking as a routine fix.
- Keep main-slide evidence selective and move secondary details to the appendix.
- Do not force the three studies into identical visual templates when their
  research logic differs.
- Preserve inherited visual structures unless a coordinated change is needed.
- A page is not correct merely because all objects remain inside the canvas.
  Internal overlap, awkward wrapping, hierarchy, and projector readability must
  also be checked.

## 8. Technical and QA lessons

Earlier OOXML work established several durable lessons:

- PowerPoint child-element order matters.
- Notes require a correctly registered notes master.
- Captions should be positioned from the rendered image dimensions.
- Low-level package changes require relationship, package, notes, image, and
  full-render checks.

Every future slide-content or layout revision must:

1. preserve the source deck under a new name;
2. render every slide;
3. inspect every slide visually;
4. run overflow and out-of-bounds checks;
5. reopen or re-import the final PPTX;
6. verify slide count, images, notes, and ZIP/package integrity;
7. compare unchanged pages against the source to detect unintended drift.

V3 completed these checks for 69 slides. The final package passed ZIP integrity,
overflow, template-fidelity, slide-count, image-presence, and note-matching
checks. Every slide was rendered and visually reviewed, with the two revised
conclusion pages inspected at full size.

The V2 review completed all of these checks for 70 slides and confirmed 70
matching Markdown and embedded note sections.

## 9. Cleanup policy

The active `slides/` directory should contain:

- V1 and its note;
- V1.4 and its note;
- V2 and its note;
- V3 and its note;
- `README.md`, `SLIDES-GUIDE.md`, and this consolidated history;
- reusable figures.

Earlier PPTX files, intermediate notes, chronological review logs, and obsolete
build assets are not active repository dependencies. During the present review
they remain recoverable in `slides/.cleanup-review/`. They should be moved to
the system Trash only after the author approves the cleanup. No PPTX should be
permanently deleted.
