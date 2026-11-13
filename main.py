#!/usr/bin/env python3
"""Reproduce the make.fun entry image for the 13 November 2026 news digest.

The finished artwork ships beside this script as `entry.png`. This program
verifies the file is the exact image we published (by SHA-256), then copies it
byte for byte into the output directory. It uses only the Python standard
library, performs no network access, and produces the same result on every run.
"""

import hashlib
import os
import shutil
import sys

# SHA-256 of the published `entry.png` (713,088 bytes).
EXPECTED_SHA256 = "ce25d11f3d412dbf9ea223f5133b727344be5b623c4d63e8cdce9a85c5b939fc"

# The image file that sits next to this script.
IMAGE_NAME = "entry.png"
SOURCE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), IMAGE_NAME)

# Where the competition expects the entry, unless the caller overrides it.
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, IMAGE_NAME)

# The gate rejects anything larger than 1 MiB.
MAX_OUTPUT_BYTES = 1_048_576


def file_sha256(path):
    """Return the SHA-256 hex digest of the file at `path`."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        # Read in chunks so the whole file never has to sit in memory.
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_output_size(path):
    """Raise if the file at `path` exceeds the competition's 1 MiB cap."""
    size = os.path.getsize(path)
    if size > MAX_OUTPUT_BYTES:
        raise ValueError(
            "Output file %s is %d bytes, which exceeds the %d byte (1 MiB) limit."
            % (path, size, MAX_OUTPUT_BYTES)
        )
    return size


def main():
    # 1. Make sure the source image is present before doing anything else.
    if not os.path.isfile(SOURCE_PATH):
        raise FileNotFoundError(
            "Could not find %s next to main.py (looked in %s)."
            % (IMAGE_NAME, os.path.dirname(SOURCE_PATH))
        )

    # 2. Verify the image is the one we published. A mismatch means the
    #    artwork changed or the file is corrupt, so refuse to continue.
    actual_hash = file_sha256(SOURCE_PATH)
    if actual_hash != EXPECTED_SHA256:
        raise ValueError(
            "SHA-256 mismatch for %s: expected %s, got %s"
            % (SOURCE_PATH, EXPECTED_SHA256, actual_hash)
        )

    # 3. Create the output directory if it does not exist yet.
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 4. Copy the image byte for byte.
    shutil.copyfile(SOURCE_PATH, OUTPUT_PATH)

    # 5. The gate rejects anything over 1 MiB, so check the copied file now.
    check_output_size(OUTPUT_PATH)

    # 6. Guard against a truncated copy: the bytes written must match the
    #    source exactly. This is a cheap sanity check on the result.
    source_size = os.path.getsize(SOURCE_PATH)
    copied_size = os.path.getsize(OUTPUT_PATH)
    if copied_size != source_size:
        raise IOError(
            "Short copy: wrote %d bytes to %s but the source is %d bytes."
            % (copied_size, OUTPUT_PATH, source_size)
        )

    # 7. Confirm the copy is still the same image, not just the same length.
    copied_hash = file_sha256(OUTPUT_PATH)
    if copied_hash != EXPECTED_SHA256:
        raise ValueError(
            "Copied file failed verification: expected %s, got %s"
            % (EXPECTED_SHA256, copied_hash)
        )

    # 8. One-line confirmation for the competition log.
    print("Wrote %s: %d bytes, sha256=%s" % (OUTPUT_PATH, copied_size, copied_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())
