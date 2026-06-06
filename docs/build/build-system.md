# Build System

Prelude Vanilla の Build System は、`addons/` 配下の各 Addon を独立した入力として扱い、`dist/` 配下へ配布用の `.mcpack` を生成する仕組みである。

Build Tooling は Python 3.12+ と `uv` を前提とし、`tools/` 配下へ責務ごとに分割して配置する。

---

## Purpose

Build System は次のことを目的とする。

* `addons/` 配下の Addon を自動検出する
* 単一 Addon と全体 Build の両方を扱う
* 配布物を `dist/` 配下へ再現性のある形で出力する
* Validation と Build を段階的な品質ゲートとして統合する
* Generator、Transform、Release 処理を追加しやすい構成を維持する

---

## Input

主な入力は次のとおりである。

* `addons/<addon_name>/`
* リポジトリルートの `LICENSE`
* Build 時に指定する Version

---

## Output

主な出力は次のとおりである。

* `build/workspaces/<addon_name>/`
* `dist/v<version>/<artifact_name>_<version>.mcpack`
* `dist/v<version>/build-report.json`

---

## Tooling

現在の Build Tooling は次の役割に分かれる。

```text
tools/
└─ build/
   ├─ build-addon.py
   ├─ build-all.py
   ├─ detect-changed.py
   ├─ generators/
   └─ transforms/
```

### build-addon.py

単一 Addon を Build する。

入力は Addon 名ではなく、Addon ディレクトリのパスとする。

例:

```bash
uv run python tools/build/build-addon.py addons/Prelude_Vanilla_Main --version 26.6.1
```

### build-all.py

`addons/` 配下を走査し、全 Addon を順番に Build する。

内部的には `build-addon.py` の公開 API を利用する。

### detect-changed.py

Git 差分から変更された Addon パスを検出するための入口とする。

CI や差分 Build と連携する前提で扱う。

### generators

Workspace 内へ生成ファイルを書き出す。

現在は次の Generator を提供する。

* `textures/textures_list.json`
* `contents.json`

`textures/textures_list.json` は Texture 一覧を生成する。

`contents.json` は Minecraft に Contents 情報の生成を要求するための空ファイルを配置する。

Generator の詳細は `generated-files.md` を参照する。

### transforms

Workspace 内の既存ファイルを変換する。

現在は JSON Minify を提供する。

---

## Build Pipeline

単一 Addon の Build Pipeline は次のとおりである。

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
textures/textures_list.json Generate
↓
contents.json Generate
↓
Build Artifact Validation
↓
mcpack Build
↓
Artifact Validation
```

Addon Validation に失敗した場合は Workspace を作成しない。

Build Artifact Validation に失敗した場合は `.mcpack` を生成しない。

Artifact Validation に失敗した場合は Build 失敗扱いとする。

---

## Generated Files

Build Pipeline は次の Generated Files を扱う。

```text
LICENSE
textures/textures_list.json
contents.json
```

`textures/textures_list.json` は Build System が生成する。

`contents.json` は Minecraft に Contents 情報の生成を要求するためのファイルであり、Build System は Contents 一覧を生成しない。

詳細は `generated-files.md` を参照する。

---

## Validation

Build System は Minecraft の仕様検証を行わない。

Validation は Prelude Vanilla の Build / Release 前提を確認するために実行する。

現在の Build 統合は次のとおりである。

* `build-addon.py` は Addon Rule を実行する
* `build-addon.py` は Workspace 上の Build Artifact Rule を実行する
* `build-addon.py` は生成済み `.mcpack` に対する Artifact Rule を実行する
* `build-all.py` は Repository Rule を実行する
* Release Rule は Build Pipeline には統合しない

Validation の詳細は `docs/validation/validation.md` を参照する。

---

## Build Report

全体 Build 成功時は `dist/v<version>/build-report.json` を生成する。

Build Report は次の用途を想定する。

* CI 実行結果の確認
* Release 処理への受け渡し
* Build 成功数と失敗数の集計
* 生成された Artifact 名の確認

Repository Validation に失敗した場合は Build Report を生成しない。

---

## Artifact

Artifact は次の命名規則に従う。

```text
<artifact_name>_<version>.mcpack
```

例:

```text
Prelude_Vanilla_26.6.1.mcpack
Prelude_Vanilla_Clear_Water_26.6.1.mcpack
```

Artifact Name は配布時に使用する名前である。

通常は Addon Name と同一とする。

ただし `Prelude_Vanilla_Main` は例外として、Artifact Name を `Prelude_Vanilla` とする。

Artifact は ZIP として読み取り可能であることを前提とする。

---

## Scope

Build System は既存 Addon を配布可能な形へ整えるための基盤である。

Addon の Minecraft 仕様や Resource Pack の内容を変更するための仕組みではない。
