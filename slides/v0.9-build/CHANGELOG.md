# Thesis Slides V0.9 Consolidated Change Record

## Final artifact

- Final deck: `slides/thesis-slides-v0.9.pptx`
- Slides: `69` (`57` main slides and `12` appendix slides)
- SHA-256: `467fc283fed0cca02fa4490f48fb17b6340165919141fbc094edfac96b8b4e86`
- V0.9 is a byte-identical promotion of the reviewed V0.87 deck.
- V0.87 was built from the author's manually revised on-disk V0.86, whose
  SHA-256 was
  `e25569acc944391532ad9364606b35f6c80da591a6db66d09f13dce9cfae15b2`.

## Consolidated review path

V0.81 through V0.87 were working iterations between the retained V0.8
pre-review milestone and the formal V0.9 deck. Their individual PPTX files and
per-version build directories were retired from the visible repository after
V0.9 promotion. They were moved to the system Trash and remain recoverable.

| Working version | SHA-256 | Main purpose |
|---|---|---|
| V0.81 | `d41183660c53a705f9bd1dd31646554853415ed2cb77547ae190379e91a0f9ad` | author's manual review starting point |
| V0.82 | `d77f84fca9ca9ca7e0a37915e4d1869f5da7b6f84d738be583d78dbd5cb1b497` | thesis line, Introduction, and global terminology |
| V0.83 | `d2fc4de2530ca2b76a7fb7f025873d7be9ea5186e4f21abdd1260cd4a34c83ea` | Study 1 causal order, curriculum, and summary |
| V0.84 | `602119f6d402ee932cd7a59c9718ab6a3c4e440387cb38050d172cdbcac2784b` | Study 2 scaling hierarchy and VEterfall evidence |
| V0.85 | `a126db923a262b12f0bef4867f2d22bec832d3c98b904dc5b3788ec10ae42d92` | Study 3, conclusion, future work, and stability pass |
| V0.86 | `e25569acc944391532ad9364606b35f6c80da591a6db66d09f13dce9cfae15b2` | full-deck evidence calibration plus author manual edits |
| V0.87 | `467fc283fed0cca02fa4490f48fb17b6340165919141fbc094edfac96b8b4e86` | final problem-formulation and Study 1 logic revision |

The consolidated review evidence is retained in `REVIEW.md`. The exact
Artifact Tool editor for the final V0.86-to-V0.87 transformation is retained as
`edit-final-pass.mjs`. It requires the restored author-edited V0.86 source and
an explicit `SOURCE_PPTX` if replay is ever necessary.

## Major changes from V0.8 to V0.9

### Introduction and thesis line

- Standardized semantic, observational, and search scaling terminology.
- Reframed the three studies as successive decisions in one retrieval pipeline.
- Rebuilt slide 5 as the problem formulation for embedding-based video
  retrieval: query and corpus embedding, similarity ranking, and top-K return.
- Clarified on slides 6–8 what each scaling stage changes, why it is difficult,
  and why the research order follows representation, observation, then search.

### Study 1: semantic scaling

- Restored the Chapter 3 task, domain, and sub-domain taxonomy.
- Reordered the argument from unified evaluation to capability analysis, data
  synthesis, curriculum training, and model validation.
- Clarified V-SynFlow, UVRD query/domain coverage, and the `60/30/10`
  synthesis distribution while retaining the `95/100` audit boundary.
- Expanded the Modality Pyramid motivation, prober-based alignment estimate,
  adaptive sampling rule, and temperature progression.
- Added an explicit experiment boundary and rebuilt the Study 1 summary as
  Evaluation → Synthesis → Training → Model.

### Study 2: observational scaling

- Defined frame sampling, tokens per frame, temporal granularity, and continuity
  before using the notation analytically.
- Restored the complete test-time and training-time scaling hierarchy.
- Connected frame-count mismatch to progressive dense-to-sparse transfer.
- Expanded VEterfall evidence across the reported configurations while
  preserving the thesis's evidence boundaries.
- Kept the required slide 30 spatial-scaling figure unchanged.

### Study 3: search scaling

- Preserved the three distinct challenges: multi-relational relevance,
  billion-scale graph search, and irregular high-concurrency GPU computation.
- Clarified MUIRML/SCL, C-HiPANNS, and Q-HiPANNS as a coupled offline-to-online
  design.
- Rebuilt the summary around challenge, design response, evidence, and novelty.
- Kept SCL framed as a soft ordering regularizer rather than a formal metric
  guarantee.

### Conclusion, appendix, and evidence calibration

- Reconstructed the conclusion around one retrieval path and stage-conditioned
  scaling.
- Distinguished measured results, findings, transfer evidence, and open
  limitations.
- Reworked future directions as research gaps rather than completed claims.
- Corrected appendix scope, visible model counts, audience-facing labels, and
  prepared committee questions.
- Preserved slide 23 wording and the embedded source figure on slide 12.

## Final V0.87-to-V0.9 pass

The final pass changed slides `5, 6, 7, 8, 13, 15, 16, and 22`. The other
`61` slides were pixel-identical to the author-edited V0.86 source. V0.9 is
byte-identical to this reviewed V0.87 result.

## Quality assurance

- All 69 slides were rendered and visually reviewed.
- The eight final-pass slides were checked individually at full size.
- Automated overflow testing passed.
- Template-fidelity testing passed with zero issues.
- PPTX ZIP/package integrity testing passed.
- Reopened inspection confirmed 69 slides, 28 media assets, and 69 notes parts.
- V0.9 is byte-identical to V0.87 and therefore inherits the completed visual QA.

## Retention decision

The visible `slides/` directory retains:

- formal PPTX milestones V0.1 through V0.8 and V0.9;
- this consolidated V0.9 record, the consolidated review evidence, and the
  final-pass editor;
- the historical V0.4/V0.5 build assets and consolidated V0.5 changelog;
- one safe non-overwriting branch script, the durable slide guide, and reusable
  figures.

This mirrors the milestone-oriented organization used before V0.8 while
preserving the important V0.81–V0.87 reasoning in a compact form.
