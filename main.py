#!/usr/bin/env python3
# news-image-20261120 entry program.
#
# The newspaper page for Friday 20 November 2026 ships in this repository
# as entry.png, already rendered. All this program has to do at grading
# time is deliver those bytes to the output path the grader reads, using
# only the standard library so it works in the bare grading image.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "entry.png")
DEST = os.path.join("/output", "entry.png")
CHUNK = 65536


def deliver() -> int:
    if not os.path.isfile(PAGE):
        sys.stderr.write("entry.png not found beside main.py\n")
        return 1
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    total = 0
    with open(PAGE, "rb") as src, open(DEST, "wb") as dst:
        while True:
            block = src.read(CHUNK)
            if not block:
                break
            dst.write(block)
            total += len(block)
    print("entry.png delivered:", total, "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(deliver())
