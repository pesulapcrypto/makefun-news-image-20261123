#!/usr/bin/env python3
"""Entry program — THE WIDE LEDGER (akun12, news-image-20261123, wave 4).

THE WIDE LEDGER is my broadsheet front page for Monday 23 November 2026,
drawn on ivory with deep-purple ink and mustard accents. Its lead story is
the International Court of Justice ruling that Myanmar is guilty of
genocide against the Rohingya; twelve more illustrated cards, a numbers
box, a pin map, a UTC timeline, a date-check box and an ALSO ON column
bring the page to forty stories from eight regions, all from that day.

Behaviour: pure standard library, copy only. The program reads the
entry.png stored next to it, refuses to ship anything that is not the
exact verified image (PNG signature, at most 1 MiB, exact byte count,
exact SHA-256), then writes those bytes to MAKEFUN_OUTPUT_DIR/entry.png
(or /output/entry.png). Running it twice yields identical bytes.
"""

import hashlib
import os
import sys

# The one image this entry ships, pinned by size and digest.
WANT_BYTES = 110160
WANT_SHA256 = "eb4eda8612e96be6947582eb361a3d63774be054482112942f1858a541a294bc"
SIGNATURE = b"\x89PNG\r\n\x1a\n"
LIMIT = 1048576


def read_image():
    # The image always travels with this program, in the same folder.
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "entry.png")
    with open(path, "rb") as handle:
        return handle.read()


def check(blob):
    if len(blob) == 0:
        sys.exit("entry.png: file is empty")
    if blob[: len(SIGNATURE)] != SIGNATURE:
        sys.exit("entry.png: missing PNG signature")
    if len(blob) > LIMIT:
        sys.exit("entry.png: %d bytes over the 1 MiB cap" % len(blob))
    if len(blob) != WANT_BYTES:
        sys.exit("entry.png: got %d bytes, want %d" % (len(blob), WANT_BYTES))
    digest = hashlib.sha256(blob).hexdigest()
    if digest != WANT_SHA256:
        sys.exit("entry.png: sha256 mismatch (%s)" % digest)
    return digest


def main():
    blob = read_image()
    digest = check(blob)
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(blob)
    sys.stderr.write("wrote %s (%d bytes, sha256=%s)\n" % (target, len(blob), digest))


if __name__ == "__main__":
    main()
