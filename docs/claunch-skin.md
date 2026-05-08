# CLaunch スキン仕様メモ

CLaunch (Ver. 4.20+) のスキンを自作するときに必要な情報をまとめたもの。公式ドキュメントは情報が散らばっているので、要点だけ抽出している。

## 1. パッケージ形式

スキンは1つのzipにまとめてCLaunchの`Skins`フォルダに配置する。zipの中身は次の構成。

```text
<SkinName>.zip
├── skin.xml         # マニフェスト
├── window.png       # ウィンドウ枠
├── caption.png      # キャプション領域
├── tabarea.png      # タブ領域背景
├── tab.png          # タブ本体（状態別）
├── buttonarea.png   # ボタン領域背景
├── button.png       # ボタン本体（状態別）
├── sysbutton.png    # システムボタン（Search/Mode/Pin/Close）
├── lockmarker.png   # ロックマーカー
├── menuframe.png    # サブメニュー枠
├── menuitem.png     # サブメニュー項目（状態別）
├── scrollbutton.png # スクロールボタン
├── arrowud.png      # 上下矢印
└── arrowlr.png      # 左右矢印
```

zip直下にファイルを配置する（中間フォルダは作らない）。

## 2. skin.xml

### エンコーディング

- **UTF-16 LE + BOM (`FF FE`) 必須**。UTF-8だとCLaunchが読めない。
- 改行コードは **CRLF** に揃える。
- 宣言行は `<?xml version="1.0" encoding="UTF-16" standalone="yes" ?>`。

### ルート構造

```xml
<skin title="..." author="..." version="...">
  <comment>...</comment>
  <general .../>
  <background .../>
  <frame>...</frame>
  <searchbutton>...</searchbutton>
  <closebutton>...</closebutton>
  <pinbutton>...</pinbutton>
  <modebutton>...</modebutton>
  <caption>...</caption>
  <tabarea>...</tabarea>
  <buttonarea>...</buttonarea>
  <submenu>...</submenu>
  <recommended>...</recommended>
</skin>
```

## 3. PNG 仕様

- **32bpp RGBA** で保存する。
- `<general alphaChannel="true">` の場合、`alpha=0` のピクセルは**クリック判定外**として扱われる（クリックが背景の親ウィンドウに抜ける）。
- 「見た目は透明にしたいがクリックは受けたい」場合、`alpha=1` の極薄ピクセルで埋める。これがないとCLaunchのデフォルト動作（モード切替など）が発動する。
- `clippingColor`（通常`#FF00FF`）は予約色として扱われる。

## 4. 主要要素

### `<general>`

```xml
<general
  tabPosition="top|bottom"
  alphaChannel="true|false"
  clippingColor="#FF00FF"
  sizeArea="6, 6, 6, 6"
  shadowArea="0, 0, 0, 0" />
```

- `sizeArea`: ウィンドウのリサイズ判定マージン（左, 上, 右, 下）。
- `shadowArea`: 影として確保する領域。動的シャドウは描けないので画像に焼き込む前提。

### `<background>`

ウィンドウの中央塗り。`window.png`の中央領域を使う。

```xml
<background image="window.png" left="8" top="44" width="72" height="44"
            method="stretch" border="0, 0, 0, 0">
  <arrangement offset="0, 0, 0, 0" />
</background>
```

### `<frame>`

ウィンドウの4辺。`<top>`, `<left>`, `<right>`, `<bottom>` を持つ。

```xml
<frame>
  <top image="window.png" left="0" top="0" width="1/1" height="44"
       method="stretch" border="12, 0, 12, 0">
    <arrangement height="ImageSize" />
  </top>
  ...
</frame>
```

- `width="1/1"` などの分数表記はソース画像の比率指定。
- `arrangement`の`width="ImageSize"` / `height="ImageSize"`はソース画像のサイズをそのまま使う指定。

### システムボタン (`<searchbutton>` 等)

`Search`, `Close`, `Pin`, `Mode` の4種類。各々 normal/hover/down/downhover の画像領域を指定する。

```xml
<searchbutton>
  <normal     image="sysbutton.png" left="0" top="0"   width="44" height="44" .../>
  <hover      image="sysbutton.png" left="0" top="44"  width="44" height="44" .../>
  <down       image="sysbutton.png" left="0" top="88"  width="44" height="44" .../>
  <downhover  image="sysbutton.png" left="0" top="132" width="44" height="44" .../>
  <arrangement>
    <left   base="TopFrame" side="left"  offset="0" />
    <top    base="TopFrame" side="top"   offset="0" />
    <right  width="ImageSize"  base="TopFrame" side="left" offset="0" />
    <bottom height="ImageSize" base="TopFrame" side="top"  offset="0" />
  </arrangement>
</searchbutton>
```

`<arrangement>`の`base`は配置の基準オブジェクト名。`TopFrame`、`CloseButton`、`PinButton`などを参照できる。

### `<caption>`

タイトル文字を描画する領域。背景画像は通常 1×1 の透明（or alpha=1）でOK。

```xml
<caption image="caption.png" left="0" top="0" width="1/1" height="1/1"
         method="stretch" border="0, 0, 0, 0">
  <arrangement>...</arrangement>
  <text>
    <font face="..." size="9" style="bold" antiAlias="false" />
    <decoration shadow="lower" color="#FFFFFF"
                shadowColor="#000000" shadowAlpha="255" shadowWidth="1" />
  </text>
</caption>
```

### `<tabarea>` / `<tab>`

```xml
<tabarea image="tabarea.png" ...>
  <arrangement offset="0, 0, 0, 0" margin="12, 4, 12, 4" />
  <tab image="tab.png" method="stretch" border="8, 8, 8, 8" designs="1">
    <arrangement pitch="2, 0" />
    <text>
      <font>
        <active   face="..." size="9" style="bold"   antiAlias="false" />
        <inactive face="..." size="9" style="normal" antiAlias="false" />
      </font>
      <decoration>
        <normal shadow="lower" color="#C7C7C7" .../>
        <hover  shadow="lower" color="#FFFFFF" .../>
        <active shadow="lower" color="#FFFFFF" .../>
      </decoration>
    </text>
  </tab>
</tabarea>
```

- `pitch`: タブ間の間隔 (x, y)。
- `designs`: 用意したデザインバリエーション数。

### `<buttonarea>` / `<button>`

```xml
<buttonarea image="buttonarea.png" ...>
  <arrangement offset="0, 0, 0, 0" margin="12, 12, 12, 12" />
  <button image="button.png" method="stretch" border="8, 8, 8, 8" designs="1">
    <arrangement pitch="6, 6" shiftHover="0, 0" shiftDown="0, 1" />
    <text>...</text>
  </button>
  <lockmarker image="lockmarker.png" ...>
    <arrangement zOrder="front" />
  </lockmarker>
</buttonarea>
```

- `shiftHover` / `shiftDown`: hover/down時の位置オフセット。

### `<submenu>`

サブメニュー（フォルダ展開時のポップアップ）。

```xml
<submenu image="menuframe.png" ...>
  <arrangement shadowArea="0, 0, 0, 0" />
  <frame>...</frame>
  <item>
    <normal   image="menuitem.png" .../>
    <selected image="menuitem.png" .../>
    <multisel image="menuitem.png" .../>
    <arrangement margin="4, 4, 4, 4" interval="8" />
    <text>
      <font fontFace="..." fontSize="9" fontStyle="normal" antiAlias="false" />
      <decoration>
        <normal   .../>
        <selected .../>
        <disabled .../>
      </decoration>
    </text>
  </item>
  <scrollbutton>...</scrollbutton>
</submenu>
```

> **注意**: `<item><text><font>` は他と属性名が違う。`face`/`size`/`style` ではなく `fontFace`/`fontSize`/`fontStyle`。

### `<recommended>`

スキン選択直後に「推奨設定を適用」ボタンで反映される推奨値。`<mode1>`（グリッド）と`<mode2>`（リスト）に分かれる。

```xml
<recommended>
  <mode1>
    <caption textMargin="4, 0, 4, 0" centerText="false" multiLine="false" />
    <tab size="56, 20" textMargin="2, 0, 2, 0" fixedWidth="true" multiLine="false" leftText="false" />
    <button size="56, 56" count="7, 3" iconSize="32" iconMargin="0, 4, 0, 0"
            textMargin="0, 1, 0, 1" leftIcon="false" text="true"
            singleLine="false" leftText="false" />
  </mode1>
  <mode2>
    ...
  </mode2>
</recommended>
```

スキンを選んだだけでは反映されない。ユーザーが明示的に「推奨設定を適用」を押す必要がある。

## 5. スプライトの並び方

複数状態を1枚のPNGに縦/横スタックで持たせる。デコードはCLaunchが`top`/`left`/`width`/`height`で切り出す。

| 画像 | 並び |
|---|---|
| `tab.png` | 縦3段: normal / hover / active |
| `button.png` | 縦3段: normal / hover / down |
| `sysbutton.png` | 4列×4段: 列=Search/Mode/Pin/Close, 段=normal/hover/down/downhover |
| `menuitem.png` | 縦3段: normal / selected / multisel |
| `scrollbutton.png` | 縦4段: normal / hover / down / disabled |
| `arrowud.png` | 横2列×縦4段: 列=up/down, 段=normal/hover/down/disabled |
| `arrowlr.png` | 横2列×縦4段: 列=left/right, 段=normal/hover/down/disabled |

## 6. 9-slice (`border` 属性)

`border="left, top, right, bottom"` で各辺の固定領域を指定する。中央のみが`stretch`/`tile`される。`window.png`や`tab.png`、`button.png`の角丸を保ったまま伸縮させたい場合に使う。

## 7. arrangement の基準

`<arrangement>`の`base`属性は配置基準オブジェクト名を指定する。

- `TopFrame`: 上端フレーム
- `BottomFrame`: 下端フレーム
- `LeftFrame`, `RightFrame`: 左右フレーム
- `SearchButton`, `CloseButton`, `PinButton`, `ModeButton`: 各システムボタン

`side="left|right|top|bottom"`で参照辺、`offset="N"`でずらし量、`width|height="ImageSize|Variable|N"`でサイズ指定。

## 8. クリック判定の落とし穴

`alphaChannel="true"`では`alpha=0`のピクセルがクリック判定外（透過）になる。

- **見た目透明 + クリックOK**: `alpha=1` の極薄ピクセルで塗る（実装上は`(0,0,0,1)`など）。
- **見た目透明 + クリック透過**: `alpha=0` のまま。

normal状態のタブやボタン、システムボタンのアイコン外余白は`alpha=1`で埋めておかないと、CLaunchのデフォルト動作（モード切替など）が発動してしまう。

## 9. シャドウ

CLaunchはウィンドウに動的シャドウを描けない。影が欲しい場合は次のどちらかを採る。

- `shadowArea`で領域確保し`window.png`に焼き込む。
- 影なしのフラットデザインで割り切る。

## 10. 参考スキン

`references/skins/`配下の既存スキンが構造の参考になる（リポジトリには含めていないが、各自CLaunchの`Skins`フォルダから入手して展開できる）。

- `Solid Black`: 公式同梱のシンプルな枠タブスキン
- `AclRndDark-ThinTop` / `AclRndDark-ThinBtm`: タブ位置違いのサードパーティスキン
