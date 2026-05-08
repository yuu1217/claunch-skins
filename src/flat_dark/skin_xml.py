"""skin.xml を UTF-16 LE (BOM 付き) で生成する。

CLaunch の仕様 (Ver. 4.20) に準拠。文字コードは UTF-16 LE のみサポート。
"""

from __future__ import annotations

from . import tokens as T

XML_DECL = '<?xml version="1.0" encoding="UTF-16" standalone="yes" ?>'

# 文字色などキャプション/タブ/ボタン/メニューのテキスト装飾は共通値
_TEXT_COLOR = T.hex_str(T.TEXT_FG)  # "#F3F3F3"
_TEXT_MUTED_COLOR = T.hex_str(T.TEXT_MUTED)  # "#C7C7C7"

_FONT_FACE_DEFAULT = "Meiryo UI"

_FONT_SIZE_ALL = 9


def render(variant: T.SkinVariant) -> str:
    """variant のメタを差し込んだ skin.xml 文字列を返す (まだバイト化はしない)。"""
    tab_pos = variant.tab_position
    tabarea_offset = "0, 0, 0, 0"
    tabarea_margin = "12, 4, 12, 4"

    # systembutton の並び。Top/Bottom 共通。
    # 左端から Search、右端から Close→Pin→Mode の並び。
    # ImageSize は 44px (sysbutton.png の 1/4)。

    return f"""{XML_DECL}

<!-- CLaunch Skin: {variant.title} -->

<skin title="{variant.title}" author="{variant.author}" version="{variant.version}">

\t<comment>{variant.comment}</comment>

\t<!-- General -->
\t<general tabPosition="{tab_pos}" alphaChannel="true" clippingColor="#FF00FF" sizeArea="6, 6, 6, 6" shadowArea="0, 0, 0, 0" />

\t<!-- Window background (88×96 中央領域) -->
\t<background image="window.png" left="8" top="44" width="72" height="44" method="stretch" border="0, 0, 0, 0">
\t\t<arrangement offset="0, 0, 0, 0" />
\t</background>

\t<!-- Window frames (88×96, TopFrame=44px) -->
\t<frame>
\t\t<top image="window.png" left="0" top="0" width="1/1" height="44" method="stretch" border="12, 0, 12, 0">
\t\t\t<arrangement height="ImageSize" />
\t\t</top>
\t\t<left image="window.png" left="0" top="44" width="8" height="44" method="stretch" border="0, 0, 0, 0">
\t\t\t<arrangement width="ImageSize" />
\t\t</left>
\t\t<right image="window.png" left="80" top="44" width="8" height="44" method="stretch" border="0, 0, 0, 0">
\t\t\t<arrangement width="ImageSize" />
\t\t</right>
\t\t<bottom image="window.png" left="0" top="88" width="1/1" height="8" method="stretch" border="12, 0, 12, 0">
\t\t\t<arrangement height="ImageSize" />
\t\t</bottom>
\t</frame>

\t<!-- Search button (左端、44×44 セル) -->
\t<searchbutton>
\t\t<normal     image="sysbutton.png" left="0" top="0"   width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<hover      image="sysbutton.png" left="0" top="44"  width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<down       image="sysbutton.png" left="0" top="88"  width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<downhover  image="sysbutton.png" left="0" top="132" width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<arrangement>
\t\t\t<left   base="TopFrame" side="left"  offset="0" />
\t\t\t<top    base="TopFrame" side="top"   offset="0" />
\t\t\t<right  width="ImageSize"  base="TopFrame" side="left" offset="0" />
\t\t\t<bottom height="ImageSize" base="TopFrame" side="top"  offset="0" />
\t\t</arrangement>
\t</searchbutton>

\t<!-- Close button (右端) -->
\t<closebutton>
\t\t<normal image="sysbutton.png" left="132" top="0"  width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<hover  image="sysbutton.png" left="132" top="44" width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<down   image="sysbutton.png" left="132" top="88" width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<arrangement>
\t\t\t<left   base="TopFrame" side="right" offset="-44" />
\t\t\t<top    base="TopFrame" side="top"   offset="0" />
\t\t\t<right  width="ImageSize"  base="TopFrame" side="left" offset="0" />
\t\t\t<bottom height="ImageSize" base="TopFrame" side="top"  offset="0" />
\t\t</arrangement>
\t</closebutton>

\t<!-- Pin button (Close の左) -->
\t<pinbutton>
\t\t<normal     image="sysbutton.png" left="88" top="0"   width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<hover      image="sysbutton.png" left="88" top="44"  width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<down       image="sysbutton.png" left="88" top="88"  width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<downhover  image="sysbutton.png" left="88" top="132" width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<arrangement>
\t\t\t<left   base="CloseButton" side="left" offset="-44" />
\t\t\t<top    base="TopFrame"    side="top"  offset="0" />
\t\t\t<right  width="ImageSize"  base="TopFrame" side="left" offset="0" />
\t\t\t<bottom height="ImageSize" base="TopFrame" side="top"  offset="0" />
\t\t</arrangement>
\t</pinbutton>

\t<!-- Mode button (Pin の左) -->
\t<modebutton>
\t\t<normal     image="sysbutton.png" left="44" top="0"   width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<hover      image="sysbutton.png" left="44" top="44"  width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<down       image="sysbutton.png" left="44" top="88"  width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<downhover  image="sysbutton.png" left="44" top="132" width="44" height="44" method="stretch" border="0, 0, 0, 0" />
\t\t<arrangement>
\t\t\t<left   base="PinButton"   side="left" offset="-44" />
\t\t\t<top    base="TopFrame"    side="top"  offset="0" />
\t\t\t<right  width="ImageSize"  base="TopFrame" side="left" offset="0" />
\t\t\t<bottom height="ImageSize" base="TopFrame" side="top"  offset="0" />
\t\t</arrangement>
\t</modebutton>

\t<!-- Caption (1×1 極薄黒、テキストは共通フォント) -->
\t<caption image="caption.png" left="0" top="0" width="1/1" height="1/1" method="stretch" border="0, 0, 0, 0">
\t\t<arrangement>
\t\t\t<left   base="SearchButton" side="right" offset="4" />
\t\t\t<top    base="TopFrame"     side="top"   offset="0" />
\t\t\t<right  width="Variable"  base="ModeButton" side="left" offset="-4" />
\t\t\t<bottom height="Variable" base="TopFrame"   side="bottom" offset="0" />
\t\t</arrangement>
\t\t<text>
\t\t\t<font face="{_FONT_FACE_DEFAULT}" size="{_FONT_SIZE_ALL}" style="bold" antiAlias="false" />
\t\t\t<decoration shadow="lower" color="{_TEXT_COLOR}" shadowColor="#000000" shadowAlpha="255" shadowWidth="1" />
\t\t</text>
\t</caption>

\t<!-- Tab area (1px セパレーター線のみ。タブ本体は文字色だけで状態表示) -->
\t<tabarea image="tabarea.png" left="0" top="0" width="1/1" height="1/1" method="stretch" border="0, 1, 0, 1">
\t\t<arrangement offset="{tabarea_offset}" margin="{tabarea_margin}" />
\t\t<tab image="tab.png" method="stretch" border="8, 8, 8, 8" designs="1">
\t\t\t<arrangement pitch="2, 0" />
\t\t\t<text>
\t\t\t\t<font>
\t\t\t\t\t<active   face="{_FONT_FACE_DEFAULT}" size="{_FONT_SIZE_ALL}" style="bold" antiAlias="false" />
\t\t\t\t\t<inactive face="{_FONT_FACE_DEFAULT}" size="{_FONT_SIZE_ALL}" style="normal" antiAlias="false" />
\t\t\t\t</font>
\t\t\t\t<decoration>
\t\t\t\t\t<normal shadow="lower" color="{_TEXT_MUTED_COLOR}" shadowColor="#000000" shadowAlpha="255" shadowWidth="1" />
\t\t\t\t\t<hover  shadow="lower" color="{_TEXT_COLOR}"       shadowColor="#000000" shadowAlpha="255" shadowWidth="1" />
\t\t\t\t\t<active shadow="lower" color="{_TEXT_COLOR}"       shadowColor="#000000" shadowAlpha="255" shadowWidth="1" />
\t\t\t\t</decoration>
\t\t\t</text>
\t\t</tab>
\t</tabarea>

\t<!-- Button area (透明、大きめのマージン) -->
\t<buttonarea image="buttonarea.png" left="0" top="0" width="1/1" height="1/1" method="stretch" border="0, 0, 0, 0">
\t\t<arrangement offset="0, 0, 0, 0" margin="12, 12, 12, 12" />
\t\t<button image="button.png" method="stretch" border="8, 8, 8, 8" designs="1">
\t\t\t<arrangement pitch="6, 6" shiftHover="0, 0" shiftDown="0, 1" />
\t\t\t<text>
\t\t\t\t<font face="{_FONT_FACE_DEFAULT}" size="{_FONT_SIZE_ALL}" style="normal" antiAlias="false" />
\t\t\t\t<decoration>
\t\t\t\t\t<normal shadow="lower" color="{_TEXT_COLOR}" shadowColor="#000000" shadowAlpha="255" shadowWidth="1" />
\t\t\t\t\t<hover  shadow="lower" color="{_TEXT_COLOR}" shadowColor="#000000" shadowAlpha="255" shadowWidth="1" />
\t\t\t\t\t<down   shadow="lower" color="{_TEXT_COLOR}" shadowColor="#000000" shadowAlpha="255" shadowWidth="1" />
\t\t\t\t</decoration>
\t\t\t</text>
\t\t</button>
\t\t<lockmarker image="lockmarker.png" left="0" top="0" width="1/1" height="1/1" method="stretch" border="0, 0, 0, 0">
\t\t\t<arrangement zOrder="front" />
\t\t</lockmarker>
\t</buttonarea>

\t<!-- Submenus (56×56 フラット、シャドウなし) -->
\t<submenu image="menuframe.png" left="8" top="16" width="40" height="24" method="tile" border="0, 0, 0, 0">
\t\t<arrangement shadowArea="0, 0, 0, 0" />
\t\t<frame>
\t\t\t<top image="menuframe.png" left="0" top="0" width="1/1" height="16" method="stretch" border="16, 0, 16, 0">
\t\t\t\t<arrangement height="ImageSize" />
\t\t\t</top>
\t\t\t<left image="menuframe.png" left="0" top="16" width="8" height="24" method="stretch" border="0, 0, 0, 0">
\t\t\t\t<arrangement width="ImageSize" />
\t\t\t</left>
\t\t\t<right image="menuframe.png" left="48" top="16" width="8" height="24" method="stretch" border="0, 0, 0, 0">
\t\t\t\t<arrangement width="ImageSize" />
\t\t\t</right>
\t\t\t<bottom image="menuframe.png" left="0" top="40" width="1/1" height="16" method="stretch" border="16, 0, 16, 0">
\t\t\t\t<arrangement height="ImageSize" />
\t\t\t</bottom>
\t\t</frame>
\t\t<item>
\t\t\t<normal   image="menuitem.png" left="0" top="0"  width="1/1" height="1/3" method="stretch" border="8, 8, 8, 8" />
\t\t\t<selected image="menuitem.png" left="0" top="36" width="1/1" height="1/3" method="stretch" border="8, 8, 8, 8" />
\t\t\t<multisel image="menuitem.png" left="0" top="72" width="1/1" height="1/3" method="stretch" border="8, 8, 8, 8" />
\t\t\t<arrangement margin="4, 4, 4, 4" interval="8" />
\t\t\t<text>
\t\t\t\t<font fontFace="{_FONT_FACE_DEFAULT}" fontSize="{_FONT_SIZE_ALL}" fontStyle="normal" antiAlias="false" />
\t\t\t\t<decoration>
\t\t\t\t\t<normal   shadow="lower" color="{_TEXT_COLOR}"       shadowColor="#000000" shadowAlpha="255" shadowWidth="1" />
\t\t\t\t\t<selected shadow="lower" color="{_TEXT_COLOR}"       shadowColor="#000000" shadowAlpha="255" shadowWidth="1" />
\t\t\t\t\t<disabled shadow="lower" color="{_TEXT_MUTED_COLOR}" shadowColor="#000000" shadowAlpha="255" shadowWidth="1" />
\t\t\t\t</decoration>
\t\t\t</text>
\t\t</item>
\t\t<scrollbutton>
\t\t\t<normal   image="scrollbutton.png" left="0" top="0"  width="1/1" height="1/4" method="stretch" border="4, 4, 4, 4" />
\t\t\t<hover    image="scrollbutton.png" left="0" top="16" width="1/1" height="1/4" method="stretch" border="4, 4, 4, 4" />
\t\t\t<down     image="scrollbutton.png" left="0" top="32" width="1/1" height="1/4" method="stretch" border="4, 4, 4, 4" />
\t\t\t<disabled image="scrollbutton.png" left="0" top="48" width="1/1" height="1/4" method="stretch" border="4, 4, 4, 4" />
\t\t\t<arrangement interval="2" width="14" height="14" />
\t\t\t<uparrow>
\t\t\t\t<normal   image="arrowud.png" left="0" top="0"  width="1/2" height="1/4" />
\t\t\t\t<hover    image="arrowud.png" left="0" top="16" width="1/2" height="1/4" />
\t\t\t\t<down     image="arrowud.png" left="0" top="32" width="1/2" height="1/4" />
\t\t\t\t<disabled image="arrowud.png" left="0" top="48" width="1/2" height="1/4" />
\t\t\t</uparrow>
\t\t\t<downarrow>
\t\t\t\t<normal   image="arrowud.png" left="8" top="0"  width="1/2" height="1/4" />
\t\t\t\t<hover    image="arrowud.png" left="8" top="16" width="1/2" height="1/4" />
\t\t\t\t<down     image="arrowud.png" left="8" top="32" width="1/2" height="1/4" />
\t\t\t\t<disabled image="arrowud.png" left="8" top="48" width="1/2" height="1/4" />
\t\t\t</downarrow>
\t\t\t<leftarrow>
\t\t\t\t<normal   image="arrowlr.png" left="0" top="0"  width="1/2" height="1/4" />
\t\t\t\t<hover    image="arrowlr.png" left="0" top="16" width="1/2" height="1/4" />
\t\t\t\t<down     image="arrowlr.png" left="0" top="32" width="1/2" height="1/4" />
\t\t\t\t<disabled image="arrowlr.png" left="0" top="48" width="1/2" height="1/4" />
\t\t\t</leftarrow>
\t\t\t<rightarrow>
\t\t\t\t<normal   image="arrowlr.png" left="8" top="0"  width="1/2" height="1/4" />
\t\t\t\t<hover    image="arrowlr.png" left="8" top="16" width="1/2" height="1/4" />
\t\t\t\t<down     image="arrowlr.png" left="8" top="32" width="1/2" height="1/4" />
\t\t\t\t<disabled image="arrowlr.png" left="8" top="48" width="1/2" height="1/4" />
\t\t\t</rightarrow>
\t\t</scrollbutton>
\t</submenu>

\t<!-- Recommended settings -->
\t<recommended>
\t\t<mode1>
\t\t\t<caption textMargin="4, 0, 4, 0" centerText="false" multiLine="false" />
\t\t\t<tab size="56, 20" textMargin="2, 0, 2, 0" fixedWidth="true" multiLine="false" leftText="false" />
\t\t\t<button size="56, 56" count="7, 3" iconSize="32" iconMargin="0, 4, 0, 0" textMargin="0, 1, 0, 1" leftIcon="false" text="true" singleLine="false" leftText="false" />
\t\t</mode1>
\t\t<mode2>
\t\t\t<caption textMargin="4, 0, 4, 0" centerText="false" multiLine="false" />
\t\t\t<tab size="56, 20" textMargin="2, 0, 2, 0" fixedWidth="true" multiLine="false" leftText="false" />
\t\t\t<button size="160, 24" count="2, 10" iconSize="16" iconMargin="6, 2, 6, 2" textMargin="0, 0, 2, 0" leftIcon="true" text="true" singleLine="true" leftText="true" />
\t\t</mode2>
\t</recommended>

</skin>
"""


def to_bytes(xml_text: str) -> bytes:
    """UTF-16 LE (BOM 付き) のバイト列にエンコード。

    CLaunch 仕様で UTF-16 LE のみサポート。Python 標準の "utf-16" は
    プラットフォームによって BE になる場合があるため "utf-16-le" + BOM を明示。
    また改行コードは CRLF に揃える。
    """
    # 改行を CRLF に正規化
    xml_text = xml_text.replace("\r\n", "\n").replace("\n", "\r\n")
    bom = b"\xff\xfe"
    return bom + xml_text.encode("utf-16-le")
