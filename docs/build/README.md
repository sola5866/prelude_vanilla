# Build

Build に関するドキュメントを配置する。

README は目次として扱い、詳細仕様は個別ドキュメントへ委譲する。

---

## Documents

### build-system.md

Build system 全体の目的、入力と出力、Build pipeline、Build Report を定義する。

### build-transforms.md

Workspace 上で実行する変換処理を定義する。

現在は JSON Minify を扱う。

### generated-files.md

Workspace 上で生成または配置するファイルを定義する。

現在は `contents.json`、`textures_list.json`、`LICENSE` を扱う。

---

## Reading Order

```text
build-system.md
↓
build-transforms.md
↓
generated-files.md
```
