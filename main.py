#!/usr/bin/env python3
"""THE WIDE LEDGER — entry program for news-image-20261123 (akun12, G4).

The Wide Ledger is a one-page broadsheet front page for Monday
23 November 2026: thirteen illustrated story cards led by the ICJ ruling
that Myanmar is guilty of genocide against the Rohingya, a day-in-numbers
box, a dotted world map with numbered pins, a red date-check box and an
ALSO ON column — forty stories, every one from that single day.

This program is stdlib-only and copy-only: it copies the entry.png that
sits beside it into the output directory, after checking the PNG magic,
the 1 MiB competition cap and the exact expected byte count and SHA-256
of the shipped image. Two runs produce byte-identical output.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 110160
EXPECTED_SHA256 = "eb4eda8612e96be6947582eb361a3d63774be054482112942f1858a541a294bc"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576  # 1 MiB competition cap


def load_entry():
    # Read the shipped image that lives next to this program.
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.png"), "rb") as fh:
        return fh.read()


def verify(data):
    if not data:
        sys.exit("entry.png is empty")
    if data[:8] != PNG_MAGIC:
        sys.exit("entry.png is not a PNG (bad magic bytes)")
    if len(data) > MAX_BYTES:
        sys.exit("entry.png exceeds 1 MiB: %d bytes" % len(data))
    if len(data) != EXPECTED_BYTES:
        sys.exit(
            "entry.png size changed: %d bytes, expected %d"
            % (len(data), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png sha256 changed: %s" % digest)
    return digest


def main():
    data = load_entry()
    digest = verify(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)
    sys.stderr.write("entry.png: %d bytes sha256=%s\n" % (len(data), digest))


if __name__ == "__main__":
    main()
