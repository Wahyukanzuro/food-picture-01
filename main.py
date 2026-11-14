#!/usr/bin/env python3
"""food-picture-01 entry: write the food picture to $MAKEFUN_OUTPUT_DIR/entry.png.

The picture ships in the repo as image.b64 (base64, one line) because the
GitHub connector cannot push binary files. This program decodes it at
runtime and writes the bytes to the output directory.
"""

import base64
import os
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    b64_path = here / "image.b64"

    with open(b64_path, "r", encoding="ascii") as f:
        data = base64.b64decode(f.read().strip())

    if not (data.startswith(b"\xff\xd8\xff") or data.startswith(b"\x89PNG")):
        raise ValueError("image.b64 does not decode to a JPEG or PNG image")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "entry.png"
    with open(out_path, "wb") as f:
        f.write(data)

    print(f"Wrote {len(data)} bytes to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
