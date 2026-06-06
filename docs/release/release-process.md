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
26.5.1
```

リリース時は全アドオンをビルドし、すべての成果物を同時に公開する。

---

# リリースフロー

```text
Version決定
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

# バージョン番号

バージョン番号はリポジトリ全体で共有する。

例:

```text
26.5.1
```

Git Tag は以下の形式とする。

```text
v26.5.1
```

---

# Git Tag 作成

例:

```bash
git tag v26.5.1
git push origin v26.5.1
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

作成される Draft には以下が添付される。

```text
dist/v<version>/*.mcpack
dist/v<version>/build-report.json
```

例:

```text
Prelude_Vanilla_Main_26.5.1.mcpack
Prelude_Vanilla_Clear_Water_26.5.1.mcpack
build-report.json
```

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

---

# 成果物

成果物は以下の命名規則に従う。

```text
<addon_name>_<version>.mcpack
```

例:

```text
Prelude_Vanilla_Main_26.5.1.mcpack
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
