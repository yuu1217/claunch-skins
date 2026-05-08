"""dist/ 内のスキン画像を CLaunch が描画するイメージで合成プレビューを作る。

`uv run python -m flat_dark.preview` で `dist/<variant>/preview.png` を生成。
画像が暗背景に対するアルファ込みなので、単独ファイルでは見えづらい部分を
合成して確認するために使う。
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from . import images as I
from . import tokens as T

DESKTOP_GRADIENT_TOP = (50, 70, 110, 255)
DESKTOP_GRADIENT_BOT = (28, 32, 60, 255)


def _desktop_bg(w: int, h: int) -> Image.Image:
    """擬似デスクトップ背景 (Win11 風のグラデ)。"""
    img = Image.new("RGBA", (w, h))
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(
            round(DESKTOP_GRADIENT_TOP[i] * (1 - t) + DESKTOP_GRADIENT_BOT[i] * t)
            for i in range(4)
        )
        for x in range(w):
            px[x, y] = c  # type: ignore[index]
    return img


def _scale(img: Image.Image, factor: int) -> Image.Image:
    return img.resize((img.width * factor, img.height * factor), Image.Resampling.NEAREST)


def make_preview(variant: T.SkinVariant) -> Image.Image:
    """変換済みスプライトを並べて表示するプレビュー画像。"""
    pngs = I.generate_all(variant.tab_position)

    # 各スプライトを 4 倍拡大して並べ、暗背景上に重ねる
    SCALE = 4
    PAD = 16
    TITLE_H = 16

    # 暗いデスクトップ上での見え方を確認するための背景
    items: list[tuple[str, Image.Image]] = [(name, img) for name, img in pngs.items()]

    # 全アイテムが収まる幅を計算 (横 4 列で並べる)
    cols = 4
    rows = (len(items) + cols - 1) // cols
    cell_w = max(img.width * SCALE for _, img in items) + PAD * 2
    cell_h = max(img.height * SCALE for _, img in items) + PAD * 2 + TITLE_H

    canvas_w = cols * cell_w + PAD
    canvas_h = rows * cell_h + PAD

    canvas = _desktop_bg(canvas_w, canvas_h)
    draw = ImageDraw.Draw(canvas)

    for i, (name, img) in enumerate(items):
        c = i % cols
        r = i // cols
        x = c * cell_w + PAD
        y = r * cell_h + PAD

        # ラベル
        draw.text((x, y), name, fill=(220, 220, 220, 255))
        # 拡大画像 (元サイズが小さいものほど拡大して見やすく)
        scaled = _scale(img, SCALE)
        canvas.alpha_composite(scaled, (x, y + TITLE_H))

    return canvas


def make_window_mockup(variant: T.SkinVariant) -> Image.Image:
    """CLaunch がウィンドウとして合成した場合の見た目を擬似的に再現。

    ・window.png を 9-slice で展開して 480×320 のウィンドウとして描画
    ・グリッド領域に button.png の hover 状態を一つ配置
    ・タブ領域に tab.png を配置
    ・システムボタン4種を右上に配置
    """
    desktop = _desktop_bg(560, 400)

    # ウィンドウサイズ
    win_w, win_h = 480, 320
    win_x, win_y = 40, 32

    # === window.png を 9-slice で展開 ===
    window_src = I.make_window_image()
    rendered_window = _nine_slice_render(
        window_src, win_w, win_h,
        slices_top=T.TOP_FRAME_H,
        slices_bottom=T.BOT_FRAME_H,
        slices_left=8,
        slices_right=T.RIGHT_FRAME_W,
    )
    desktop.alpha_composite(rendered_window, (win_x, win_y))

    # === ボタンを 6×5 配置 (中央領域) ===
    button_src = I.make_button_image()
    btn_w, btn_h = T.BUTTON_W, T.BUTTON_H
    grid_origin_x = win_x + 16
    grid_origin_y = win_y + 36
    for row in range(5):
        for col in range(6):
            # 全部 normal、ただし (1, 2) を hover, (2, 3) を down にしてサンプル
            state_idx = 0
            if (row, col) == (1, 2):
                state_idx = 1  # hover
            elif (row, col) == (2, 3):
                state_idx = 2  # down
            sub = button_src.crop((0, btn_h * state_idx, btn_w, btn_h * (state_idx + 1)))
            x = grid_origin_x + col * (btn_w + 4)
            y = grid_origin_y + row * (btn_h + 4)
            desktop.alpha_composite(sub, (x, y))

    # === タブを下端に配置 ===
    tab_src = I.make_tab_image()
    tab_w, tab_h = T.TAB_W, T.TAB_H
    tab_origin_x = win_x + 16
    tab_origin_y = win_y + win_h - tab_h - 20
    for col in range(4):
        state_idx = 0
        if col == 1:
            state_idx = 1
        elif col == 3:
            state_idx = 2
        sub = tab_src.crop((0, tab_h * state_idx, tab_w, tab_h * (state_idx + 1)))
        x = tab_origin_x + col * (tab_w + 2)
        desktop.alpha_composite(sub, (x, tab_origin_y))

    # === システムボタン (4 個 normal で配置 / 右上に Close-Pin-Mode、左上に Search) ===
    sys_src = I.make_sysbutton_image()
    sys_cell = T.SYSBTN_CELL
    # Search at left
    desktop.alpha_composite(sys_src.crop((0, 0, sys_cell, sys_cell)), (win_x, win_y))
    # Mode/Pin/Close at right (列順 1,2,3 = Mode/Pin/Close)
    for i, col in enumerate((1, 2, 3)):
        sub = sys_src.crop(
            (col * sys_cell, 0, (col + 1) * sys_cell, sys_cell)
        )
        x = win_x + win_w - 16 - sys_cell * (3 - i)
        desktop.alpha_composite(sub, (x, win_y))

    return desktop


def _nine_slice_render(
    src: Image.Image, dst_w: int, dst_h: int,
    slices_top: int, slices_bottom: int, slices_left: int, slices_right: int,
) -> Image.Image:
    """ソース画像を 9-slice で dst_w × dst_h に引き伸ばす。

    src の四隅は固定、辺は引き伸ばし。
    シンプルな実装なので CLaunch とは厳密に一致しないが視覚確認用には十分。
    """
    sw, sh = src.width, src.height
    sl, sr = slices_left, slices_right
    st, sb = slices_top, slices_bottom

    # ソースを 9 個に切り出し
    parts = {
        "tl": src.crop((0, 0, sl, st)),
        "tc": src.crop((sl, 0, sw - sr, st)),
        "tr": src.crop((sw - sr, 0, sw, st)),
        "ml": src.crop((0, st, sl, sh - sb)),
        "mc": src.crop((sl, st, sw - sr, sh - sb)),
        "mr": src.crop((sw - sr, st, sw, sh - sb)),
        "bl": src.crop((0, sh - sb, sl, sh)),
        "bc": src.crop((sl, sh - sb, sw - sr, sh)),
        "br": src.crop((sw - sr, sh - sb, sw, sh)),
    }

    # 出力サイズ
    out = Image.new("RGBA", (dst_w, dst_h), (0, 0, 0, 0))
    mid_w = dst_w - sl - sr
    mid_h = dst_h - st - sb

    def stretch(p: Image.Image, w: int, h: int) -> Image.Image:
        if w <= 0 or h <= 0:
            return Image.new("RGBA", (max(0, w), max(0, h)))
        return p.resize((w, h), Image.Resampling.BILINEAR)

    out.alpha_composite(parts["tl"], (0, 0))
    out.alpha_composite(stretch(parts["tc"], mid_w, st), (sl, 0))
    out.alpha_composite(parts["tr"], (dst_w - sr, 0))
    out.alpha_composite(stretch(parts["ml"], sl, mid_h), (0, st))
    out.alpha_composite(stretch(parts["mc"], mid_w, mid_h), (sl, st))
    out.alpha_composite(stretch(parts["mr"], sr, mid_h), (dst_w - sr, st))
    out.alpha_composite(parts["bl"], (0, dst_h - sb))
    out.alpha_composite(stretch(parts["bc"], mid_w, sb), (sl, dst_h - sb))
    out.alpha_composite(parts["br"], (dst_w - sr, dst_h - sb))
    return out


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    dist = project_root / "dist"
    for variant in T.VARIANTS:
        out_dir = dist / variant.name
        if not out_dir.exists():
            print(f"  skip (not built): {variant.name}")
            continue
        # スプライト一覧
        preview = make_preview(variant)
        preview.save(out_dir / "_preview-sprites.png")
        # ウィンドウモックアップ
        mockup = make_window_mockup(variant)
        mockup.save(out_dir / "_preview-mockup.png")
        print(f"  preview: {variant.name}")
    print("done.")


if __name__ == "__main__":
    main()
