#!/usr/bin/env python3
"""Build thesis defense slides v0.5 from the stable v0.4 deck.

This is an intentionally conservative incremental builder. It preserves the
v0.4 visual system, source figures, notes, and package structure, while applying
the first-stage content and narrative changes documented in
``v0.5-final-changelog.md``.

Run from any directory:

    python3 slides/v0.5-build/base.py --source <v0.4.pptx> --output <base.pptx>

Input and output are resolved relative to this script. The v0.4 file is never
overwritten.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from pptx import Presentation
from pptx.oxml.ns import qn


HERE = Path(__file__).resolve().parent
SLIDES_DIR = HERE.parent
DESIGN_SYSTEM = SLIDES_DIR / "build.py"
FIGURES = SLIDES_DIR / "figures"

EXPECTED_SLIDES = 79
EXPECTED_MAIN_SLIDES = 57
EXPECTED_BACKUP_PAGES = 21


def load_design_system():
    spec = importlib.util.spec_from_file_location("thesis_slide_design", DESIGN_SYSTEM)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load design system: {DESIGN_SYSTEM}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def slide_text(slide) -> str:
    return "\n".join(
        shape.text for shape in slide.shapes
        if getattr(shape, "has_text_frame", False) and shape.text.strip()
    )


def find_slide_index(prs, title_fragment: str) -> int:
    matches = [
        i for i, slide in enumerate(prs.slides)
        if title_fragment in slide_text(slide)
    ]
    if len(matches) != 1:
        raise AssertionError(
            f"Expected one slide containing {title_fragment!r}, found {matches}"
        )
    return matches[0]


def iter_text_frames(shapes):
    for shape in shapes:
        if getattr(shape, "has_text_frame", False):
            yield shape.text_frame
        if getattr(shape, "shape_type", None) == 6:  # group
            yield from iter_text_frames(shape.shapes)
        try:
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        yield cell.text_frame
        except Exception:
            pass


def replace_in_text_frame(text_frame, old: str, new: str) -> int:
    count = 0
    for paragraph in text_frame.paragraphs:
        for run in paragraph.runs:
            if old in run.text:
                occurrences = run.text.count(old)
                run.text = run.text.replace(old, new)
                count += occurrences
    return count


def replace_on_slide(
    prs,
    title_fragment: str,
    old: str,
    new: str,
    *,
    expected: int = 1,
    include_notes: bool = False,
) -> int:
    slide = prs.slides[find_slide_index(prs, title_fragment)]
    count = sum(replace_in_text_frame(tf, old, new) for tf in iter_text_frames(slide.shapes))
    if include_notes:
        try:
            count += replace_in_text_frame(slide.notes_slide.notes_text_frame, old, new)
        except Exception:
            pass
    if count != expected:
        raise AssertionError(
            f"{title_fragment!r}: replacement {old!r} expected {expected}, got {count}"
        )
    return count


def replace_everywhere(prs, old: str, new: str, *, minimum: int = 1) -> int:
    count = 0
    for slide in prs.slides:
        count += sum(replace_in_text_frame(tf, old, new) for tf in iter_text_frames(slide.shapes))
        try:
            count += replace_in_text_frame(slide.notes_slide.notes_text_frame, old, new)
        except Exception:
            pass
    if count < minimum:
        raise AssertionError(f"Global replacement {old!r} found only {count} times")
    return count


def delete_slide_by_title(prs, design, title_fragment: str) -> None:
    idx = find_slide_index(prs, title_fragment)
    design.delete_slide(prs, idx)


def move_last_slide_after(prs, title_fragment: str) -> None:
    target_idx = find_slide_index(prs, title_fragment)
    sld_id_list = prs.slides._sldIdLst
    new_id = sld_id_list[-1]
    sld_id_list.remove(new_id)
    sld_id_list.insert(target_idx + 1, new_id)


def set_marker_text(shape, new_text: str) -> None:
    tf = shape.text_frame
    paragraph = tf.paragraphs[0]
    if paragraph.runs:
        paragraph.runs[0].text = new_text
        for run in paragraph.runs[1:]:
            run.text = ""
    else:
        paragraph.text = new_text


def renumber_main_pages(prs) -> int:
    page = 0
    for slide in prs.slides:
        text = slide_text(slide)
        if "Questions?" in text or ("Backup &" in text and "Q&A" in text):
            break
        candidates = [
            shape for shape in slide.shapes
            if getattr(shape, "has_text_frame", False)
            and shape.left / 914400 >= 11.5
            and shape.top / 914400 <= 0.45
            and re.fullmatch(r"\d+", shape.text.strip())
        ]
        if candidates:
            if len(candidates) != 1:
                raise AssertionError(f"Ambiguous main page marker on: {text[:80]}")
            page += 1
            set_marker_text(candidates[0], str(page))
    return page


def renumber_backup_pages(prs) -> int:
    number = 0
    in_backup = False
    for slide in prs.slides:
        text = slide_text(slide)
        if "Backup &" in text and "Q&A" in text:
            in_backup = True
            continue
        if not in_backup:
            continue
        candidates = [
            shape for shape in slide.shapes
            if getattr(shape, "has_text_frame", False)
            and shape.left / 914400 >= 11.5
            and shape.top / 914400 <= 0.50
            and re.fullmatch(r"B\d+", shape.text.strip())
        ]
        if candidates:
            if len(candidates) != 1:
                raise AssertionError(f"Ambiguous backup marker on: {text[:80]}")
            number += 1
            set_marker_text(candidates[0], f"B{number}")
    return number


def apply_content_edits(prs) -> None:
    # Roadmap: retain one compact roadmap instead of two agenda pages.
    replace_on_slide(prs, "Outline", "Outline", "Thesis Roadmap")
    replace_on_slide(
        prs, "Thesis Roadmap",
        "Video retrieval as a pipeline-level scaling problem",
        "One pipeline-level question, three successive scaling bottlenecks",
    )
    replace_on_slide(
        prs, "Thesis Roadmap",
        "UVRB diagnosis → UVRD synthesis → GVE unified embedding",
        "Diagnose capabilities → synthesize targeted data → train GVE",
    )
    replace_on_slide(
        prs, "Thesis Roadmap",
        "MG-LVR benchmark → scaling laws → VEterfall distillation",
        "Measure granularity → derive scaling laws → distill VEterfall",
    )
    replace_on_slide(
        prs, "Thesis Roadmap",
        "MUIRML+SCL metric → HiPANNS graph → GMP-GR GPU execution",
        "Regularize metric → parallelize graph/GPU search → deploy GMP-GR",
    )
    replace_on_slide(
        prs, "Thesis Roadmap",
        "Structure-aware scaling across the pipeline",
        "Structure-aware scaling → stage-specific evidence → future work",
    )

    # Study 1: restore thesis wording and factual precision.
    replace_on_slide(
        prs, "Universal Video Retrieval Requires Capability Coverage",
        "reveals nothing about",
        "reveals little about",
    )
    replace_on_slide(
        prs, "Three Non-Trivial Capability Gaps Emerge",
        "one scaling paradox",
        "one parameter-scaling limitation",
    )
    replace_on_slide(
        prs, "Three Non-Trivial Capability Gaps Emerge",
        "87M > 8B",
        "87M vs. 8B",
    )
    replace_on_slide(
        prs, "Three Non-Trivial Capability Gaps Emerge",
        "Scaling paradox (VIS)",
        "Limited scaling impact (VIS)",
    )
    replace_on_slide(
        prs, "Three Non-Trivial Capability Gaps Emerge",
        "On visual-only retrieval an 87M CLIP model (0.714) beats an 8B MLLM (0.702) — perceptual breadth over raw capacity.",
        "On VIS, CLIP4Clip (87M, 0.714) outperforms UniME-7B (8B, 0.702): parameter scale alone does not ensure stronger visual retrieval.",
    )
    replace_on_slide(
        prs, "Three Non-Trivial Capability Gaps Emerge",
        "Bigger is not broader — targeted, diverse data, not parameter count, closes these gaps.",
        "Parameter scale alone does not ensure capability coverage; targeted data should follow diagnosed gaps.",
    )
    replace_on_slide(
        prs, "UVRD Is Capability-Targeted, Not Merely Large",
        "Skew beats naive scale: UVRD is not the largest corpus, but the most effective for filling the capability gaps UVRB diagnosed.",
        "UVRD is not designed for size alone: its distribution directly targets the capability gaps UVRB diagnosed.",
    )
    replace_on_slide(
        prs, "GVE Improves Zero-Shot Retrieval Generalization",
        "data quality beats parameter count.",
        "targeted data and curriculum compensate for smaller model size in this comparison.",
    )
    replace_everywhere(
        prs,
        "the scaling-paradox skill where a compact CLIP encoder remains hard to beat",
        "parameter scaling brings limited gains, and a compact CLIP encoder remains hard to beat",
        minimum=1,
    )
    replace_everywhere(prs, "the scaling paradox", "the parameter-scaling limitation", minimum=1)

    # Study 2: sample-size correction and faithful MG-LVR construction semantics.
    replace_on_slide(prs, "MG-LVR: A Multi-Granularity Long-Video Benchmark", "96%", "48/50")
    replace_on_slide(prs, "MG-LVR: A Multi-Granularity Long-Video Benchmark", "Audited", "Human audit")
    replace_on_slide(
        prs, "MG-LVR: A Multi-Granularity Long-Video Benchmark",
        "Human-validated.",
        "96% correct pairs.",
    )
    replace_on_slide(
        prs, "MG-LVR Benchmark Construction",
        "Isolated clip nodes give fine queries; Louvain communities give coarse queries.",
        "Clip Relation Graphs discover single- and multi-clip units before query categorization.",
    )
    replace_on_slide(
        prs, "MG-LVR Benchmark Construction",
        "Clip Relation Graph controls granularity: fine (G) from isolated moments · coarse (C) from communities.",
        "Graph units precede categorization: G assigns FN/MD/CR, while C distinguishes continuous and discrete evidence.",
    )

    # Study 3: maintain thesis claims without slide-only intensifiers.
    replace_on_slide(
        prs, "Web-Scale Retrieval: Reduce Billions to Candidates",
        "A more accurate neural metric δ is worthless if it cannot be searched: expressive metrics can violate the regularity graph traversal relies on.",
        "A more accurate neural metric δ has limited deployment value if it cannot be searched efficiently: expressive metrics can violate the regularity graph traversal relies on.",
    )
    replace_on_slide(
        prs, "Web-Scale Retrieval: Reduce Billions to Candidates",
        "Study 3 is search scaling for a learned signal — making accuracy compatible with graph and GPU execution. (Here queries are users and items; the searchable-signal principle is the same as for video.)",
        "Study 3 tests the deployment layer shared by embedding-based retrieval: making a learned signal compatible with graph and GPU execution, using user-item retrieval as the production setting.",
    )
    replace_on_slide(
        prs, "Expressive Neural Metrics Can Break Graph Traversal",
        "The triangle inequality holds, so every greedy hop provably moves closer to the target — graph traversal reaches the true nearest neighbors.",
        "Euclidean distance provides regular neighborhood structure that supports effective greedy graph traversal.",
    )
    replace_on_slide(
        prs, "Expressive Neural Metrics Can Break Graph Traversal",
        "Better offline relevance is useless unless the signal stays searchable.",
        "Offline relevance gains must survive graph search to matter at deployment scale.",
    )
    replace_on_slide(
        prs, "MUIRML + SCL Make Relevance Searchable",
        "SCL transplants Euclidean ranking regularity into the learned metric, retaining approximate triangle inequality property.",
        "SCL transfers Euclidean ranking regularity to the learned metric for more efficient graph navigation.",
    )
    replace_on_slide(
        prs, "Online A/B Tests Validate Production Impact",
        "Validated by two online A/B services (main feed and short video), then subsequently extended across 20+ Baidu applications — the broader rollout is deployment, not a single A/B result.",
        "The controlled online table reports two services; the broader GMP-GR system is deployed across 20+ Baidu applications.",
    )
    replace_on_slide(prs, "System-Level Execution Makes the Signal Deployable", "+74%", "+74-75%")
    replace_on_slide(prs, "System-Level Execution Makes the Signal Deployable", "+26%", "+25-26%")
    replace_on_slide(
        prs, "System-Level Execution Makes the Signal Deployable",
        "Streaming index updates keep embeddings current under dynamic catalogs; two services on five servers each sustain production-scale traffic within the P99 latency budget.",
        "Streaming index updates keep embeddings current under dynamic catalogs; two services supported by five servers in total sustain production-scale traffic within the P99 latency budget.",
    )

    # Conclusion: distinguish the shared principle from stage-specific evidence.
    replace_on_slide(
        prs, "Generalizability Confirms the Right Bottleneck",
        "Generalizability Confirms the Right Bottleneck",
        "Generalizability Provides Stage-Specific Evidence",
    )
    replace_on_slide(
        prs, "Generalizability Provides Stage-Specific Evidence",
        "The opening framework, now filled with evidence from each study.",
        "The three studies test transfer under different but complementary conditions.",
    )
    replace_on_slide(
        prs, "Generalizability Provides Stage-Specific Evidence",
        "Generalizability is the evidence that scaling has addressed the right bottleneck.",
        "Scaling is meaningful when gains extend beyond the narrow condition directly optimized.",
    )
    replace_on_slide(
        prs, "Publications and Research Outputs",
        "The three studies correspond to three papers and reusable public artifacts.",
        "The three studies correspond to three papers and reusable research artifacts.",
    )
    replace_on_slide(
        prs, "Publications and Research Outputs",
        "UVRB, UVRD, MG-LVR data and GVE, VEterfall, GMP-GR methods — released for reproducible research.",
        "UVRB/UVRD, MG-LVR, and model/code artifacts follow the release commitments of the associated papers.",
    )

    # Backup corrections retained after the main-deck edit.
    replace_on_slide(
        prs, "A2-1  MG-LVR vs. Prior Long-Video Benchmarks",
        "Isolated clip nodes → Fine queries · Louvain communities → Coarse queries — granularity is structural, derived from the Clip Relation Graph, not manually labeled.",
        "Low-connection nodes and Louvain communities discover single- and multi-clip units; G and C then categorize granularity and continuity.",
    )


def add_semantic_data_scaling_slide(prs, design) -> None:
    design.prs = prs
    design.BLANK = prs.slide_layouts[6]
    design.FIG = str(FIGURES)

    slide = design.base(
        1,
        "GVE Data Scaling Follows a Logarithmic Law",
        "More training data improves both model sizes, with diminishing returns.",
    )
    design.pic(slide, "gve/scaling_avg", 0.55, 2.02, width=8.05)
    design.result_card(
        slide, 8.82, 2.05, 3.96, 1.72,
        "Both scales improve",
        "Dataset and ability averages rise approximately log-linearly with the number of training pairs.",
    )
    design.info_card(
        slide, 8.82, 3.97, 3.96, 1.78,
        "Different scaling rates",
        "Per 10× data: GVE-3B gains +7.4% vs. +5.4% for GVE-7B, while GVE-7B retains higher absolute performance.",
    )
    design.take(
        slide,
        "Semantic scaling depends on training data volume as well as model capacity, with diminishing returns.",
        y=6.36,
    )
    design.notes(
        slide,
        "Targeted data scaling is approximately logarithmic for both GVE sizes. "
        "The smaller model gains more in relative terms per decade of data, while "
        "the larger model maintains higher absolute capability.",
    )
    move_last_slide_after(prs, "Inter-Ability Correlations Reveal Decoupled Representations")


def apply_structural_edits(prs, design) -> None:
    add_semantic_data_scaling_slide(prs, design)

    # Delete only high-confidence duplicates or misleading self-made frames.
    for title in (
        "Roadmap: From Representation to Observation to Search",
        "Video Retrieval Is a Pipeline, Not a Single Benchmark Task",
        "The Benchmark–Reality Gap Is Structural",
        "The Coarse–Fine Gap Is Universal Across Model Families",
        "Search Scaling Couples Metric, Graph, and GPU Bottlenecks",
        "Ablation: Metric and Graph Are Both Necessary",
        "A1-6  Targeted Data Scaling Follows a Logarithmic Law",
    ):
        delete_slide_by_title(prs, design, title)

    # The overall data-scaling evidence is now in the main talk. Keep the more
    # detailed per-ability scaling page as the single backup data-scaling page.
    replace_on_slide(
        prs,
        "A1-7  GVE Data Scaling: Per-Ability Logarithmic Laws",
        "A1-7  GVE Data Scaling: Per-Ability Logarithmic Laws",
        "A1-6  GVE Data Scaling: Per-Ability Logarithmic Laws",
    )


def ensure_notes_master_registration(prs) -> None:
    design = load_design_system()
    design._register_notes_master(prs)


def validate_basic_package(path: Path) -> None:
    reloaded = Presentation(str(path))
    if len(reloaded.slides) != EXPECTED_SLIDES:
        raise AssertionError(f"Expected {EXPECTED_SLIDES} slides, got {len(reloaded.slides)}")

    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        for name in names:
            if name.endswith((".xml", ".rels")):
                ET.fromstring(archive.read(name))

        pres = ET.fromstring(archive.read("ppt/presentation.xml"))
        ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
        if pres.find("p:notesMasterIdLst", ns) is None:
            raise AssertionError("presentation.xml is missing notesMasterIdLst")

        slide_xml = b"\n".join(
            archive.read(name) for name in names
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        )
        if b"normAutofit" in slide_xml or b"fontScale" in slide_xml:
            raise AssertionError("Automatic font shrinking detected")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the original v0.5 base deck from v0.4.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    input_path = args.source.resolve()
    output_path = args.output.resolve()
    if not input_path.exists():
        raise FileNotFoundError(input_path)
    if output_path.exists():
        raise FileExistsError(f"Refusing to overwrite: {output_path}")
    if not FIGURES.exists():
        raise FileNotFoundError(FIGURES)

    design = load_design_system()
    prs = Presentation(str(input_path))

    apply_content_edits(prs)
    apply_structural_edits(prs, design)

    main_pages = renumber_main_pages(prs)
    backup_pages = renumber_backup_pages(prs)
    if main_pages != EXPECTED_MAIN_SLIDES - 3:  # title, roadmap, questions are unnumbered
        raise AssertionError(f"Unexpected numbered main pages: {main_pages}")
    if backup_pages != EXPECTED_BACKUP_PAGES:
        raise AssertionError(f"Unexpected backup page count: {backup_pages}")

    for slide in prs.slides:
        design._walk(slide.shapes)
    design._register_notes_master(prs)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))
    validate_basic_package(output_path)

    print(f"Saved {output_path}")
    print(f"Slides: {len(prs.slides)} (main {EXPECTED_MAIN_SLIDES}, backup pages {backup_pages})")
    print(f"Numbered main pages: {main_pages}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
