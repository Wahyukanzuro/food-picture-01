import base64
import os
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    image_bytes = base64.b64decode((here / "image.b64").read_text().strip())
    if image_bytes[:3] != b"\xff\xd8\xff":
        raise ValueError("entry is not a JPEG (bad magic bytes)")
    if len(image_bytes) > 1024 * 1024:
        raise ValueError("entry exceeds the 1 MiB limit")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.png").write_bytes(image_bytes)


if __name__ == "__main__":
    main()
