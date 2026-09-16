---
name: prelude-release
description: Prelude Vanilla のバージョン更新、リリース前検証、成果物確認、タグ作成、Draft Release 確認を行うときに使用する。通常の編集や単純な検証には使用しない。
---

# Prelude Vanilla Release

リリース準備とリリース実施を、リポジトリの正本に従って進める。

## 正本

作業前に次を順番に読む。

1. `docs/release/branching.md`
2. `docs/release/versioning.md`
3. `docs/release/release-process.md`
4. `.github/workflows/release.yml`

文書と Workflow が異なる場合は、外部操作を止めて差異を報告する。

## 境界

- バージョン形式は `YY.M.N` とし、全アドオンで統一する。
- リリースはアドオン変更を配布する場合だけ行う。
- リポジトリ全体を同じバージョンでリリースする。
- commit、tag、push、GitHub Release の変更や公開は、ユーザーがその外部操作を明示的に依頼した場合だけ行う。
- 依頼された終端がリリース準備までなら、ローカル検証と成果物確認で停止する。

## 手順

1. `git status`、現在のブランチ、対象差分を確認する。
2. アドオン変更の有無と、リリース対象バージョンを確認する。
3. 各 `manifest.json` のバージョンを正本に従って更新し、全アドオンで一致することを確認する。
4. 検証を実行する。

   ```bash
   uv run python tools/validate/validate.py
   ```

5. 全アドオンをビルドする。

   ```bash
   uv run python tools/build/build-all.py --version <version>
   ```

6. `dist/v<version>/build-report.json` をローカルの確認資料として読み、`Successful` が検出したアドオン数と一致し、`Failed` が `0` であることを確認する。
7. 各 `.mcpack` が存在し、ファイル名とバージョンが正しいことを確認する。
8. 明示的に依頼されている場合だけ tag と push を行い、GitHub Actions が作成した Draft Release を確認する。

`build-report.json` は GitHub Release へ添付しない。Draft Release の添付対象は `.mcpack` のみとする。

## 完了報告

確認済み、未確認、実行しなかった外部操作を区別する。検証や Workflow の結果を確認していない場合は、成功したと報告しない。
