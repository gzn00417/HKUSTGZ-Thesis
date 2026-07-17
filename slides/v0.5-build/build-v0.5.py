#!/usr/bin/env python3
"""Rebuild the final v0.5 defense deck from the unchanged v0.4 deck.

The final v0.5 incorporates the original v0.5 restructuring, the committee
review formerly developed through v0.6.3, and the evidence-boundary calibration
formerly finalized as v0.6.6. Intermediate PPTX files live only in a temporary
directory and are removed after the build.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SLIDES_DIR = HERE.parent
SUPPORT = HERE
DEFAULT_SOURCE = SLIDES_DIR / "thesis-slides-v0.4.pptx"
DEFAULT_OUTPUT = SLIDES_DIR / "thesis-slides-v0.5.pptx"


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, env=os.environ.copy())


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the consolidated final v0.5 deck.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    if not source.exists():
        raise FileNotFoundError(source)
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite: {output}")

    node = shutil.which("node")
    if not node:
        raise RuntimeError("Node.js is required for the two final review stages.")

    with tempfile.TemporaryDirectory(prefix="thesis-slides-v05-") as tmp:
        tmpdir = Path(tmp)
        base = tmpdir / "base-v0.5.pptx"
        reviewed = tmpdir / "committee-reviewed.pptx"
        run([sys.executable, str(SUPPORT / "base.py"), "--source", str(source), "--output", str(base)])
        run([node, str(SUPPORT / "committee-review.mjs"), "--source", str(base), "--output", str(reviewed)])
        run([node, str(SUPPORT / "evidence-calibration.mjs"), "--source", str(reviewed), "--output", str(output)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
