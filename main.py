#!/usr/bin/env python3
"""Entry point for the make.fun bounty news-image-20261120.

The front page is already drawn: entry.png is produced by make_image.py
and shipped in this repository. This program only copies that file to
the grader's output location. It uses nothing beyond the Python standard
library, so it runs in the bare grader image with no network and no
third-party packages.
"""

import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
TARGET = Path("/output") / "entry.png"


def run() -> int:
    if not SOURCE.is_file():
        print("error: entry.png is missing next to main.py", file=sys.stderr)
        return 1
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    print("wrote", TARGET, TARGET.stat().st_size, "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
