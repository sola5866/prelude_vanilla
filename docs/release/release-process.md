# Release Process

このドキュメントは Prelude Vanilla のリリース手順を定義する。

---

# 目的

Prelude Vanilla の全アドオンを同一バージョンで配布し、GitHub Release を用いて公開する。

リリースはリポジトリ単位で行う。

個別アドオン単位のリリースは行わない。

---

# 基本方針

すべてのアドオンは同じバージョン番号を共有する。

例:

```text
26.6.1
```

リリース時は全アドオンをビルドし、すべての成果物を同時に公開する。

---

# Release Trigger

main へのマージだけではリリースしない。

リリースは Git Tag の作成によって開始する。

例:

```text
feature/*
↓
develop
↓
main
↓
Git Tag
↓
Release
```

ドキュメント更新や CI/CD 更新のみの場合は、main へマージしてもリリースしない。

アドオンの変更を配布する場合のみ Git Tag を作成する。

---

# リリースフロー

```text
Version確定
↓
manifest.json更新
↓
mainへ反映
↓
Git Tag作成
↓
Git Tag Push
↓
GitHub Actions実行
↓
Validation
↓
Build
↓
Artifact Validation
↓
Release Draft作成
↓
Changelog記入
↓
Publish Release
```

---

# Version Consistency

リリース時は以下のバージョンを一致させる。

```text
manifest.json
Artifact File Name
Git Tag
GitHub Release
```

例:

```text
manifest.json
26.6.1

Artifact
Prelude_Vanilla_26.6.1.mcpack

Git Tag
v26.6.1

Release Title
Prelude Vanilla 26.6.1
```

Git Tag のみ `v` プレフィックスを付与する。

---

# バージョン番号

バージョン番号はリポジトリ全体で共有する。

詳細は `versioning.md` を参照する。

例:

```text
26.6.1
```

Git Tag は以下の形式とする。

```text
v26.6.1
```

---

# Git Tag 作成

例:

```bash
git tag v26.6.1
git push origin v26.6.1
```

Tag を Push すると GitHub Actions の Release Workflow が開始される。

---

# Release Workflow

Release Workflow は以下を自動実行する。

```text
Validation
↓
Build All
↓
Artifact Validation
↓
Release Draft作成
↓
成果物添付
```

---

## 実行内容

Repository Validation を実行する。

Addon Validation を実行する。

Workspace Validation を実行する。

Artifact Validation を実行する。

すべて成功した場合のみ Release Draft を作成する。

---

# Release Draft

Release Workflow は公開済み Release ではなく Draft Release を作成する。

---

## Release Title

Release Title は以下の形式とする。

```text
Prelude Vanilla <version>
```

例:

```text
Prelude Vanilla 26.6.1
Prelude Vanilla 26.6.2
Prelude Vanilla 26.7.1
```

Git Tag の `v` は含めない。

---

## Assets

Draft Release には `.mcpack` 成果物のみを添付する。

例:

```text
Prelude_Vanilla_26.6.1.mcpack
Prelude_Vanilla_Clear_Water_26.6.1.mcpack
Prelude_Vanilla_Glowing_Ores_26.6.1.mcpack
```

`build-report.json` は添付しない。

`build-report.json` は開発用成果物として保持する。

---

# Changelog

Changelog は自動生成しない。

リリース担当者が Draft Release 上で記入する。

例:

```markdown
## Added

-

## Changed

-

## Fixed

-
```

記載内容や形式はリリースごとに調整してよい。

---

# Publish Release

Changelog を確認した後、GitHub の Release 画面から Publish Release を実行する。

公開前に以下を確認する。

* バージョン番号が正しい
* 添付ファイルが正しい
* Changelog が記入されている
* Build Report に問題がない

Build Report は配布しないが、公開前の確認には使用する。

---

# 成果物

成果物は以下の命名規則に従う。

```text
<artifact_name>_<version>.mcpack
```

---

## Artifact Name

Artifact Name は配布時に使用する名前とする。

通常は Addon Name と同一とする。

例:

```text
Addon Name
Prelude_Vanilla_Clear_Water

Artifact Name
Prelude_Vanilla_Clear_Water
```

---

## Prelude_Vanilla_Main

`Prelude_Vanilla_Main` はリポジトリ内の識別名である。

配布時は `Main` を付与しない。

例:

```text
Addon Name
Prelude_Vanilla_Main

Artifact Name
Prelude_Vanilla
```

成果物名:

```text
Prelude_Vanilla_26.6.1.mcpack
```

---

# 将来の拡張

将来的に以下を追加する可能性がある。

* version 更新の自動化
* Release Validation の強化
* リリースメタデータの検証
* GitHub Release 作成処理のツール化
* changelog 補助機能

ただし現時点では、Changelog は手動管理を前提とする。
