# Generated Files

Prelude Vanilla の Build では、Workspace 上で配布用の補助ファイルを生成または配置する。

Generated Files は `addons/` 配下の元ファイルを変更せず、Workspace にだけ作成する。

---

## Purpose

Generated Files は次のことを目的とする。

* 配布時に必要な補助ファイルを安定して生成する
* 生成処理を Build Pipeline から分離して保守しやすくする
* OS に依存しない再現性のある出力を行う

---

## Files

現在の対象は次の 3 つである。

* `LICENSE`
* `textures/textures_list.json`
* `contents.json`

`LICENSE` はコピーであり、`textures/textures_list.json` と `contents.json` は Generator により生成する。

---

## Generation Order

生成と配置は次の順序で行う。

```text
LICENSE Copy
↓
textures/textures_list.json Generate
↓
contents.json Generate
```

`contents.json` は Minecraft に Contents 情報の生成を要求するためのファイルである。

Build System は Contents 一覧を生成しない。

---

## LICENSE

### Source

```text
<repo_root>/LICENSE
```

### Destination

```text
<workspace>/LICENSE
```

`build-addon.py` はリポジトリルートの `LICENSE` を Workspace へコピーする。

---

## textures/textures_list.json

### Destination

```text
<workspace>/textures/textures_list.json
```

### Public API

```python
generate_textures_list(
    workspace_path: Path,
) -> Path
```

### Purpose

Resource Pack 内で使用する Texture 一覧を定義する。

### Specification

`textures/textures_list.json` は `textures/` 配下の PNG を列挙して生成する。

生成仕様は次のとおりである。

* `textures/**/*.png` を対象とする
* 拡張子 `.png` は含めない
* パス区切りは `/` を使用する
* ソートする
* UTF-8 で書き出す
* JSON のトップレベルは配列とする
* 配列の要素は文字列とする

### Generation Conditions

`textures/` ディレクトリが存在する場合のみ生成する。

```text
textures/
```

が存在しない場合は、

```text
textures/textures_list.json
```

を生成しない。

空配列を書き出すことはしない。

### Example

入力:

```text
textures/entity/enderman/enderman.png
```

出力:

```text
textures/entity/enderman/enderman
```

### Example Output

```json
[
  "textures/entity/enderman/enderman",
  "textures/items/apple"
]
```


---

## contents.json

### Destination

```text
<workspace>/contents.json
```

### Public API

```python
generate_contents(
    workspace_path: Path,
) -> Path
```

### Purpose

Minecraft に Contents 情報の生成を要求する。

Build System は Contents 一覧を生成しない。

Contents 一覧の生成は Minecraft が行う。

### Specification

Build System は次の内容を書き込む。

```json
{}
```

生成仕様は次のとおりである。

* UTF-8 で書き出す
* JSON Object とする
* 空 Object を出力する
* Workspace の内容は走査しない
* Contents 一覧は生成しない

### Responsibility

Build System の責務:

```text
contents.json を配置する
```

Build System の責務ではない:

```text
Contents 一覧を生成する
```

Minecraft は Resource Pack の初回読み込み時に Contents 情報を生成する。

Build System はその生成処理に関与しない。

---

## Build Pipeline

Generated Files は JSON Minify の後、Package Build の前に扱う。

```text
JSON Minify
↓
textures/textures_list.json Generate
↓
contents.json Generate
↓
Build Artifact Validation
↓
mcpack Build
```

Generated Files は Minecraft の仕様検証を行わない。

配布用 Workspace を整える Build Tooling の一部として扱う。
