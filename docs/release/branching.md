# Branching

このドキュメントは Prelude Vanilla のブランチ運用ルールを定義する。

---

# 目的

開発中の変更とリリース済みの状態を分離し、安全に開発とリリースを行う。

Prelude Vanilla ではシンプルな 3 層構成を採用する。

```text
main
develop
feature/*
```

---

# ブランチ構成

```text
main
└─ develop
   ├─ feature/add-new-addon
   ├─ feature/improve-build-system
   └─ feature/update-textures
```

---

# main

リリース用ブランチ。

常にリリース可能な状態を維持する。

---

## 用途

* リリース済みコードの管理
* Git Tag 作成
* GitHub Release 作成

---

## 原則

`main` へ直接コミットしない。

変更は `develop` 経由で取り込む。

---

## Release

リリースは `main` 上で行う。

例:

```bash
git checkout main

git tag v26.6.1

git push origin main --tags
```

Tag Push により Release Workflow が実行される。

---

# develop

開発統合ブランチ。

複数の feature ブランチを統合し、リリース前の検証を行う。

---

## 用途

* 機能統合
* Validation
* Build テスト
* リリース候補の確認

---

## 原則

新しい開発は `develop` から作成する。

リリース前には十分な確認を行う。

---

## マージ先

```text
feature/*
↓
develop
```

---

```text
develop
↓
main
```

---

# feature/*

機能開発用ブランチ。

新機能、修正、リファクタリングは feature ブランチ上で行う。

---

## 命名規則

形式:

```text
feature/<name>
```

例:

```text
feature/add-build-validation
feature/add-clear-water-addon
feature/improve-release-workflow
feature/update-ore-textures
```

---

## 作成方法

例:

```bash
git checkout develop

git pull

git checkout -b feature/add-build-validation
```

---

## 統合

開発完了後は Pull Request を作成し、`develop` へマージする。

---

# 開発フロー

```text
feature/*
↓
Pull Request
↓
develop
↓
Validation
↓
Build
↓
確認
↓
main
↓
Git Tag
↓
Release
```

---

# GitHub Actions

## build.yml

以下のブランチで実行される。

```text
feature/*
develop
main
```

目的:

```text
Validation
↓
Build
↓
Artifact Validation
```

---

## release.yml

以下で実行される。

```text
Git Tag
```

例:

```text
v26.6.1
```

---

# 禁止事項

以下は行わない。

* main への直接コミット
* main への直接 Push
* feature から main への直接マージ
* feature ブランチ上でのリリース

---

# 将来の拡張

必要になった場合は以下を追加する可能性がある。

* release ブランチ
* hotfix ブランチ
* 自動バージョン管理
* ブランチ保護ルール

ただし現時点では採用しない。
