# Prelude Vanilla Development Skill

このドキュメントは Prelude Vanilla の開発時に実施する検証、ビルド、リリース手順をまとめる。

詳細な仕様は docs 配下を参照する。

---

# Validation

変更後は Validation を実行する。

```bash
uv run python tools/validate/validate.py
```

成功条件:

```text
Failed: 0
```

Validation が失敗した場合は原因を解消してから次へ進む。

---

# Build

全体ビルドを実行する。

```bash
uv run python tools/build/build-all.py \
  --version 99.99.99-test
```

確認項目:

* Successful が期待値と一致する
* Failed が 0
* build-report.json が生成される

生成先:

```text
dist/v99.99.99-test/
```

---

# Artifact Check

生成された mcpack を確認する。

確認項目:

```text
LICENSE
contents.json
textures_list.json
```

Build Validation と Artifact Validation が成功していることを確認する。

---

# Pull Request

開発は feature ブランチで行う。

```text
feature/*
```

完了後は Pull Request を作成し、develop へマージする。

---

# Develop Integration

develop ブランチでは以下を確認する。

```text
Validation
↓
Build
↓
CI
```

問題がなければ main へマージする。

---

# Release

リリースは main ブランチで行う。

バージョン形式:

```text
YY.M.N
```

例:

```text
26.6.1
26.6.2
26.7.1
```

---

## Release Procedure

実運用は次の順序で行う。

### 開発

```text
feature/*
↓
develop
↓
main
```

### リリース対象判定

アドオン変更なしの場合は終了する。

```text
終了
```

アドオン変更ありの場合はリリースを実施する。

```text
リリース実施
```

### Version 確定

manifest.json の version を更新する。

例:

```text
26.6.1
```

### Validation

```bash
uv run python tools/validate/validate.py
```

成功することを確認する。

### Build

```bash
uv run python tools/build/build-all.py --version 26.6.1
```

成功することを確認する。

### Tag 作成

```bash
git tag v26.6.1
git push origin v26.6.1
```

### Draft Release

GitHub Actions により Draft Release が生成される。

確認項目:

```text
Release Title
添付 mcpack
Version
Build Result
```

### Changelog

Draft Release 上で手動記入する。

### Publish

GitHub Release 画面から Publish Release を実行する。

---

## Create Tag

例:

```bash
git checkout main

git pull

git tag v26.6.1

git push origin v26.6.1
```

---

## Release Draft

Tag Push により GitHub Actions が実行される。

```text
Validation
↓
Build
↓
Artifact Validation
↓
Release Draft
```

---

## Publish Release

GitHub Release の Draft を確認する。

確認項目:

* Changelog
* 添付された mcpack
* build-report.json

問題がなければ Publish Release を実行する。

---

# Reference

Build:

```text
docs/build/
```

Validation:

```text
docs/validation/
```

Release:

```text
docs/release/
```
