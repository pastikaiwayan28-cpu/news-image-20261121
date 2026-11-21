#!/usr/bin/env python3
"""Entry point for the news-image-20261121 competition.

Copies the pre-built front-page image (entry.png, next to this file)
to /output/entry.png, byte for byte, after validating that it is a
whole, well-formed PNG of at most 1 MiB and 1024x1024 pixels.

Standard library only. No network, no randomness, no clock: the two
grader runs therefore write identical bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import struct
import sys
import zlib

MAX_BYTES = 1048576
MAX_DIM = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("main.py: invalid entry.png: " + message, file=sys.stderr)
    return 1


def validate_png(data):
    """Check the PNG is whole: signature, IHDR size, CRC of every
    chunk, IEND present, and nothing trailing after IEND."""
    if len(data) > MAX_BYTES:
        return "size %d exceeds %d bytes" % (len(data), MAX_BYTES)
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        return "missing PNG signature"
    pos = 8
    seen_ihdr = False
    seen_iend = False
    first = True
    while pos < len(data):
        if pos + 8 > len(data):
            return "truncated chunk header at offset %d" % pos
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + length > len(data):
            return "truncated %s chunk at offset %d" % (ctype.decode("latin1"), pos)
        chunk_data = data[pos + 8:pos + 8 + length]
        stored_crc = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        actual_crc = zlib.crc32(ctype + chunk_data) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            return "CRC mismatch in %s chunk" % ctype.decode("latin1")
        if first:
            if ctype != b"IHDR":
                return "first chunk is not IHDR"
            if length != 13:
                return "IHDR has wrong length %d" % length
            width, height = struct.unpack(">II", chunk_data[:8])
            if width > MAX_DIM or height > MAX_DIM:
                return "dimensions %dx%d exceed %d" % (width, height, MAX_DIM)
            if width != 1024 or height != 1024:
                return "expected 1024x1024, got %dx%d" % (width, height)
            seen_ihdr = True
            first = False
        if ctype == b"IEND":
            if length != 0:
                return "IEND has nonzero length"
            seen_iend = True
            pos += 12 + length
            break
        pos += 12 + length
    if not seen_ihdr:
        return "no IHDR chunk"
    if not seen_iend:
        return "no IEND chunk"
    if pos != len(data):
        return "%d trailing bytes after IEND" % (len(data) - pos)
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    try:
        with open(src, "rb") as f:
            data = f.read()
    except OSError as exc:
        print("main.py: cannot read entry.png: %s" % exc, file=sys.stderr)
        return 1
    error = validate_png(data)
    if error is not None:
        return fail(error)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    # Verify the copy byte for byte: read it back and compare SHA-256.
    with open(dst, "rb") as f:
        written = f.read()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        return fail("written copy does not match entry.png (SHA-256)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
