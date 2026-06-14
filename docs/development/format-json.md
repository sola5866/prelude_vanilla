# Format JSON

## Purpose

`addons/` 配下の JSON / JSONC ファイルのフォーマットを統一する。

---

## Scope

対象:

```text
addons/**/*.json
```

対象外:

```text
dist/
build/
.venv/
.uv-cache/
```

---

## Formatting Rules

以下の形式で整形する。

```text
UTF-8
indent = 4
ensure_ascii = false
sort_keys = false
末尾改行あり
```

---

## JSONC Support

Resource Pack 内の JSON にはコメントが含まれる場合があるため、Formatter は JSONC を読み取る。

対応するコメント:

```text
// line comment
/* block comment */
```

文字列内の `//` や `/* */` はコメントとして扱わない。

---

## Usage

既定対象:

```bash
uv run python tools/format/format-json.py
```

対象ディレクトリ指定:

```bash
uv run python tools/format/format-json.py addons/Prelude_Vanilla_Main
```

対象ファイル指定:

```bash
uv run python tools/format/format-json.py addons/Prelude_Vanilla_Main/manifest.json
```

チェックのみ:

```bash
uv run python tools/format/format-json.py --check
```

---

## Policy

Build Pipeline からは実行しない。
