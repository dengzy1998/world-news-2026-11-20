#!/usr/bin/env python3
"""Competition entrypoint for news-image-20261120.

The rendered newspaper page lives beside this file as ``entry.png``.
Grading expects that page at ``/output/entry.png``, so this program
moves a copy there. It relies on nothing outside the Python standard
library, which keeps it working in the plain grading container.
"""

from pathlib import Path
import sys

PAGE_NAME = "entry.png"
OUTPUT_FOLDER = Path("/output")


def locate_page() -> Path:
    """Return the path of the page image stored in this repository."""
    return Path(__file__).resolve().parent / PAGE_NAME


def publish(page: Path) -> int:
    """Copy ``page`` into the output folder; return its size in bytes."""
    payload = page.read_bytes()
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    target = OUTPUT_FOLDER / PAGE_NAME
    target.write_bytes(payload)
    return len(payload)


def main() -> int:
    page = locate_page()
    if not page.exists():
        print(f"missing page image: {page}", file=sys.stderr)
        return 1
    size = publish(page)
    print(f"published {PAGE_NAME}: {size} bytes -> {OUTPUT_FOLDER / PAGE_NAME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
