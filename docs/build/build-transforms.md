# JSON Minify

## 目的

配布物に含まれる JSON ファイルのサイズを削減する。

ソースコードの可読性は維持し、成果物のみを最適化する。

---

## Bedrock JSON

Prelude Vanilla では Minecraft Bedrock Edition の慣習に従い、コメント付き JSON (JSONC) を許可する。

ソースツリーには以下のようなファイルが存在してもよい。

例:

```json
{
  // Entity definition
  "format_version": "1.21.0"
}
```

```json
{
  /*
   * Multi-line comment
   */
  "format_version": "1.21.0"
}
```

これらのコメントは開発時の保守性向上を目的とする。

---

## 対象

Workspace 配下の JSON ファイル。

例:

```text
manifest.json

animations/**/*.json

animation_controllers/**/*.json

biomes/**/*.json

entity/**/*.json

fogs/**/*.json

render_controllers/**/*.json

texts/**/*.json
```

---

## 変換方式

Transform は JSONC を入力として扱う。

処理手順:

```text
JSONC
 ↓
コメント除去
 ↓
JSON解析
 ↓
JSON再シリアライズ
```

出力は純粋な JSON とする。

コメントは成果物へ含めない。

---

## コメント除去

以下のコメントを除去対象とする。

```text
// Single-line comment

/* Multi-line comment */
```

---

## 重要

文字列内部の内容は変更しない。

例:

入力:

```json
{
  "url": "https://example.com",
  "description": "Entity // comment"
}
```

出力:

```json
{"url":"https://example.com","description":"Entity // comment"}
```

以下はコメントとして扱わない。

```text
https://example.com

Entity // comment
```

Transform は JSON データの意味を変更してはならない。

---

## JSON 再シリアライズ

コメント除去後の JSON は標準 JSON として再シリアライズする。

出力形式:

```python
json.dumps(
    data,
    ensure_ascii=False,
    separators=(",", ":"),
)
```

---

## 削除されるもの

再シリアライズ時に以下は削除される。

```text
改行

インデント

コロン(:)後の整形用空白

カンマ(,)後の整形用空白

行末空白
```

---

## 保持されるもの

JSON の値として保持される文字列は変更しない。

例:

入力:

```json
{
  "title": "Better Entities",
  "description": "Makes mobs look better"
}
```

出力:

```json
{"title":"Better Entities","description":"Makes mobs look better"}
```

以下は保持される。

```text
Better Entities

Makes mobs look better
```

---

## 除外対象

Transform は除外対象を指定できる設計とする。

除外対象は Workspace ルートからの相対パスで管理する。

例:

```text
contents.json

textures_list.json
```

除外対象に一致したファイルは変更しない。

---

## 実装方針

想定配置:

```text
tools/
└─ build/
   └─ transforms/
      └─ minify_json.py
```

想定 API:

```python
def minify_json_files(
    workspace_path: Path,
    *,
    excluded_paths: set[str] | None = None,
) -> int:
```

戻り値:

```text
変換したファイル数
```

---

## ビルドパイプライン

Transform は Generated Files より先に実行する。

```text
Addon Validation
 ↓
Workspace Creation
 ↓
Addon Copy
 ↓
LICENSE Copy
 ↓
JSON Minify
 ↓
textures_list.json Generate
 ↓
contents.json Generate
 ↓
Package Build
```
