# claunch-skins

CLaunch用のダークスキンをPython/Pillowで生成するプロジェクトです。

> このプロジェクトはほぼ全てAIによって構築されています。

## 生成物

- `dist/Flat Dark.zip`

`dist/`はビルド出力なのでGit管理対象外です。

## コマンド

依存関係の同期:

```powershell
rtk uv sync
```

スキン生成:

```powershell
rtk uv run python -m flat_dark.build
```

プレビュー生成:

```powershell
rtk uv run python -m flat_dark.preview
```

構文確認:

```powershell
rtk uv run python -m compileall src
```

## ディレクトリ

- `src/flat_dark/`: スキン生成コード
- `docs/`: 設計メモ
- `references/`: 参考にした既存スキン・モックアップ・元zip
- `dist/`: 生成されたスキンフォルダとzip

## 現在の主な仕様

- `skin.xml`はUTF-16 LE BOM付きで生成
- PNGはRGBAで生成
- タブ画像は見た目を描かず、`alpha=1`でクリック判定のみ維持
- タブのactive表現は文字色・文字サイズで行う
- フォントは`UD デジタル 教科書体 NK`
