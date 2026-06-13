# Minecraft Junctions

このドキュメントは、Git 管理中の Addon ディレクトリを Minecraft Bedrock Edition の開発用 Resource Pack ディレクトリから参照する方法を定義する。

---

## Purpose

Minecraft Bedrock Edition は、開発用 Resource Pack を次のディレクトリから読み込む。

```text id="w4rznp"
development_resource_packs
```

Prelude Vanilla では、Git 管理中の `addons/` 配下を Minecraft から直接参照できるようにする。

これにより、Addon の編集結果を `.mcpack` にビルドせずに Minecraft で確認できる。

---

## Scope

この仕組みはローカル開発用である。

Release Build や GitHub Actions では使用しない。

対象:

```text id="w7wgo5"
addons/*
```

対象外:

```text id="d3tuvz"
dist/
build/
.github/workflows/
```

---

## Overview

Git Repository 側の Addon ディレクトリと、Minecraft 側の `development_resource_packs` を Windows の Junction で接続する。

```text id="3tqv5z"
Git Repository
addons/Prelude_Vanilla_Main
        ↓ Junction
Minecraft
development_resource_packs/Prelude_Vanilla_Main
```

Junction は実体ファイルをコピーしない。

Minecraft 側に見えるディレクトリは、Git Repository 側の Addon ディレクトリを参照する。

---

## Environment File

ローカル環境ごとのパスは `.env` で指定する。

`.env` は Git 管理しない。

Git 管理するサンプルとして `.env.example` を用意する。

---

## .env.example

`.env.example` には、個人環境に依存しない抽象的なパスを書く。

```env id="36bm72"
# Minecraft Bedrock Edition の development_resource_packs ディレクトリを指定する。
# 自分の環境に合わせて <UserName> を置き換える。
# パスに半角スペースが含まれる場合に備えて、値はダブルクォートで囲む。
MINECRAFT_RESOURCE_PACKS_DIR="C:\Users\<UserName>\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\development_resource_packs"

# このリポジトリの addons ディレクトリを指定する。
# 自分の環境に合わせて <RepositoryRoot> を置き換える。
# 各アドオンへのジャンクションは、このディレクトリ配下から自動検出して作成する。
PRELUDE_VANILLA_ADDONS_DIR="<RepositoryRoot>\addons"
```

---

## .env

`.env.example` をコピーして `.env` を作成する。

```bash id="u7xvxj"
copy .env.example .env
```

`.env` には実際のローカルパスを書く。

パスに半角スペースが含まれる場合も、値全体をダブルクォートで囲む。

---

## Tool

Junction の作成には次の Tool を使用する。

```text id="doxlbe"
tools/development/link-minecraft-resource-packs.py
```

この Tool は `.env` を読み込み、`PRELUDE_VANILLA_ADDONS_DIR` 配下の Addon を検出する。

Addon は `manifest.json` を持つディレクトリとして扱う。

---

## Create Junctions

実行前に、`.env` が存在することを確認する。

変更内容を確認するだけの場合は `--dry-run` を使う。

```bash id="x1sylc"
uv run python tools/development/link-minecraft-resource-packs.py --dry-run
```

Junction を作成する。

```bash id="77qpjm"
uv run python tools/development/link-minecraft-resource-packs.py
```

---

## Remove Junctions

作成した Junction を削除する場合は `--remove` を使う。

```bash id="f4km7j"
uv run python tools/development/link-minecraft-resource-packs.py --remove
```

削除内容を確認するだけの場合は `--dry-run` を併用する。

```bash id="ru1aib"
uv run python tools/development/link-minecraft-resource-packs.py --remove --dry-run
```

---

## Safety

Tool は既存の同名ディレクトリを上書きしない。

Minecraft 側に同名のディレクトリまたは Junction が存在する場合は、作成をスキップする。

Junction を削除する場合は、Minecraft 側のリンクだけを削除する。

Git Repository 側の Addon ディレクトリは削除しない。

---

## Notes

この仕組みは Windows の Junction を使用する。

Junction 作成には次のコマンドを内部的に使用する。

```bat id="qmjog9"
mklink /J
```

Junction 削除には次のコマンドを使用する。

```bat id="f20tka"
rmdir
```

`del` は使用しない。

---

## Build Pipeline

この Tool は Build Pipeline から実行しない。

Build は引き続き `addons/` を入力として Workspace を作成し、`dist/` に `.mcpack` を出力する。

Junction はローカル開発時に Minecraft で確認しやすくするための補助機能である。
