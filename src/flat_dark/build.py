"""ビルドスクリプト。

`uv run python -m flat_dark.build` で全スキン (`tokens.VARIANTS`) を
`dist/` 以下に生成する。
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from . import images, skin_xml
from . import tokens as T

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DIST_DIR = PROJECT_ROOT / "dist"


def build_variant(variant: T.SkinVariant) -> Path:
    """1 バリアントをビルドして zip パスを返す。"""
    out_dir = DIST_DIR / variant.name
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    # PNG ファイル生成
    pngs = images.generate_all(variant.tab_position)
    for filename, image in pngs.items():
        image.save(out_dir / filename, format="PNG", optimize=True)

    # skin.xml (UTF-16 LE)
    xml_text = skin_xml.render(variant)
    (out_dir / "skin.xml").write_bytes(skin_xml.to_bytes(xml_text))

    # zip
    zip_path = DIST_DIR / f"{variant.name}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(out_dir.iterdir()):
            zf.write(path, arcname=path.name)

    return zip_path


def main() -> None:
    DIST_DIR.mkdir(exist_ok=True)
    for variant in T.VARIANTS:
        zip_path = build_variant(variant)
        print(f"  built: {zip_path.relative_to(PROJECT_ROOT)}")
    print("done.")


if __name__ == "__main__":
    main()
