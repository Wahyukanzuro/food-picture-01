import base64
import os
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
JPEG_MAGIC = b"\xff\xd8\xff"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    here = Path(__file__).resolve().parent
    data = base64.b64decode((here / "image.b64").read_text().strip())
    if len(data) > MAX_BYTES:
        sys.exit(f"image exceeds 1 MiB cap: {len(data)} bytes")
    if not (data[:3] == JPEG_MAGIC or data[:8] == PNG_MAGIC):
        sys.exit("image is neither JPEG nor PNG (bad magic bytes)")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "."))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    out.write_bytes(data)
    print(f"wrote {out} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
