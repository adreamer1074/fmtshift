# fmtshift - Format Shift Tool

ファイル形式を相互に変換できるCLIツールです。

## サポートタイプ: xlsx,md

- 複数シート対応: Excelの複数シートをMarkdownの見出しで区別
- 列幅の自動調整、空行のスキップ
- CLI対応
- 日本語対応




## 📦 インストール

```bash

git clone https://github.com/adreamer1074/fmtshift.git
cd fmtshift
pip install -r requirements.txt
```

### fmtshiftをグローバルコマンドとしてインストール（オプション1）

```bash
pip install -e .
```

### またはPATH追加に追加（オプション２）
※オプション１つい使わない場合）
```powershell
$env:PATH += ";C:\Users\you\path\to\fmtshift"
```

これで`fmtshift`コマンドがどこからでも使えるようになります！

## 使い方

### 基本コマンド

```bash
# Markdown → Excel
fmtshift -f input.md -t output.xlsx

# Excel → Markdown
fmtshift -f input.xlsx -t output.md
```

### オプション

| オプション | 説明 | 必須 |
|-----------|------|------|
| `-f`, `--from` | 変換元ファイルパス | 〇 |
| `-t`, `--to` | 変換先ファイルパス | 〇 |
| `-v`, `--version` | バージョン表示 | |
| `-h`, `--help` | ヘルプ表示 | |

### 使用例

```bash
# 例1: サンプルファイルで試す
fmtshift -f sample_full.md -t sample_full.xlsx

# 例2: Excelファイルをドキュメント化
fmtshift -f data.xlsx -t documentation.md

# 例3: 別のディレクトリのファイル
fmtshift -f path\to\report.md -t path\to\report.xlsx

# 例4: バージョン確認
fmtshift --version
```

## 📝 Markdownフォーマット

### 推奨フォーマット

```markdown
# ドキュメントタイトル（オプション）

このドキュメントの説明...

## シート1

説明文やリスト：
- 項目1
- 項目2

| 列1 | 列2 | 列3 |
| --- | --- | --- |
| データ1 | データ2 | データ3 |

## シート2

別のシートの内容...
```

### サポートする要素

| 要素 | Markdown | Excel変換 |
|------|----------|-----------|
| **タイトル** | `# テキスト` | 太字、サイズ14 |
| **シート** | `## シート名` | 新しいExcelシート |
| **テキスト** | 通常の段落 | セルに配置 |
| **リスト** | `- 項目` | 箇条書き（•） |
| **番号リスト** | `1. 項目` | 番号付きリスト |
| **テーブル** | `\| 列 \|` | Excelテーブル |
| **コード** | ` ```言語` | Courier Newフォント |


### ファイル構成

```
fmtshift/
├── fmtshift.py              # CLIエントリーポイント
├── converters/              # 変換ロジック
│   ├── base.py             # 中間データ構造
│   └── converter.py        # 変換コーディネーター
├── parsers/                # パーサー（読み込み）
│   ├── excel_parser.py
│   └── markdown_parser.py
└── writers/                # ライター（書き込み）
    ├── excel_writer.py
    └── markdown_writer.py
```

## アンインストール

```bash 
pip uninstall fmtshift -y
```
## バージョン
- 0.2
