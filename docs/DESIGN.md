# CLaunch スキン設計書 — Flat Dark

ユーザーのモックアップ `references/mockups/claunch-skin-1/claunch-winui-flyout-variants-4-2.html` の **Version C (Mica / 枠なし)** をベースに、Win11 ネイティブのフライアウト風スキンを CLaunch 用に変換するための実装仕様。

---

## 1. 配布物

| スキン名 | タブ位置 | パッケージ |
|---|---|---|
| Flat Dark | 上 | `Flat Dark.zip` |

両者でシステムボタン位置・キャプション領域は同一。タブ位置と関連する余白の左右反転のみが差分。

---

## 2. デザイントークン（pixel ベースに変換済）

### 2.1 カラー (sRGB / プリマルチプライドアルファ)

| トークン | 値 | 用途 |
|---|---|---|
| `surface.mica` | `#202020 @ 88%` | ウィンドウ全体背景（Mica）|
| `surface.mica.tintTop` | `#FFFFFF @ 5.5%` | 上部からの白グラデーション（高位） |
| `surface.mica.tintBot` | `#FFFFFF @ 2.4%` | 下部の白グラデーション（低位） |
| `stroke.window` | `#FFFFFF @ 10.5%` | ウィンドウ外周 1px ボーダー |
| `stroke.highlight` | `#FFFFFF @ 12.5%` | 上端 1px ハイライト |
| `stroke.tabSep` | `#FFFFFF @ 8.5%` | タブとボタン領域のセパレーター線 |
| `accent` | `#4CC2FF` | ホバー時のサブアクセント（Win11 Light Accent）|
| `accent.deep` | `#0078D4` | 必要に応じて (今回未使用) |
| `text.fg` | `#F3F3F3` | 主要テキスト |
| `text.muted` | `#C7C7C7` | タブ非アクティブ |
| `text.subtle` | `#8F8F8F` | 補助テキスト |
| `cell.normal.bg` | `#FFFFFF @ 0%` | ボタン通常時 (枠なしモック準拠で透明) |
| `cell.hover.bg` | `#FFFFFF @ 6.4%` | ボタンホバー時背景 |
| `cell.hover.stroke` | `#FFFFFF @ 7.8%` | ボタンホバー時インセットボーダー |
| `cell.down.bg` | `#FFFFFF @ 4.0%` | ボタン押下時（補間: hoverより薄く・引き締まり）|
| `tab.active.bg` | `#FFFFFF @ 4.0%` | タブアクティブ |
| `tab.hover.bg` | `#FFFFFF @ 3.5%` | タブホバー |
| `closeButton.hover.bg` | `#C42B1C` | 閉じるボタンホバー時赤（Win11 標準）|
| `sysbutton.hover.bg` | `#FFFFFF @ 7.5%` | 閉じる以外のシステムボタンホバー |

### 2.2 角丸

| 対象 | px |
|---|---|
| ウィンドウ外周 | 8 |
| ボタンセル（ホバー時の下地）| 6 |
| タブ | 5 |
| システムボタン下地 | 6 |

### 2.3 シャドウ (ウィンドウ周辺の影)

CLaunchではウィンドウ自体に動的シャドウを描画できないため、`<general shadowArea>` で領域を確保し、画像にそのまま焼き込む。

| パラメータ | 値 |
|---|---|
| 影領域確保 | 右下 12px、上左 0px (`shadowArea="0,0,12,12"`) |
| メインシャドウ | offset y +16 / blur 48 / `#000 @ 44%` |
| サブシャドウ | offset y +2 / blur 8 / `#000 @ 30%` |

※ 影は基本的に画像（window.png）に焼き込み済みとして描画。シャドウ領域でリサイズ判定が外れる仕様を活かす。

### 2.4 タイポグラフィ

CLaunch は OS フォント参照のため、画像には焼き込まない（`<font>` で指定）。

| 用途 | font face | size | weight |
|---|---|---|---|
| キャプション | `Segoe UI Variable`（fallback `Yu Gothic UI`）| 9 | normal |
| タブ | `Segoe UI Variable` | 9 | normal |
| ボタン | `Segoe UI Variable` | 9 | normal |
| サブメニュー | `Segoe UI Variable` | 10 | normal |

`antiAlias="true"` を全箇所で指定。`<decoration>` の `shadow="none"`、`color="#F3F3F3"` で統一。

---

## 3. ウィンドウレイアウト (Mode 1 / 表示モード1)

```
                ┌─────────────────────────────────────────────┐ ← top frame  32px
                │  ⌕  Mode  Pin     CLaunch       ✕            │   キャプション
                ├─────────────────────────────────────────────┤
                │                                              │
                │   ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐            │
                │   │  │ │  │ │  │ │  │ │  │ │  │            │   button area
                │   └──┘ └──┘ └──┘ └──┘ └──┘ └──┘            │   60×60 セル × 6×5
                │     ...                                      │
                │                                              │
                ├─────────────────────────────────────────────┤   セパレーター線
                │  Tab1  Tab2  Tab3  Tab4  [Tab5]              │   tab area 30px
                └─────────────────────────────────────────────┘ ← bottom frame 8px
                  ↘︎ shadow (right/bottom 12px)
```

### 3.1 推奨設定値 (`<recommended>`)

```xml
<recommended>
  <mode1>
    <caption textMargin="0, 0, 0, 0" centerText="true" multiLine="false" />
    <tab size="80, 26" textMargin="0, 0, 0, 0" fixedWidth="false" multiLine="false" leftText="false" />
    <button size="60, 60" count="6, 5" iconSize="32" iconMargin="0, 8, 0, 0"
            textMargin="0, 0, 0, 4" leftIcon="false" text="true" singleLine="true" leftText="false" />
  </mode1>
  <mode2>
    <caption textMargin="0, 0, 0, 0" centerText="true" multiLine="false" />
    <tab size="80, 26" textMargin="0, 0, 0, 0" fixedWidth="false" multiLine="false" leftText="false" />
    <button size="200, 28" count="2, 12" iconSize="16" iconMargin="6, 0, 6, 0"
            textMargin="0, 0, 4, 0" leftIcon="true" text="true" singleLine="true" leftText="true" />
  </mode2>
</recommended>
```

### 3.2 マージン詳細

| 領域 | 上下左右の数値 |
|---|---|
| `<tabarea> <arrangement offset>` | `0, 0, 0, 0` |
| `<tabarea> <arrangement margin>` | `8, 4, 8, 4` |
| `<buttonarea> <arrangement offset>` | `0, 0, 0, 0` |
| `<buttonarea> <arrangement margin>` | `8, 8, 8, 8` |
| ボタン pitch | `4, 4` |
| タブ pitch | `2, 0` |

---

## 4. CLaunchパーツとPNGファイル

ファイル単位で寸法・スプライト構造・9-slice border を定義する。座標系は左上原点 (top-left origin)、x=横、y=縦 (px)。すべて 32bpp PNG (RGBA)。

### 4.1 `window.png` — 80×80

ウィンドウの外枠4辺＋背景＋シャドウを1枚に焼き込む。

```
        x:  0    16        64   80
        ┌────┬────────┬────┐
   y=0  │ ╭──┤        ├──╮ │   top frame 32px
        │ │            │ │  │   8px round corner + 1px stroke + caption mica
        │ │            │ │  │   
   y=32 │ │            │ │  │   left/right edges (1px stroke + mica)
        │ │            │ │  │
   y=64 │ ╰──┤        ├──╯ │   bottom frame 8px
   y=72 │  shadow region    │   shadow 8×8 bake (right+bottom)
   y=80 └────────────────────┘
```

#### スプライト切り出し

| 部位 | XML 参照 | 元画像領域 | 9-slice border | 描画 |
|---|---|---|---|---|
| 上フレーム | `<frame><top>` | x=0, y=0, w=80, h=32 | `border="16, 0, 16, 0"` | stretch、横方向に伸長 |
| 左フレーム | `<frame><left>` | x=0, y=32, w=8, h=32 | `border="0, 0, 0, 0"` | stretch、縦方向に伸長 |
| 右フレーム | `<frame><right>` | x=72, y=32, w=8, h=32 | `border="0, 0, 0, 0"` | stretch、縦方向に伸長 |
| 下フレーム | `<frame><bottom>` | x=0, y=64, w=80, h=16 | `border="16, 0, 16, 0"` | stretch、横方向に伸長 |
| 背景 | `<background>` | x=8, y=32, w=64, h=32 | `border="0, 0, 0, 0"` | stretch (Mica の単色) |

#### 描画レイヤー (上から下)
1. **シャドウ**: 右下方向に 12px 拡張、ガウシアンブラー、`#000 @ 44%` + サブシャドウ `#000 @ 30%`
2. **ストローク**: 8px 角丸の1px外周線、`stroke.window`
3. **ハイライト**: ストロークの内側 1px、上端だけ `stroke.highlight`、左右に gradient 減衰
4. **Mica 面**: `surface.mica` (`#202020 @ 88%`) + 上から `surface.mica.tintTop` → `surface.mica.tintBot` の縦グラデーション

### 4.2 `caption.png` — 1×1 (透明)

CLaunch のキャプション要素は `<background>` の上に重なるが、Mica では追加塗りは不要なため **1×1 完全透明 PNG** を使用してオーバーペイントを抑制。

`<caption>` 自体は省略せずテキスト描画のために宣言。`image` だけ透明な極小画像にしておく（CLaunchはimage指定が前提のため）。

### 4.3 `sysbutton.png` — 144×72

システムボタン（Search / Mode / Pin / Close）のスプライトシート。

#### 横方向（ボタン種別、各 36×36）

| 列 | x範囲 | ボタン |
|---|---|---|
| 0 | 0–36 | Search (虫眼鏡) |
| 1 | 36–72 | Mode (表示モード切替) |
| 2 | 72–108 | Pin (ピン留め) |
| 3 | 108–144 | Close (×) |

#### 縦方向（状態、各 36×36 ※ Pin/Mode/Search は 4 状態 / Close は 3 状態）

統一して 4 段にしておき、Close の最下段（downhover相当）は normal と同じ画像にして実害なし。

| 段 | y範囲 | 状態 |
|---|---|---|
| 0 | 0–36 | normal |
| 1 | 36–72 | hover |
| 2 | — | （未使用、以下は別シートで） |

**※ 上記サイズだと 144×72 になるため、状態数に合わせて拡張する**。最終仕様:

`sysbutton.png` — 144×144 (4列 × 4状態)

| 段 | y範囲 | 状態 |
|---|---|---|
| 0 | 0–36 | normal |
| 1 | 36–72 | hover |
| 2 | 72–108 | down |
| 3 | 108–144 | downhover |

#### XML 参照例 (Search)

```xml
<searchbutton>
  <normal     image="sysbutton.png" left="0"  top="0"   width="36" height="36" />
  <hover      image="sysbutton.png" left="0"  top="36"  width="36" height="36" />
  <down       image="sysbutton.png" left="0"  top="72"  width="36" height="36" />
  <downhover  image="sysbutton.png" left="0"  top="108" width="36" height="36" />
  ...
</searchbutton>
```

#### 各ボタンの描画内容

- **下地** (28×24 角丸6px、状態によって `cell.normal.bg`/`sysbutton.hover.bg`/`cell.down.bg` を切替)
- **アイコン** (中央配置、線幅1.2px、線色 `text.fg`/`text.muted`)
  - Search: 虫眼鏡（円Φ8 + 線）
  - Mode: 横棒2本（モード1=横棒、モード2=ハンバーガー風 ※down状態）
  - Pin: 押しピン（normal=傾斜、down=直立 ※ピン留め時）
  - Close: ×（線2本、normal=`text.fg`、hover時は背景 `closeButton.hover.bg` (#C42B1C) + 線白）

#### `<arrangement>` 配置

モックの並び順 `Search ... brand ... Mode Pin Close` を踏襲:

```xml
<searchbutton>
  <arrangement>
    <left   base="TopFrame" side="left"  offset="8" />
    <top    base="TopFrame" side="top"   offset="0" />
    <right  width="ImageSize"  base="TopFrame" side="left" offset="0" />
    <bottom height="ImageSize" base="TopFrame" side="top"  offset="0" />
  </arrangement>
</searchbutton>

<closebutton>
  <arrangement>
    <left   base="TopFrame" side="right"  offset="-44" />
    <top    base="TopFrame" side="top"    offset="0" />
    <right  width="ImageSize"  base="TopFrame" side="left" offset="0" />
    <bottom height="ImageSize" base="TopFrame" side="top"  offset="0" />
  </arrangement>
</closebutton>

<pinbutton>
  <arrangement>
    <left   base="CloseButton" side="left"  offset="-36" />
    ...
  </arrangement>
</pinbutton>

<modebutton>
  <arrangement>
    <left   base="PinButton"   side="left"  offset="-36" />
    ...
  </arrangement>
</modebutton>
```

### 4.4 `tabarea.png` — 4×4 (1px 上ボーダー線のみ)

タブ領域は本質的に透明（背景は window.png の Mica が透けて見える）。ただし上端1pxにセパレーター線 `stroke.tabSep` を引く。

サイズ最小 4×4 で `border="0,1,0,0"` の 9-slice にすれば、上1pxラインだけが描画される。

### 4.5 `tab.png` — 80×78 (designs=1)

タブのスプライト。状態は normal/hover/active の3段。デザインバリエーション(`designs`属性)は 1。

```
       80
   ┌──────────┐
   │ normal   │ 26px (透明、テキストのみ)
   ├──────────┤
   │ hover    │ 26px (#FFFFFF @ 3.5% 角丸5px)
   ├──────────┤
   │ active   │ 26px (#FFFFFF @ 4.0% 角丸5px)
   └──────────┘
   total: 80 × 78
   border = "8, 8, 8, 8" (角丸保持の9-slice)
```

### 4.6 `buttonarea.png` — 4×4 (完全透明)

ボタン領域は背景を持たない（モックの without-frames 通り）。透明1pxを使用。

### 4.7 `button.png` — 60×180 (designs=1)

ボタンのスプライト。状態 normal/hover/down の3段。

```
       60
   ┌──────────┐
   │ normal   │ 60px (完全透明)
   ├──────────┤
   │ hover    │ 60px (#FFFFFF @ 6.4% bg + #FFFFFF @ 7.8% inset stroke、角丸6px)
   ├──────────┤
   │ down     │ 60px (#FFFFFF @ 4.0% bg、角丸6px、ストロークなし)
   └──────────┘
   border = "8, 8, 8, 8"
```

### 4.8 `lockmarker.png` — 14×14

ボタンロック時にボタンの右上に重なる小さな印。

- 角丸2px の小さな塗り、`accent` (#4CC2FF) で南京錠アイコンか、もしくは シンプルな丸点
- 提案: 8×8 程度のドット形 + 軽い影
- `<arrangement zOrder="front" />` で前面表示

### 4.9 `menuframe.png` — 64×64

サブメニュー（フォルダ展開）の枠。Mica 同様の 8px 角丸。window.png より小さい影とする。

```
レイアウト:
- 上フレーム: 0–16 (16px、角丸 8px + ストローク + Mica)
- 左/右: 16px 幅の単純な縦帯
- 下フレーム: 0–16 (16px、角丸下)
- 中央: Mica 単色

XML割当:
<frame>
  <top    image="menuframe.png" left="0" top="0"  width="1/1" height="16" border="16,0,16,0" />
  <left   image="menuframe.png" left="0" top="24" width="8"   height="16" />
  <right  image="menuframe.png" left="56" top="24" width="8"  height="16" />
  <bottom image="menuframe.png" left="0" top="48" width="1/1" height="16" border="16,0,16,0" />
</frame>
<submenu> 自身: x=8, y=16, w=48, h=32 (中央タイル)
shadowArea="0,0,8,8"
```

### 4.10 `menuitem.png` — 32×96 (3状態)

```
       32
   ┌──────────┐
   │ normal   │ 32px (完全透明)
   ├──────────┤
   │ selected │ 32px (#FFFFFF @ 6.4% + 1pxストローク、角丸4px)
   ├──────────┤
   │ multisel │ 32px (#0078D4 @ 25% + #4CC2FF @ 60% ストローク、角丸4px)
   └──────────┘
   border = "6, 6, 6, 6"
```

### 4.11 `scrollbutton.png` — 16×64 (4状態)

サブメニューのスクロール矢印の下地。基本は半透明の小さな矩形。

```
       16
   ┌──────┐
   │ norm │ 16 (完全透明)
   ├──────┤
   │ hover│ 16 (#FFFFFF @ 6%, 角丸4px)
   ├──────┤
   │ down │ 16 (#FFFFFF @ 4%, 角丸4px)
   ├──────┤
   │ disab│ 16 (完全透明)
   └──────┘
   border = "4, 4, 4, 4"
```

### 4.12 `arrowud.png` — 16×64、`arrowlr.png` — 16×64

矢印（CLaunchでは元サイズ描画、9-sliceなし）。各PNGは縦に上下/左右の2方向 × 4状態を並べる必要がある。

```
arrowud.png 仕様:
   16 × 64 (横2列 × 縦4状態)
   左列(x=0..8): up arrow
   右列(x=8..16): down arrow
   ※ 仕様書では <uparrow><normal image left=1/2 top=1/4 .../></uparrow> のように
     n/分母 表記で領域を指定
   各セル 8×16、矢印図形は各セル中央に4×4のシェブロンで描画

arrowlr.png 仕様:
   16 × 64 (横2列 × 縦4状態)
   左列(x=0..8): left arrow
   右列(x=8..16): right arrow
```

`text.muted` (`#C7C7C7`) を normal/disabled 弱め、`text.fg` を hover/down で。

### 4.13 検索ウィンドウ

CLaunch 4.20 から検索ウィンドウもスキン化対象になっているが、本スキンでは **専用画像を作らず、submenu の枠と項目を流用** する設計とする（`<searchwindow>` はメニューと同じ menuframe.png/menuitem.png を参照）。

---

## 5. ファイル一覧 (1スキン分)

```
Flat Dark/
├── skin.xml          (UTF-16 LE, BOM付き)
├── window.png        80×80
├── caption.png       1×1
├── sysbutton.png     144×144
├── tabarea.png       4×4
├── tab.png           80×78
├── buttonarea.png    4×4
├── button.png        60×180
├── lockmarker.png    14×14
├── menuframe.png     64×64
├── menuitem.png      32×96
├── scrollbutton.png  16×64
├── arrowud.png       16×64
├── arrowlr.png       16×64
└── readme.txt
```

`Flat Dark/` は `skin.xml` の `tabPosition` を `"top"` にする。

---

## 6. タブ位置

現在はTop版のみ生成する。`<general tabPosition>`は`"top"`、セパレーター線は`tabarea.png`の下端に描画する。

---

## 7. 不足部分の補間方針サマリー

| 不足項目 | 補間 |
|---|---|
| ボタン down 状態 | hover より背景を薄く（#FFFFFF @ 4.0%）、ストロークなしで「沈み込み」 |
| システムボタン down/downhover | 押下時は hover よりも 30% 暗いトーン、Pin/Mode の downhover は accent 寄りのティント |
| Close 専用ホバー赤 | `#C42B1C` で Win11 ネイティブ準拠、下段（down）は `#7C1A0E` |
| サブメニュー全体 | window と同じ Mica + 8px 角丸を踏襲、項目は menuitem の3状態 |
| ロックマーカー | accent カラーの小さなドット印 |
| 検索ウィンドウ | submenu リソースを共用 |

---

## 8. レビュー観点（チェックしてほしい箇所）

1. **タブ位置**: Top版のみで問題ないか
2. **Mica の透過度**: `#202020 @ 88%` で実機Win11Micaに近いか、もう少し不透明寄りにしたほうが視認性が良いか
3. **角丸**: ウィンドウ8px / ボタン6px / タブ5px のバランス
4. **システムボタンの並び**: 左端 Search、右端 Close-Pin-Mode の並び（モックは min-pin-close で逆順）でOKか
5. **シャドウ方向**: 右下のみで良いか（Win11 通知では全方向だが、CLaunchの `shadowArea` は左上を縮められないので右下方向にしか焼けない）
6. **`button.png` の hover/down 描画**: ストロークの有無の違いで状態を伝えるという表現で OK か
7. **キャプション中央寄せ**: モックは左端ブランド表示だが、CLaunch のキャプションはアイテム名が入る箇所のため中央寄せにした。OKか
8. **Mode 2 (リスト表示)**: モックには無いが、CLaunch のモード2（リスト形）も推奨設定で200×28に設定。デザインそのままでOKか

---

## 9. 実装プラン（レビュー後）

ルートに既存の uv プロジェクト (`pyproject.toml` / `.python-version=3.13`) を活用する。

### プロジェクト構造

```
claunch-skins/
├── pyproject.toml              # 既存。Pillow を依存に追加
├── .python-version             # 既存 (3.13)
├── .gitignore                  # 新規 (dist/, __pycache__ 等)
├── src/
│   └── flat_dark/
│       ├── tokens.py           # デザイントークン (色・寸法)
│       ├── images.py           # PNG 生成 (Pillow)
│       ├── skin_xml.py         # skin.xml 生成 (UTF-16 LE)
│       └── build.py            # CLI エントリ
├── docs/
│   └── DESIGN.md               # 本書
└── dist/                       # 生成物 (gitignore 対象)
    ├── Flat Dark/
    └── Flat Dark.zip
```

### 実行方法

```pwsh
uv sync                                 # 依存解決
uv run python -m flat_dark.build    # ビルド (全スキン生成)
```

### 既存の `main.py` の扱い

`uv init` 由来の Hello World スクリプトのため削除する。

### 開発ループ

1. `src/flat_dark/tokens.py` のトークン値を編集
2. `uv run python -m flat_dark.build` でビルド
3. `dist/*.zip` を CLaunch の `Skins` フォルダにコピー
4. CLaunch オプションでスキンを選び実機確認
5. 必要に応じて 1 へ戻る
