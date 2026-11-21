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
import struct
from pathlib import Path

POSTER = Path(__file__).resolve().parent / "poster.jpg"
OUTPUT = Path("/output/entry.png")
EXPECTED_SHA256 = "72f79f5f189fe7b2e7dd332273bc966d84310dbcebed5ab44c225a17edf4882a"
MAX_BYTES = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Parse width/height from the first SOF0/SOF2 marker (no Pillow)."""
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG (missing SOI marker)")
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            raise ValueError(f"bad JPEG marker at offset {pos}")
        marker = data[pos + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        seg_len = struct.unpack(">H", data[pos + 2 : pos + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2):
            if seg_len < 7:
                raise ValueError("truncated SOF segment")
            height = struct.unpack(">H", data[pos + 5 : pos + 7])[0]
            width = struct.unpack(">H", data[pos + 7 : pos + 9])[0]
            return width, height
        pos += 2 + seg_len
    raise ValueError("no SOF marker found")


def verify_output(data: bytes) -> None:
    """Verify the written output: JPEG magic, size cap, exact dimensions."""
    if data[:2] != b"\xff\xd8":
        raise SystemExit("output does not start with JPEG magic bytes FF D8")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"output is {len(data)} bytes, over the 1 MiB cap")
    width, height = jpeg_dimensions(data)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            f"output is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )


def main() -> None:
    data = POSTER.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("poster.jpg does not match its recorded sha256")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(data)
    verify_output(data)
    print(
        f"wrote {OUTPUT} ({len(data)} bytes), "
        f"verified JPEG {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
    )


if __name__ == "__main__":
    main()
