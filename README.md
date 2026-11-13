# news-image-13nov — Friday 13 November 2026 news digest

This entry is a single 1024x1024 image that sums up the world news of Friday 13 November 2026 as a six-panel newspaper-style digest. The finished artwork is shipped in this repository as `entry.png`; `main.py` verifies it and writes a byte-identical copy to the output directory the competition reads from, with no network access and no third-party dependencies.

The six stories shown in the panels are:

- Microsoft Teams and Outlook suffered a widespread outage.
- Vladimir Putin raised his peace demands.
- North Korea stole roughly $400m in crypto using fake video calls.
- A baby died of cold in Gaza.
- A bus and truck crash in Assam, India, killed 24 people.
- Rosalía won her third Latin Grammy for best album.

To run it, use the standard library Python 3 interpreter from this directory:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program reads `entry.png` beside it, checks its SHA-256 against the published digest, and copies it into `MAKEFUN_OUTPUT_DIR` (default `/output`) as `entry.png`, creating the directory if needed. It prints one line with the byte count and digest, and exits non-zero with a clear error if the source is missing, the hash does not match, or the copy is short.

The gate accepts PNG or JPEG only, at most 1 MiB in size, and at most 1024x1024 pixels. This entry is a 713,088-byte PNG at exactly 1024x1024, so it sits comfortably inside every limit.

## Checks performed

`main.py` runs three verifications before it reports success:

- **Hash match** — the source `entry.png` has SHA-256 `ce25d11f…c5b939fc`, the digest of the published artwork; a different digest aborts the run.
- **Byte-identical copy** — the output file is compared against the source size and re-hashed after copying, so a truncated or altered copy fails.
- **Size under the 1 MiB cap** — the copied file is checked against 1,048,576 bytes and a `ValueError` reports the real size if it is ever exceeded.

