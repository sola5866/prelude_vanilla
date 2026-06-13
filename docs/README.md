# Docs

Prelude Vanilla の設計資料と運用ドキュメントを管理する。

README は目次として扱い、詳細仕様は各カテゴリの README と個別ドキュメントへ委譲する。

---

## Categories

### build

Build system、Workspace 変換、生成ファイルに関するドキュメントを配置する。

詳細は `docs/build/README.md` を参照する。

### validation

Validation の目的、分類、Rule 設計に関するドキュメントを配置する。

詳細は `docs/validation/README.md` を参照する。

### release

Branch 運用、Version ルール、Release 手順に関するドキュメントを配置する。

詳細は `docs/release/README.md` を参照する。

### development

開発支援ツールと開発時の作業手順に関するドキュメントを配置する。

詳細は `docs/development/README.md` を参照する。

---

## Structure

```text
docs/
├─ README.md
├─ documentation-style.md
├─ build/
├─ development/
├─ validation/
└─ release/
```

---

## Style

ドキュメントの配置、責務、文体、用語は `docs/documentation-style.md` に従う。
