"""PNG スプライトを Pillow で生成する。

各 `make_*_image()` は 32bpp RGBA の PIL.Image を返す。
build.py が dist/ に保存する。
"""

from __future__ import annotations

from collections.abc import Callable

from PIL import Image, ImageDraw

from . import tokens as T

ICON_SUPERSAMPLE = 4
"""アイコン描画時のオーバーサンプリング倍率。1px線をきれいに見せる。"""


# ---------------------------------------------------------------------------
# 共通ヘルパー
# ---------------------------------------------------------------------------

def _new(w: int, h: int, color: T.RGBA = T.TRANSPARENT) -> Image.Image:
    return Image.new("RGBA", (w, h), color)


def _supersampled(
    w: int, h: int, draw_fn: Callable[[ImageDraw.ImageDraw, int], None],
    scale: int = ICON_SUPERSAMPLE,
) -> Image.Image:
    """draw_fn(draw, scale) を w*scale × h*scale で実行し、LANCZOS で縮小。"""
    big = _new(w * scale, h * scale)
    draw_fn(ImageDraw.Draw(big), scale)
    return big.resize((w, h), Image.Resampling.LANCZOS)


def _filled_rounded(w: int, h: int, radius: int, fill: T.RGBA,
                    stroke: T.RGBA | None = None) -> Image.Image:
    """角丸矩形のフィル（オプションで 1px ストローク）画像。"""
    img = _new(w, h)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        (0, 0, w - 1, h - 1), radius=radius, fill=fill,
        outline=stroke, width=1 if stroke else 0,
    )
    return img


# CLaunch の仕様: alphaChannel="true" 下では alpha=0 のピクセルはクリック判定外。
# 完全に見せたくないが「クリックは受ける」状態を作るための極薄黒。
HITTEST_ALPHA: T.RGBA = (0, 0, 0, 1)


# ---------------------------------------------------------------------------
# window.png
# ---------------------------------------------------------------------------

def make_window_image() -> Image.Image:
    """88×96 の不透明パネル + 1px ストローク + 上端ハイライト。"""
    return _make_mica_panel(T.WINDOW_PNG_W, T.WINDOW_PNG_H, T.RADIUS_WINDOW)


def _make_mica_panel(w: int, h: int, radius: int) -> Image.Image:
    """完全不透明な角丸パネルを生成。

    CLaunch側のアルファ判定を安定させるため、角丸外側以外はalpha=255にする。
    """
    surface = _new(w, h)
    sdraw = ImageDraw.Draw(surface)

    # ベース塗り潰し
    sdraw.rounded_rectangle(
        (0, 0, w - 1, h - 1), radius=radius, fill=T.SURFACE_MICA,
    )
    # 外周ストローク
    sdraw.rounded_rectangle(
        (0, 0, w - 1, h - 1), radius=radius,
        outline=T.STROKE_WINDOW, width=1,
    )
    # 上端 1px ハイライト
    sdraw.line(
        [(radius, 1), (w - 1 - radius, 1)],
        fill=T.STROKE_HIGHLIGHT, width=1,
    )
    return surface


# ---------------------------------------------------------------------------
# caption.png — 1×1 極薄黒
# ---------------------------------------------------------------------------

def make_caption_image() -> Image.Image:
    """1×1 の極薄黒。完全透明だとクリック判定外になるため。"""
    return _new(T.CAPTION_W, T.CAPTION_H, HITTEST_ALPHA)


# ---------------------------------------------------------------------------
# tabarea.png — 4×4、上 or 下に 1px セパレーター線
# ---------------------------------------------------------------------------

def make_tabarea_image(tab_position: T.TabPosition) -> Image.Image:
    img = _new(T.AREA_W, T.AREA_H)
    draw = ImageDraw.Draw(img)
    if tab_position == "bottom":
        # ボタン領域とタブ領域の間 = タブエリアの上端に線
        draw.line([(0, 0), (T.AREA_W - 1, 0)], fill=T.STROKE_TAB_SEP, width=1)
    else:
        # Top の場合はタブエリアの下端に線
        draw.line(
            [(0, T.AREA_H - 1), (T.AREA_W - 1, T.AREA_H - 1)],
            fill=T.STROKE_TAB_SEP, width=1,
        )
    return img


# ---------------------------------------------------------------------------
# buttonarea.png — 4×4 完全透明
# ---------------------------------------------------------------------------

def make_buttonarea_image() -> Image.Image:
    return _new(T.AREA_W, T.AREA_H)


# ---------------------------------------------------------------------------
# tab.png — 140×114 (3 状態)
# ---------------------------------------------------------------------------

def make_tab_image() -> Image.Image:
    img = _new(T.TAB_PNG_W, T.TAB_PNG_H)
    # 視覚表現は文字色だけに任せ、alpha=1でクリック判定は維持する。
    hit_area = _new(T.TAB_W, T.TAB_H, HITTEST_ALPHA)
    for state_index in range(3):
        img.alpha_composite(hit_area, (0, T.TAB_H * state_index))
    return img


# ---------------------------------------------------------------------------
# button.png — 100×300 (3 状態)
# ---------------------------------------------------------------------------

def make_button_image() -> Image.Image:
    img = _new(T.BUTTON_PNG_W, T.BUTTON_PNG_H)
    # normal: 視覚的には透明、alpha=1 でクリック判定を確保
    # (これがないと CLaunch のデフォルト動作 "モード切替" が発動する)
    normal = _new(T.BUTTON_W, T.BUTTON_H, HITTEST_ALPHA)
    img.alpha_composite(normal, (0, 0))
    # hover: 背景 + ストローク
    hover = _filled_rounded(
        T.BUTTON_W, T.BUTTON_H, T.RADIUS_BUTTON,
        T.CELL_HOVER_BG, stroke=T.CELL_HOVER_STROKE,
    )
    img.alpha_composite(hover, (0, T.BUTTON_H))
    # down: 薄い背景のみ、ストロークなし
    down = _filled_rounded(
        T.BUTTON_W, T.BUTTON_H, T.RADIUS_BUTTON,
        T.CELL_DOWN_BG,
    )
    img.alpha_composite(down, (0, T.BUTTON_H * 2))
    return img


# ---------------------------------------------------------------------------
# lockmarker.png — 14×14 アクセント色のドット
# ---------------------------------------------------------------------------

def make_lockmarker_image() -> Image.Image:
    """フラット: アクセント色の小さなドット + 1px ホワイト縁。"""
    img = _new(T.LOCKMARKER_W, T.LOCKMARKER_H)
    draw = ImageDraw.Draw(img)
    cx = T.LOCKMARKER_W // 2
    cy = T.LOCKMARKER_H // 2
    # アクセント色ドット (ストローク付き)
    draw.ellipse(
        (cx - 4, cy - 4, cx + 4, cy + 4),
        fill=T.ACCENT, outline=(255, 255, 255, 200), width=1,
    )
    return img


# ---------------------------------------------------------------------------
# sysbutton.png — 176×176 (4ボタン × 4状態)
# ---------------------------------------------------------------------------

def make_sysbutton_image() -> Image.Image:
    """各セル 44×44。
    列: Search, Mode, Pin, Close
    行: normal, hover, down, downhover
    """
    img = _new(T.SYSBTN_PNG_W, T.SYSBTN_PNG_H)

    # 4状態 × 4ボタンの背景 + アイコンを描画
    button_kinds = ("search", "mode", "pin", "close")
    states = ("normal", "hover", "down", "downhover")

    for col, kind in enumerate(button_kinds):
        for row, state in enumerate(states):
            cell = _new(T.SYSBTN_CELL, T.SYSBTN_CELL)
            _draw_sysbutton_cell(cell, kind, state)
            img.alpha_composite(cell, (col * T.SYSBTN_CELL, row * T.SYSBTN_CELL))
    return img


def _draw_sysbutton_cell(canvas: Image.Image, kind: str, state: str) -> None:
    """1セル分 (44×44) を描画。canvas に直接合成する。

    セル全体を HITTEST_ALPHA で埋め、アイコン以外の余白でも
    マウス hover/click が効くようにする。
    """
    # セル全体を alpha=1 で塗る (hover判定をセル全体で効かせる)
    hit_base = _new(T.SYSBTN_CELL, T.SYSBTN_CELL, HITTEST_ALPHA)
    canvas.alpha_composite(hit_base, (0, 0))

    # === 背景 ===
    bg_color: T.RGBA | None = None
    if kind == "close":
        if state == "hover":
            bg_color = T.CLOSE_HOVER_BG
        elif state == "down":
            bg_color = T.CLOSE_DOWN_BG
        elif state == "downhover":
            bg_color = T.CLOSE_HOVER_BG
    else:
        if state == "hover":
            bg_color = T.SYSBTN_HOVER_BG
        elif state == "down":
            bg_color = T.SYSBTN_DOWN_BG
        elif state == "downhover":
            bg_color = T.SYSBTN_HOVER_BG

    if bg_color:
        # 28×24 の角丸下地、セル中央に配置
        bg = _filled_rounded(
            T.SYSBTN_INNER, T.SYSBTN_INNER_H, T.RADIUS_SYSBTN, bg_color,
        )
        bx = (T.SYSBTN_CELL - T.SYSBTN_INNER) // 2
        by = (T.SYSBTN_CELL - T.SYSBTN_INNER_H) // 2
        canvas.alpha_composite(bg, (bx, by))

    # === アイコン色 ===
    icon_color: T.RGBA = T.TEXT_FG
    if kind == "close" and state in {"hover", "down", "downhover"}:
        icon_color = (255, 255, 255, 255)

    # === アイコン本体 ===
    # 18×18 の領域にスーパーサンプリング描画してセル中央に貼る (Mode は 20×20 で大きめに)
    icon_size = 20 if kind == "mode" else 18
    icon = _supersampled(
        icon_size, icon_size,
        lambda d, s: _draw_icon(d, s, icon_size, kind, state, icon_color),
    )
    ix = (T.SYSBTN_CELL - icon_size) // 2
    iy = (T.SYSBTN_CELL - icon_size) // 2
    canvas.alpha_composite(icon, (ix, iy))


def _draw_icon(
    draw: ImageDraw.ImageDraw, scale: int, size: int,
    kind: str, state: str, color: T.RGBA,
) -> None:
    """size×size アイコンを scale 倍で描画。座標は size px ベース。

    元々 12px ベースだったロジックを size に合わせてスケールする
    (係数は size/12 で内部的に調整)。
    """
    s = scale
    k = size / 12.0  # 12px → size の倍率
    cx, cy = (size // 2) * s, (size // 2) * s
    line_w = max(1, round(1.4 * s))

    def sx(v: float) -> int:
        return round(v * k * s)

    if kind == "search":
        r = sx(3.5)
        offset = sx(1)
        draw.ellipse(
            (cx - r - offset, cy - r - offset, cx + r - offset, cy + r - offset),
            outline=color, width=line_w,
        )
        # 持ち手 (右下方向)
        hx0, hy0 = cx + sx(2.0), cy + sx(2.0)
        hx1, hy1 = cx + sx(4.5), cy + sx(4.5)
        draw.line([(hx0, hy0), (hx1, hy1)], fill=color, width=line_w)

    elif kind == "mode":
        if state in {"normal", "hover"}:
            # 4つの小矩形 (塗り潰し、Win11 グリッド表示風)
            sz = sx(2.4)
            gap = sx(1.2)
            offset = (sz + gap) // 2
            for ix in (-1, 1):
                for iy in (-1, 1):
                    x0 = cx + ix * offset - sz // 2
                    y0 = cy + iy * offset - sz // 2
                    draw.rectangle(
                        (x0, y0, x0 + sz, y0 + sz),
                        fill=color,
                    )
        else:
            # 3本の横棒 (塗り潰し、Win11 リスト表示風)
            bar_h = sx(1.6)
            bar_w = sx(9)
            for dy in (-3, 0, 3):
                y = cy + sx(dy)
                draw.rectangle(
                    (cx - bar_w // 2, y - bar_h // 2,
                     cx + bar_w // 2, y + bar_h // 2),
                    fill=color,
                )

    elif kind == "pin":
        if state in {"normal", "hover"}:
            head_size = sx(4)
            hx0 = cx - head_size // 2
            hy0 = cy - head_size // 2 - sx(2)
            draw.rectangle(
                (hx0, hy0, hx0 + head_size, hy0 + head_size),
                outline=color, width=line_w,
            )
            draw.line(
                [(cx, hy0 + head_size), (cx, hy0 + head_size + sx(4))],
                fill=color, width=line_w,
            )
        else:
            # ピン留め中: 塗りつぶし
            head_size = sx(5)
            hx0 = cx - head_size // 2
            hy0 = cy - head_size // 2 - sx(1)
            draw.rectangle(
                (hx0, hy0, hx0 + head_size, hy0 + head_size),
                fill=color,
            )
            draw.line(
                [(cx, hy0 + head_size), (cx, hy0 + head_size + sx(4))],
                fill=color, width=line_w + 1,
            )

    elif kind == "close":
        d = sx(3.5)
        draw.line([(cx - d, cy - d), (cx + d, cy + d)], fill=color, width=line_w)
        draw.line([(cx + d, cy - d), (cx - d, cy + d)], fill=color, width=line_w)


# ---------------------------------------------------------------------------
# menuframe.png — 56×56
# ---------------------------------------------------------------------------

def make_menuframe_image() -> Image.Image:
    """サブメニューの枠 (window.png と同質感の小型版、フラット)。"""
    return _make_mica_panel(T.MENU_PNG_W, T.MENU_PNG_H, T.RADIUS_MENU)


# ---------------------------------------------------------------------------
# menuitem.png — 48×108 (3 状態)
# ---------------------------------------------------------------------------

def make_menuitem_image() -> Image.Image:
    img = _new(T.MENUITEM_PNG_W, T.MENUITEM_PNG_H)
    # normal: 視覚は透明だが alpha=1 でクリック判定を生かす
    normal = _new(T.MENUITEM_W, T.MENUITEM_H, HITTEST_ALPHA)
    img.alpha_composite(normal, (0, 0))
    # selected
    sel = _filled_rounded(
        T.MENUITEM_W, T.MENUITEM_H, T.RADIUS_MENUITEM,
        T.CELL_HOVER_BG, stroke=T.CELL_HOVER_STROKE,
    )
    img.alpha_composite(sel, (0, T.MENUITEM_H))
    # multisel (アクセント混じり)
    multi = _filled_rounded(
        T.MENUITEM_W, T.MENUITEM_H, T.RADIUS_MENUITEM,
        (T.ACCENT_DEEP[0], T.ACCENT_DEEP[1], T.ACCENT_DEEP[2], 64),
        stroke=(T.ACCENT[0], T.ACCENT[1], T.ACCENT[2], 153),
    )
    img.alpha_composite(multi, (0, T.MENUITEM_H * 2))
    return img


# ---------------------------------------------------------------------------
# scrollbutton.png — 16×64 (4 状態)
# ---------------------------------------------------------------------------

def make_scrollbutton_image() -> Image.Image:
    img = _new(T.SCROLLBTN_PNG_W, T.SCROLLBTN_PNG_H)
    # normal: 視覚は透明だが alpha=1 でクリック判定を生かす
    img.alpha_composite(
        _new(T.SCROLLBTN_W, T.SCROLLBTN_H, HITTEST_ALPHA), (0, 0),
    )
    # hover
    img.alpha_composite(
        _filled_rounded(T.SCROLLBTN_W, T.SCROLLBTN_H, 4, T.CELL_HOVER_BG),
        (0, T.SCROLLBTN_H),
    )
    # down
    img.alpha_composite(
        _filled_rounded(T.SCROLLBTN_W, T.SCROLLBTN_H, 4, T.CELL_DOWN_BG),
        (0, T.SCROLLBTN_H * 2),
    )
    # disabled: 完全透明のまま (クリック貫通 = OK、機能しないので)
    return img


# ---------------------------------------------------------------------------
# arrowud.png / arrowlr.png — 16×64 (2 方向 × 4 状態)
# ---------------------------------------------------------------------------

def make_arrowud_image() -> Image.Image:
    """上下矢印: 左列 = up, 右列 = down。"""
    return _make_arrow_image(directions=("up", "down"))


def make_arrowlr_image() -> Image.Image:
    """左右矢印: 左列 = left, 右列 = right。"""
    return _make_arrow_image(directions=("left", "right"))


def _make_arrow_image(directions: tuple[str, str]) -> Image.Image:
    img = _new(T.ARROW_PNG_W, T.ARROW_PNG_H)
    states = ("normal", "hover", "down", "disabled")
    for col, direction in enumerate(directions):
        for row, state in enumerate(states):
            color = _arrow_color(state)
            cell = _supersampled(
                T.ARROW_CELL_W, T.ARROW_CELL_H,
                lambda d, s, c=color, dr=direction:
                    _draw_arrow(d, s, dr, c),
            )
            img.alpha_composite(
                cell, (col * T.ARROW_CELL_W, row * T.ARROW_CELL_H),
            )
    return img


def _arrow_color(state: str) -> T.RGBA:
    if state == "disabled":
        return (T.TEXT_SUBTLE[0], T.TEXT_SUBTLE[1], T.TEXT_SUBTLE[2], 128)
    if state in {"hover", "down"}:
        return T.TEXT_FG
    return T.TEXT_MUTED


def _draw_arrow(
    draw: ImageDraw.ImageDraw, scale: int, direction: str, color: T.RGBA,
) -> None:
    """ARROW_CELL (8×16) サイズに矢印を描く (scale 倍)。
    シンプルなシェブロン (山形 \\/) を描画。
    """
    s = scale
    line_w = max(1, round(1.2 * s))
    cx, cy = 4 * s, 8 * s
    arm = round(2.5 * s)
    if direction == "up":
        draw.line([(cx - arm, cy + arm // 2), (cx, cy - arm)], fill=color, width=line_w)
        draw.line([(cx, cy - arm), (cx + arm, cy + arm // 2)], fill=color, width=line_w)
    elif direction == "down":
        draw.line([(cx - arm, cy - arm // 2), (cx, cy + arm)], fill=color, width=line_w)
        draw.line([(cx, cy + arm), (cx + arm, cy - arm // 2)], fill=color, width=line_w)
    elif direction == "left":
        draw.line([(cx + arm // 2, cy - arm), (cx - arm, cy)], fill=color, width=line_w)
        draw.line([(cx - arm, cy), (cx + arm // 2, cy + arm)], fill=color, width=line_w)
    elif direction == "right":
        draw.line([(cx - arm // 2, cy - arm), (cx + arm, cy)], fill=color, width=line_w)
        draw.line([(cx + arm, cy), (cx - arm // 2, cy + arm)], fill=color, width=line_w)


# ---------------------------------------------------------------------------
# 全PNGをまとめて生成
# ---------------------------------------------------------------------------

def generate_all(tab_position: T.TabPosition) -> dict[str, Image.Image]:
    """1 スキン分の全 PNG を生成して dict で返す。

    キーはファイル名 (拡張子込み)。
    """
    return {
        "window.png": make_window_image(),
        "caption.png": make_caption_image(),
        "tabarea.png": make_tabarea_image(tab_position),
        "buttonarea.png": make_buttonarea_image(),
        "tab.png": make_tab_image(),
        "button.png": make_button_image(),
        "sysbutton.png": make_sysbutton_image(),
        "lockmarker.png": make_lockmarker_image(),
        "menuframe.png": make_menuframe_image(),
        "menuitem.png": make_menuitem_image(),
        "scrollbutton.png": make_scrollbutton_image(),
        "arrowud.png": make_arrowud_image(),
        "arrowlr.png": make_arrowlr_image(),
    }
