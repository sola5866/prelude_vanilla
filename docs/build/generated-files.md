# Generated Files

Prelude Vanilla の Build では、Workspace 上で配布用の補助ファイルを生成または配置する。

Generated Files は `addons/` 配下の元ファイルを変更せず、Workspace にだけ作成する。

---

## Purpose

Generated Files は次のことを目的とする。

* 配布時に必要な補助ファイルを安定して生成する
* 生成処理を Build pipeline から分離して保守しやすくする
* OS に依存しない再現性のある出力を行う

---

## Files

現在の対象は次の 3 つである。

* `LICENSE`
* `textures_list.json`
* `contents.json`

`LICENSE` はコピーであり、`textures_list.json` と `contents.json` は Generator により生成する。

---

## Generation Order

生成と配置は次の順序で行う。

```text
LICENSE Copy
↓
textures_list.json Generate
↓
contents.json Generate
```

`contents.json` は Workspace 配下のファイル一覧から生成するため、`textures_list.json` 生成後に作成する。

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

コピーされた `LICENSE` は `contents.json` に含まれる。

---

## textures_list.json

### Destination

```text
<workspace>/textures_list.json
```

### Public API

```python
generate_textures_list(
    workspace_path: Path,
) -> Path
```

### Specification

`textures_list.json` は `textures/` 配下の PNG を列挙する。

生成仕様は次のとおりである。

* 拡張子は含めない
* パス区切りは `/` を使用する
* ソートする
* `textures/` が存在しない場合は空リストとする
* UTF-8 で書き出す
* JSON のトップレベルは配列とする
* 配列の要素は文字列とする

例:

```text
textures/entity/enderman/enderman.png
```

出力:

```text
textures/entity/enderman/enderman
```

`textures_list.json` は `contents.json` に含まれる。

### Reference

* https://wiki.bedrock.dev/concepts/textures-list

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

### Specification

`contents.json` は Workspace 配下のファイル一覧から生成する。

生成仕様は次のとおりである。

* Workspace 配下のファイル一覧から生成する
* `contents.json` 自身は含めない
* `LICENSE` を含める
* `textures_list.json` を含める
* パス区切りは `/` を使用する
* 再現性のためソートする
* UTF-8 で書き出す
* JSON のトップレベルは配列とする
* 配列の要素は文字列とする
* OS 非依存で扱う

### Reference

* https://wiki.bedrock.dev/concepts/contents

---

## Build Pipeline

Generated Files は JSON Minify の後、Package Build の前に扱う。

```text
JSON Minify
↓
textures_list.json Generate
↓
contents.json Generate
↓
Build Artifact Validation
↓
mcpack Build
```

Generated Files は Minecraft の仕様検証を行わない。

配布用 Workspace を整える Build tooling の一部として扱う。
