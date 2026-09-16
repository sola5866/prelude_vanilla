# tools

このディレクトリは、Prelude Vanilla の build tooling を整理して配置するための場所です。
ビルド、検証、リリース、共通処理を責務ごとに分離し、将来的にツールが増えても保守しやすい構成にすることを目的とします。

`uv run python ...` を前提とした Python ベースの開発ツールをこの配下に配置しています。

主な構成は次のとおりです。

- `build`: アドオン全体または単体のビルド、変更検出に関するツール
- `validate`: JSON、アドオン単位、リポジトリ構造の検証に関するツール
- `release`: バージョン更新、変更履歴生成、リリース作業に関するツール
- `shared`: 複数ツールから共通利用される定数、ファイル操作、アドオン列挙などの補助モジュール

この構成により、個別スクリプトの寄せ集めではなく、役割が明確な tooling 基盤として段階的に拡張できるようにします。

## 基本コマンド

リポジトリ全体の検証:

```bash
uv run python tools/validate/validate.py
```

全アドオンのビルド:

```bash
uv run python tools/build/build-all.py --version 99.99.99-test
```

詳細な仕様は `docs/validation/`、`docs/build/`、`docs/release/` を参照してください。
