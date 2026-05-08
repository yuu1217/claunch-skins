"""スキン生成に使う色・寸法・バリアント定義。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# ---------------------------------------------------------------------------
# 型エイリアス
# ---------------------------------------------------------------------------

RGBA = tuple[int, int, int, int]
"""(r, g, b, a) all in 0-255。Pillow と互換。"""


# ---------------------------------------------------------------------------
# 色ヘルパー
# ---------------------------------------------------------------------------

def hexa(hex_str: str, alpha: float = 1.0) -> RGBA:
    """`#RRGGBB` と alpha (0.0-1.0) から RGBA を生成。"""
    h = hex_str.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"expected #RRGGBB, got {hex_str!r}")
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return (r, g, b, max(0, min(255, round(alpha * 255))))


def hex_str(color: RGBA) -> str:
    """skin.xml で使う #RRGGBB 表記へ変換 (alpha は捨てる)。"""
    r, g, b, _ = color
    return f"#{r:02X}{g:02X}{b:02X}"


# ---------------------------------------------------------------------------
# カラーパレット
# ---------------------------------------------------------------------------

# 完全透明色。クリック判定が必要な領域には使わない。
TRANSPARENT: RGBA = (0, 0, 0, 0)

# 表面 (完成不透明)
SURFACE_MICA: RGBA = hexa("#202020", 1.0)

# 線 (すべて完全 opaque + プリブレンド済みの色。透過を一切使わない)
# #202020 の上に重ねることを前提としたグレー値
STROKE_WINDOW: RGBA = (56, 56, 56, 255)      # 外周ボーダー
STROKE_HIGHLIGHT: RGBA = (72, 72, 72, 255)    # 上端ハイライト
STROKE_TAB_SEP: RGBA = (50, 50, 50, 255)      # タブセパレーター

# アクセント
ACCENT: RGBA = hexa("#4CC2FF", 1.0)
ACCENT_DEEP: RGBA = hexa("#0078D4", 1.0)

# テキスト
TEXT_FG: RGBA = hexa("#F3F3F3", 1.0)
TEXT_MUTED: RGBA = hexa("#C7C7C7", 1.0)
TEXT_SUBTLE: RGBA = hexa("#8F8F8F", 1.0)

# セル状態
CELL_HOVER_BG: RGBA = hexa("#FFFFFF", 0.064)
CELL_HOVER_STROKE: RGBA = hexa("#FFFFFF", 0.078)
CELL_DOWN_BG: RGBA = hexa("#FFFFFF", 0.040)

# システムボタン
SYSBTN_HOVER_BG: RGBA = hexa("#FFFFFF", 0.075)
SYSBTN_DOWN_BG: RGBA = hexa("#FFFFFF", 0.040)
CLOSE_HOVER_BG: RGBA = hexa("#C42B1C", 1.0)
CLOSE_DOWN_BG: RGBA = hexa("#7C1A0E", 1.0)

# ---------------------------------------------------------------------------
# 寸法
# ---------------------------------------------------------------------------

# 角丸
RADIUS_WINDOW = 8
RADIUS_BUTTON = 8
RADIUS_SYSBTN = 6
RADIUS_MENU = 8
RADIUS_MENUITEM = 6

# ウィンドウフレーム
# TopFrame を大きく取り、システムボタンとのマージンを確保
WINDOW_PNG_W = 88
WINDOW_PNG_H = 96
TOP_FRAME_H = 44  # キャプション + システムボタン領域 (大きめ)
BOT_FRAME_H = 8
LEFT_FRAME_W = 8
RIGHT_FRAME_W = 8

# システムボタン (TopFrame 高さと一致 = 44px)
SYSBTN_CELL = 44
SYSBTN_INNER = 36  # 中央に置く角丸下地の幅
SYSBTN_INNER_H = 30  # 高さ
SYSBTN_PNG_W = SYSBTN_CELL * 4  # 4ボタン × 44 = 176
SYSBTN_PNG_H = SYSBTN_CELL * 4  # 4状態 × 44 = 176

# タブ (推奨設定の rendered 値とソース画像を一致 → ストレッチ劣化なし)
TAB_W = 140
TAB_H = 38
TAB_PNG_W = TAB_W
TAB_PNG_H = TAB_H * 3  # normal/hover/active

# ボタン (推奨設定の rendered 値とソース画像を一致)
BUTTON_W = 100
BUTTON_H = 100
BUTTON_PNG_W = BUTTON_W
BUTTON_PNG_H = BUTTON_H * 3  # normal/hover/down

# サブメニュー
MENU_PNG_W = 56
MENU_PNG_H = 56

# メニュー項目 (大きめ)
MENUITEM_W = 48
MENUITEM_H = 36
MENUITEM_PNG_W = MENUITEM_W
MENUITEM_PNG_H = MENUITEM_H * 3  # normal/selected/multisel

# スクロールボタン
SCROLLBTN_W = 16
SCROLLBTN_H = 16
SCROLLBTN_PNG_W = SCROLLBTN_W
SCROLLBTN_PNG_H = SCROLLBTN_H * 4  # normal/hover/down/disabled

# 矢印 (上下 / 左右、各 2 方向 × 4 状態)
ARROW_CELL_W = 8
ARROW_CELL_H = 16
ARROW_PNG_W = ARROW_CELL_W * 2  # 2 方向
ARROW_PNG_H = ARROW_CELL_H * 4  # 4 状態

# ロックマーカー
LOCKMARKER_W = 14
LOCKMARKER_H = 14

# キャプション (実態は1×1極薄黒)
CAPTION_W = 1
CAPTION_H = 1

# ボタンエリア / タブエリア (4×4透明、ただしタブエリアは上 or 下に1pxセパレーター線)
AREA_W = 4
AREA_H = 4


# ---------------------------------------------------------------------------
# スキンバリアント
# ---------------------------------------------------------------------------

TabPosition = Literal["top", "bottom"]


@dataclass(frozen=True)
class SkinVariant:
    """1スキン分のメタデータ。"""

    name: str
    """フォルダ名・zip名。"""

    title: str
    """skin.xml の title 属性。"""

    tab_position: TabPosition

    author: str = "Yuu"
    version: str = "1"

    @property
    def comment(self) -> str:
        return "Flat dark color CLaunch skin."


VARIANTS: list[SkinVariant] = [
    SkinVariant(
        name="Flat Dark",
        title="Flat Dark",
        tab_position="top",
    ),
]
