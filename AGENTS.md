# AGENTS.md

## リポジトリ概要

このリポジトリは Minecraft Bedrock Edition の Resource Pack アドオンを管理するモノレポです。

各アドオンは独立して配布可能な単位です。

## ディレクトリ構成

```text
addons/
├─ Prelude_Vanilla_Main/
├─ Prelude_Vanilla_Better_Entities/
├─ Prelude_Vanilla_Cinematic_Fog/
├─ Prelude_Vanilla_Clear_Staind_Glasses/
├─ Prelude_Vanilla_Clear_Water/
└─ Prelude_Vanilla_Glowing_Ores/
```

### addons

各ディレクトリが1つの配布パックを表します。

Codexは addons 配下のディレクトリを追加・変更対象として扱ってください。

### dist

ビルド成果物の出力先です。

生成物は dist 配下へ出力してください。

### .github/workflows

GitHub Actions の設定です。

ビルド処理を変更する場合は GitHub Actions との整合性を維持してください。

## 設計原則

### アドオンは独立している

各アドオンは単独でビルド・配布可能であること。

他アドオンへの依存を追加しないこと。

### 配布物の互換性を維持する

既存アドオンのフォルダ構成や Minecraft が参照するパスを変更しないこと。

リファクタリング時は配布物の内容が変化しないことを優先する。

### ビルドは自動検出を優先する

アドオン名のハードコーディングは避けること。

以下のような実装を優先する。

```text
addons/*
```

を走査してビルド対象を検出する。

## Codexへの指示

### 変更前に分析する

大規模な変更を行う前に以下を実施すること。

1. 影響範囲の調査
2. 修正対象ファイルの特定
3. 想定リスクの列挙

### 次の場合は確認を求める

* ディレクトリ移動
* 名前変更
* ビルド方式変更
* GitHub Actions の全面的な書き換え
* 既存アドオンへの互換性影響

### 避けること

* 不要なリネーム
* 不要な整形変更
* ファイル内容の一括書き換え
* アドオンの仕様変更

## 完了条件

変更後も以下を満たすこと。

* 全アドオンがビルド可能
* dist に成果物を出力できる
* GitHub Actions が成功する
* 配布物の内容が意図せず変化しない
* 新しいアドオンを addons 配下へ追加できる

## 文字コード

ドキュメントとデータファイルは UTF-8 で統一する。
Markdown と JSON は UTF-8 で読み書きする。
ASCII だけで足りる場面でも、既存の文書やデータが UTF-8 を使っている場合はそれに合わせる。
