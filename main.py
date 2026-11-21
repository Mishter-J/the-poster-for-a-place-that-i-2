#!/usr/bin/env python3
"""VELMORA - The Poster for a Place That Isn't There (make.fun, program/v1).

Writes the finished travel poster to /output/entry.png.

The poster ships in this repository as poster.jpg (a 1024x1024 JPEG,
248,683 bytes) and is copied byte-for-byte. Stdlib only: no network,
no fonts, no third-party libraries, so the run is deterministic in any
sandbox. The sha256 below is a self-check that the shipped image was
not altered.
"""

import hashlib
from pathlib import Path

POSTER = Path(__file__).resolve().parent / "poster.jpg"
OUTPUT = Path("/output/entry.png")
EXPECTED_SHA256 = "72f79f5f189fe7b2e7dd332273bc966d84310dbcebed5ab44c225a17edf4882a"


def main() -> None:
    data = POSTER.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("poster.jpg does not match its recorded sha256")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(data)
    print(f"wrote {OUTPUT} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
