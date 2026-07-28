# Defense Slides: Durable Editing Guide

This is the authoritative guide for future defense-slide work. It consolidates
the user's feedback, the thesis-alignment decisions, visual standards, failure
cases, the retained version history, and the reviewed V0.9 state. It is
deliberately a decision document rather than a chronological work log.

## 1. Retained versions

| Version | Slides | SHA-256 | Role |
|---|---:|---|---|
| `v0.1` | 47 | `3b573ede345926c2785fa848a308382ca36b9ceaeb0696f7457c7d8111a9cce3` | initial structural draft |
| `v0.2` | 76 | `a8877724c7f93d8aaad37e02ead59b089ac49128ad9b492ab0472199e9895c30` | factual and visual-hierarchy expansion |
| `v0.3` | 72 | `e34ffb963dfff8c43ed4694bb825999cef1e00b77c2cea00f0e62b13a647db9d` | aesthetic and source-faithfulness pass |
| `v0.4` | 85 | `07bfa9cb5639ccbd7f4469c3b761b936cecb0736f5cbb5f7a383e061da5a6527` | design-system and OOXML stabilization |
| `v0.5` | 79 | `24f1898e9bd1c6e6c38ce8ef11c6d280f0911cd4f5ecf857172b5e69731946c2` | thesis-level restructuring and evidence calibration |
| `v0.6` | 79 | `bd856ec48c1b6cfb7ed63b656322a64885148cb9c15b1bdd2ee23147ee547c21` | original v0.66, stable classical baseline |
| `v0.7` | 69 | `1feb4ea7eda31f2449ef285608d5a8b21d64fdc61406439c1bec0d897e92df97` | original v0.69, stable compressed baseline |
| `v0.8` | 69 | `45e8070682ee4e5d166f47301e9c62c057c84b11041e57a57e45f972e39b0b56` | pre-review 69-slide baseline |
| `v0.9` | 69 | `467fc283fed0cca02fa4490f48fb17b6340165919141fbc094edfac96b8b4e86` | current formal defense deck |

The retained versions are formal milestones. `v0.1`–`v0.5` preserve the early
design and content evolution. `v0.6`, `v0.7`, and `v0.8` preserve the major
restructuring milestones. V0.9 consolidates the V0.81–V0.87 review chain. Its
important intermediate reasoning and hashes remain in
`v0.9-build/CHANGELOG.md`, while repetitive working PPTX files and build folders
are kept only in the system Trash.

Never overwrite a formal version. Create `v0.91` or another explicit new
version. If old PPTX files are pruned, move them to the system Trash after
notifying the user. Do not permanently delete them.

### 1.1 Historical evolution worth preserving

- **v0.1** established the first complete structural direction.
- **v0.2** expanded the deck and corrected factual presentation, hierarchy, and
  page-level legibility.
- **v0.3** concentrated on visual polish, thesis-faithful wording, figure
  callouts, and narrative continuity.
- **v0.4** stabilized the inherited design system. It introduced consistent
  layout bounds, anchored captions to actual image dimensions, reduced font
  roles to a controlled set, corrected recurring text/card overflow, compressed
  repetitive Q&A pages, and repaired two PowerPoint package defects:
  `defRPr` child ordering and notes-master registration.
- **v0.5** reduced 85 slides to 79 and organized the deck around semantic,
  observational, and search scaling. It preserved thesis figures, strengthened
  cross-study transitions, and performed a committee-oriented evidence-boundary
  pass without a risky visual redesign.

### 1.2 v0.5 evidence-boundary lessons

The following corrections remain valid even when later versions use different
pages or layouts:

- Say **14 evaluated baselines/models** according to the exact thesis context,
  rather than casually inflating the comparison set.
- Show audit sample size with the result. A visible `95 / 100` is more honest
  than an isolated `95%`.
- Distinguish **input-token reduction** from measured latency, throughput, or
  end-to-end efficiency.
- Present MSE as VEterfall's primary distillation signal and InfoNCE as an
  auxiliary regularizer when following the reported ablation.
- Treat SCL as a soft ordering regularizer supported empirically. Do not claim a
  formal metric or triangle-inequality guarantee without source and
  implementation evidence.
- Do not infer a latency SLA from a production configuration when the thesis does
  not report that threshold.
- Describe single reported configurations as evaluated points, not as a complete
  operating curve or proof of Pareto dominance.
- Distinguish a direct observation miss from incomplete semantic-constraint
  matching in error analysis.
- Preserve useful limitations and baseline-exposure caveats rather than turning
  transfer evidence into an unconditional superiority claim.

### 1.3 Technical lessons from the early design system

- Do not use automatic font shrinking as a routine fix. Rewrite the copy or
  change the frame/layout.
- A picture caption should be positioned from the picture's rendered height, not
  an assumed aspect ratio.
- A card must be tall and wide enough for its label and body. A frame can stay
  inside the slide while its internal text still overlaps another element.
- OOXML child order matters. In particular, `defRPr` must follow the schema order.
- Notes require a registered notes master. An orphaned notes-master relationship
  can make PowerPoint report that the file needs repair.
- After any low-level package or notes change, check package integrity,
  relationships, slide reload, images, overflow, and the full render.

## 2. Highest-order intent

This is a PhD defense, not a company report and not three paper talks joined
together. The audience should be able to identify:

1. the thesis-wide research problem;
2. why each study is necessary;
3. the methodological novelty;
4. what evidence supports each claim;
5. how the three studies form a coherent thesis.

The thesis is the source of truth. Before modifying a study, first read the
corresponding chapter introduction to recover its motivation, problem framing,
research order, and relative emphasis. Then read the relevant method and
experiment passages for wording and evidence. Use the chapter conclusion to
calibrate the final contribution statement. Slides may condense and adapt thesis
prose for speech, but must not invent a claim, result, calculation, or conceptual
hierarchy.

When a source sentence is too long for a slide, preserve its subject, comparison,
condition, and claim strength. Do not turn a qualified observation into a
universal conclusion. Do not magnify a small numerical difference with dramatic
color or a new calculation.

## 3. Cross-page reasoning rules

A criticism about one slide is usually a possible deck-wide defect. Every
revision must check analogous roles in all three studies:

- motivation and problem statement;
- problem definition and challenge framing;
- method overview and detailed mechanism;
- experiment, finding, and takeaway;
- study summary and thesis-level conclusion.

Coordinate neighboring pages. If a method name is introduced later, an earlier
page may describe only the scene, problem, and implication. If a result moves,
also repair the overview, transition, summary, and conclusion that referred to
the old order.

Do not force the three studies into identical box counts or visual templates.
Consistency means matching semantic roles and terminology, not making distinct
research arguments look artificially identical.

At any physical slide number, the committee should understand what has already
been established without needing a future slide to explain an unexplained term.
Self-contained does not mean repeating everything. It means every new concept has
the minimum definition, motivation, or context required at first use.

## 4. Thesis-wide narrative

The introduction frames retrieval as three successive decisions:

1. **Semantic scaling:** what should be represented?
2. **Observational scaling:** what visual evidence should be observed?
3. **Search scaling:** how should learned relevance be searched at scale?

These are successive retrieval stages with different scaling challenges, not
three unrelated projects. The conclusion
returns to the same vocabulary and states the thesis principle:

> Align capacity with the active stage constraint, then test whether the capability
> transfers.

Roadmap, section openers, detailed slides, study summaries, and conclusion must
use this terminology consistently.

## 5. Study 1: semantic scaling

Use the Chapter 3 order:

1. Explain why universal video retrieval remains unresolved.
2. State the two thesis-defined hurdles.
3. Define UVRB and its unified evaluation protocol.
4. Analyze capability correlations.
5. Introduce V-SynFlow and UVRD.
6. Introduce GVE and the Modality Pyramid curriculum.
7. Present comparison, overall results, ability-level results, ablation, and data
   scaling.
8. State the finding, novelty, and contribution.

Do not show a GVE result before GVE is introduced. UVRB evaluates 14 models; do
not casually relabel all 14 as baselines. Use the thesis's exact capability and
evaluation vocabulary.

The summary should answer:

- Why was universal evaluation needed?
- What did the analysis reveal?
- What representation and training design followed from that evidence?
- What is new beyond a benchmark or a larger model?

## 6. Study 2: observational scaling

Study 2 follows Chapter 4. Its research process is:

**Benchmark → Analysis → Methodology**

### 6.1 Benchmark

Motivate sampling as a structural constraint in long-video retrieval. Define
temporal granularity and continuity before using them analytically. Explain why
MG-LVR is needed, what it measures, and how its construction supports controlled
analysis. A benchmark statistic is evidence, not the contribution by itself.

### 6.2 Analysis

The hierarchy is:

- **Test-time scaling**
  - spatial density;
  - temporal density;
  - spatial–temporal trade-off under a fixed budget.
- **Training-time scaling**
  - the thesis's training-time experiment and conclusion;
  - temporal frame-count evidence as the main body counterpart;
  - less central training-time spatial detail may remain in the appendix.

Never alternate among labels such as “test-time spatial schedule,” “temporal
test-time schedule,” or an ambiguous “spatial scaling” without the parent
hierarchy. First distinguish training time from test time. Then distinguish
spatial and temporal scaling inside the relevant branch.

The purpose of the analysis slides is not to display isolated deltas. Each page
should make the experiment, comparison, observed result, and intuitive finding
immediately legible. Use restrained emphasis when gains are small.

Slide 30 must use:

`figures/mglvr/mglvr_testtime_spatial_scaling_2.png`

The `_1` and `_2` images represent materially different experiments and are not
interchangeable.

### 6.3 Methodology

The analysis motivates VEterfall. Introduce the sparse deployment scene and the
information-loss problem before naming the solution. Explain both method ideas:

- progressive knowledge transfer;
- dense-to-sparse self-distillation.

Use thesis wording for the setup and mechanism. Do not introduce a method name on
a transition slide before the audience knows the scene, problem, and design
implication.

### 6.4 Study 2 summary

The summary uses three connected blocks:

1. why the benchmark was constructed;
2. why the analysis was performed and what it revealed;
3. how the methodology responds to that evidence.

Close with the contribution, not a corporate-style “report result.” Distinguish:

- **Result:** a measured numerical or statistical outcome.
- **Finding:** the interpretation directly supported by one or more results.
- **Takeaway:** the concise message the audience should retain.
- **Contribution:** the research artifact or method enabled by the work.
- **Novelty:** what is methodologically new relative to prior work.

## 7. Study 3: search scaling

Use the Chapter 5 introduction's allocation of attention.

### 7.1 Problem and challenges

First define web-scale recommendation retrieval and the offline-to-online search
scene. Present the thesis's **three challenges** separately:

1. unified multi-relational relevance;
2. efficient billion-scale graph search;
3. irregular, high-concurrency GPU computation.

Do not replace “three challenges” with an improvised umbrella phrase. Do not
introduce the method while the audience is still learning the problem. Triangle
inequality and other background properties require only the minimum explanation
needed to understand why the challenge exists.

### 7.2 Method

Present GMP-GR as offline learning followed by online search:

1. explain why MUIRML is needed;
2. explain how SCL works and why it supports the metric-learning objective;
3. explain C-HiPANNS within a query;
4. explain Q-HiPANNS across queries;
5. explain the production/GPU execution optimization.

Equations cannot stand alone. Each formula page needs a plain-language purpose,
the mechanism, and the relation to the corresponding challenge.

C-HiPANNS and Q-HiPANNS are coupled parts of the online retrieval design, not
unrelated parallel modules. When presenting two components, state their
difference, their dependency, and how they work together.

### 7.3 Evidence and summary

Offline metrics and online A/B results validate the research contribution. They
are not the organizing logic of the study. The summary must map:

**Challenge → Design response → Evidence → Contribution/novelty**

Novelty should be visible throughout the study, especially in the problem-to-
method transitions and final summary.

## 8. Conclusion, limitations, and future work

The conclusion mirrors the three retrieval stages and the exact contribution language
used in the studies. It should not introduce a fourth framing at the end.
Generalizability means transfer beyond the optimization condition and must be
defined operationally for each study.

Place limitations where they support honest synthesis, not where they interrupt
the contribution before it is understood. Future work must state a concrete
unresolved problem, why it follows from the thesis, and a plausible research
direction. One-line slogans are insufficient, but speculative detail must not be
presented as completed evidence.

## 9. Visual standards

The preferred style is restrained, professional, thesis-like, and stable.
Preserve the inherited master, theme, Times New Roman typography, and established
navy/gold/green/red/muted palette unless the user explicitly requests a redesign.
Avoid decoration, animation, and complex layout systems that add risk without
improving the argument.

### 9.1 Page balance

- Fill the page, but do not crowd it.
- Keep the visual mass centered, both horizontally and vertically.
- Leave useful whitespace around the main argument.
- A large card should not contain text that occupies only half of its usable
  area. Resize the card, enlarge the meaningful content, or restructure the page.
- Box size must reflect semantic weight. Do not preserve an oversized emphasis
  box merely because it existed in the prior version.
- Align edges, centers, gaps, and baselines. Similar objects need intentional,
  repeated spacing.
- The appendix may be denser and less narratively polished because it is a
  reference layer, but it still must remain readable.

### 9.2 Text

- No text may escape its box, collide with another object, or approach the footer
  unsafely.
- Avoid an orphaned final word or a one-word line.
- Keep terminology and capitalization identical across pages.
- Prefer rewriting, resizing the box, or changing the layout over automatic font
  shrink.
- Use emphasis for genuine conceptual or evidential importance, not for arbitrary
  small numbers.
- Titles should make a claim or orient the audience, not merely repeat a module
  name.
- Avoid unexplained abbreviations and editorial terms absent from the thesis.

### 9.3 Figures

- Verify the experiment represented by a figure, not just its visual similarity
  or filename.
- Preserve aspect ratio and legibility.
- Do not crop, edit, or regenerate a thesis figure without telling the user and
  receiving permission.
- A figure should have a clear “how to read” cue or a nearby finding when the
  intended comparison is not immediately obvious.

## 10. Failure cases and critical observations

These lessons came from adversarial review of the actual deck:

1. **A page-specific complaint can expose a systemic problem.** An inconsistent
   scaling label required auditing the entire Study 2 hierarchy, not changing one
   title.
2. **Ordering is often safer than adding.** Moving a result behind its method can
   restore self-containment without increasing density.
3. **No canvas overflow is necessary but insufficient.** In v0.76, slide 10 had
   internal overlap after a label auto-expanded, although the object stayed inside
   the slide.
4. **A one-line bar can still fail.** In v0.76, slide 47 wrapped beyond its blue
   emphasis bar despite passing a basic boundary check.
5. **Automatic shrinking hides structural problems.** It can make a crowded slide
   technically fit while degrading hierarchy and projector readability.
6. **Symmetry must follow meaning.** The three studies share a research rhythm,
   but forcing identical layouts can misrepresent their actual contributions.
7. **Source-faithful is not verbatim dumping.** Thesis language should be adapted
   for oral presentation while preserving the original logic and claim strength.
8. **Benchmark, analysis, and methodology are different roles.** Combining them
   into a flat list obscures the causal research process.
9. **Experimental detail has a narrative priority.** Main slides carry the
   experiments emphasized by the chapter; secondary evidence belongs in the
   compact appendix.
10. **A stable deck favors inherited structures.** Targeted edits to existing
    elements are less risky than overlaying a second design system.

## 11. Editing and QA workflow

### Before editing

1. Read this guide and the relevant section of `TODO-v0.6.md`.
2. Read the corresponding thesis chapter introduction and conclusion.
3. Locate the exact source passages, tables, and figures for every proposed
   factual change.
4. Identify neighboring and analogous slides affected by the same change.
5. Create a new version. Never work directly on `v0.9`.

To make an exact non-overwriting branch:

```bash
SLIDES_OUTPUT=slides/thesis-slides-v0.91.pptx node slides/build.mjs
```

The branch script validates the canonical V0.9 SHA-256 and PPTX/ZIP signature,
refuses overwrite, and verifies that the new file is byte-identical.

To trace a V0.8-to-V0.9 decision, start with
`slides/v0.9-build/CHANGELOG.md` and `slides/v0.9-build/REVIEW.md`. The exact
editor for the final pass is `slides/v0.9-build/edit-final-pass.mjs`. It requires
the restored author-edited V0.86 source if replay is ever necessary. Full
byte-for-byte reconstruction of every working iteration is not a maintenance
requirement.

### During editing

- Prefer the smallest coordinated change that solves the content and layout
  problem.
- Recheck terminology at the roadmap, study opener, detail page, summary, and
  conclusion.
- Keep a distinction between confirmed source-based changes and editorial
  hypotheses.
- Do not add calculations or experimental claims not present in the thesis.
- Do not create a new record file for every render or minor patch.

### Required final checks

1. Confirm the intended slide count and section boundaries.
2. Render every slide.
3. Review all slides in montages for rhythm, balance, density, and repeated
   defects.
4. Review dense, newly changed, and visually suspicious pages at full resolution.
5. Check slide-boundary overflow and internal text/object overlap.
6. Check line wrapping, orphan words, box fill, footer clearance, and visual
   centering.
7. Check terminology consistency and first-use definitions.
8. Check the identity of critical figures, especially Study 2 slide 30.
9. Check that the PPTX package opens without repair and has valid ZIP/package
   structure.
10. Reopen the exported PPTX and verify slide count, image presence, and notes.
11. Compare unchanged slides with the source version to detect unintended drift.

Automated checks do not replace rendered visual inspection.

## 12. Current status

### Confirmed and implemented through V0.9

- 69 slides: 57 main slides and 12 compact appendix slides.
- Repository-level `README.md`, `TODO.md`, and `AGENTS.md`, together with the
  slide-local documents, identify V0.9 as the current formal defense deck.
- Study 1 result order follows the introduction of its data, model, and
  curriculum.
- Study 2 distinguishes training-time and test-time scaling and uses the correct
  spatial-scaling figure.
- Study 2 summary follows Benchmark → Analysis → Methodology.
- Study 3 presents three challenges separately and preserves the Chapter 5 method
  order.
- C-HiPANNS and Q-HiPANNS are framed as coupled online components.
- Roadmap, study summaries, and conclusion use consistent semantic,
  observational, and search scaling language.
- Chapter 3 task/domain/sub-domain terminology and the editable V-SynFlow stage
  name are aligned with the thesis.
- Chapter 4 granularity and continuity definitions use the thesis notation.
- SCL, transfer, correlation, and efficiency claims are evidence-calibrated.
- Appendix result scope, radar-series count, audience-facing labels, and six
  prepared committee questions are self-contained.
- All 69 V0.9 slides were rendered and reviewed at full size.
- Canvas-overflow, template-fidelity, package-integrity, critical-render, and
  speaker-note checks passed during the V0.9 review chain.
- The consolidated V0.9 changelog records working-version hashes, affected
  sections, source alignment, preserved content, and deferred risks.

### Uncertain but not blocking

- The defense duration is not fixed. Fifty-seven main slides may require a
  speaker-level skip plan for a short slot.
- Dense experimental figures are readable in the checked render, but room and
  projector conditions may change the optimal speaking pace.
- Future-work slides are thesis-derived but necessarily more speculative than
  completed-study slides.
- External publication, acceptance, deployment, and defense-date wording may
  change and should be reverified before presentation.
- Slide 12's embedded thesis figure retains the source phrase “Multimodal Task
  Extending.” The editable slide label is corrected, but the source figure was
  not regenerated.
- Slide 23's publication-status wording is intentionally unchanged from V0.85.

### Decisions that require the author

- Target speaking duration and which evidence slides are mandatory, skippable, or
  appendix-only.
- Whether a particular committee prefers more equations or more empirical detail.
- Whether genuinely new experiments and verified results should be added.
- Any externally changed venue, status, date, or deployment wording.

### Deliberately unnecessary or too risky

- A complete visual redesign.
- More decorative diagrams, animations, or complex responsive layouts.
- New calculations designed to make a small improvement look dramatic.
- Expanding the appendix beyond its compact reference role.
- Forcing all studies into identical numbers of stages or boxes.
- Removing limitations merely to make claims appear stronger.

## 13. File and record policy

Keep the visible directory reviewable:

- five early historical PPTX files (`v0.1`–`v0.5`);
- three restructuring milestone PPTX files (`v0.6`, `v0.7`, and `v0.8`);
- the formal V0.9 deck;
- `README.md`;
- this guide;
- the early feedback record (`TODO-v0.6.md`) and consolidated V0.9 review
  evidence (`v0.9-build/REVIEW.md`);
- one safe version-branch script;
- the consolidated V0.9 changelog and final-pass editor;
- the historical v0.4 design-system source (`build.py`);
- the reproducible v0.5 build chain and consolidated v0.5 changelog;
- the figure directory.

Starter decks, edited candidates, rendered PNGs, layout JSON, extracted source
media, inspection output, and dependency workspaces are temporary and are not
long-term repository dependencies. If temporary PPTX files are pruned, move the
containing temporary directory to the system Trash rather than deleting those
PPTX files directly.

Only update this guide when a decision is likely to matter in a future editing
session. Record durable rules, source alignment, unresolved author decisions, and
new failure modes. Do not recreate a large collection of per-version plan,
review, QA, and handoff documents.
