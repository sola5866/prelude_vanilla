# Validation

このドキュメントは Prelude Vanilla の Validation System の設計方針を定義する。

## Purpose

Validation は Minecraft の仕様検証を目的としない。

Validation は以下を目的とする。

* アドオンとして認識できること
* ビルド可能であること
* 配布可能であること
* リポジトリ全体で整合性が保たれていること

Validation はビルド前およびビルド中の品質ゲートとして機能する。

---

# Out of Scope

以下は Minecraft 自体が検証するため、Validation の対象としない。

* JSON 構文
* models の内容
* render_controllers の内容
* animations の内容
* entity の内容
* textures の参照関係
* Resource Pack の Minecraft 仕様
* Bedrock Edition の内部仕様

Validation は Minecraft Validator ではない。

---

# Validation Pipeline

Validation は複数の段階で実行する。

```text
Repository Validation
↓
Addon Validation
↓
Workspace Creation
↓
Build
↓
Build Validation
↓
Artifact Build
↓
Artifact Validation
↓
Build Report
```

Validation に失敗した場合は次の段階へ進まない。

---

# Validation Categories

Validation Rule は以下の分類を持つ。

## Repository Rule

リポジトリ全体を対象とする。

目的:

* リポジトリ構成確認
* アドオン間の整合性確認

---

## Addon Rule

単一アドオンを対象とする。

目的:

* アドオンとして認識できること
* ビルド入力として扱えること

---

## Build Rule

Workspace を対象とする。

目的:

* Build Pipeline が生成した成果物を確認する
* 配布前の Workspace が妥当であることを確認する

---

## Artifact Rule

生成済み Artifact を対象とする。

目的:

* 配布物として成立していることを確認する
* Build 結果と成果物の整合性を確認する

---

## Release Rule

リリース対象を対象とする。

目的:

* リリース前チェック
* 配布成果物の整合性確認

現在は未実装とする。

---

# Validation Context

Validation は ValidationContext を利用して実行する。

想定保持情報:

```python
repo_root: Path
addons_root: Path | None
addon: Addon | None
version: str | None
workspace_path: Path | None
artifact_path: Path | None
```

Validation Rule は ValidationContext から必要な情報を取得する。

---

# Validation Status

Validation 結果は Enum を利用して表現する。

現在の状態:

```text
PASSED
FAILED
```

必要に応じて将来拡張できる。

---

# Validation Result

各 Rule は RuleResult を返す。

保持情報:

* rule_id
* category
* status
* target
* message

---

## Validation Report

Validation 全体の結果は ValidationReport として集約する。

保持情報:

* successful
* failed
* results

ValidationReport は将来的に Build Report と統合できる構造を維持する。

---

# Validation Runner

Validation Runner は Rule の実行のみを担当する。

Runner は Rule の内容を知らない。

```text
Rule
↓
Rule
↓
Rule
↓
ValidationReport
```

新しい検証を追加する場合は Runner を変更しない。

---

# Rule Design

Rule は単一責務とする。

1つの Rule は1つの問題のみを検証する。

---

## Rule ID

すべての Rule は一意な rule_id を持つ。

例:

```text
repository_structure
addon_name_unique
generated_files_exist
artifact_is_zip_readable
```

Build Report やログでは rule_id を利用する。

---

## Rule Message

失敗時は人間が理解しやすいメッセージを返す。

例:

```text
manifest.json not found
```

---

# Implemented Rules

## Repository Rule

### repository_structure

責務:

以下が存在すること。

```text
addons/
docs/
tools/
LICENSE
```

---

### addon_name_unique

責務:

アドオン名が一意であること。

Windows の大小文字差異を考慮する。

---

### addon_uuid_unique

責務:

manifest.json の UUID が重複していないこと。

確認対象:

* header.uuid
* modules[].uuid

---

### license_source_exists

責務:

ビルド時に利用する LICENSE が存在すること。

---

## Addon Rule

### manifest_exists

責務:

manifest.json が存在すること。

---

### addon_recognizable

責務:

tools.shared.addons.is_addon() が True を返すこと。

---

## Build Rule

### generated_files_exist

責務:

Build Pipeline が生成または配置するファイルが存在すること。

確認対象:

```text
LICENSE
contents.json
```

条件付き対象:

```text
textures/textures_list.json
```

---

### generated_files_valid

責務:

生成ファイルの内容が最低限妥当であること。

確認対象:

```text
contents.json
```

期待値:

```json
{}
```

条件付き対象:

```text
textures/textures_list.json
```

---

## Artifact Rule

### artifact_is_zip_readable

責務:

Artifact が ZIP として読み取り可能であること。

---

### artifact_contains_generated_files

責務:

Artifact に必要な生成ファイルが含まれていること。

確認対象:

```text
LICENSE
contents.json
```

条件付き対象:

```text
textures/textures_list.json
```

---

### artifact_name_matches_convention

責務:

Artifact 名が命名規則に従うこと。

例:

```text
Prelude_Vanilla_26.6.1.mcpack
Prelude_Vanilla_Clear_Water_26.6.1.mcpack
```

---

# Rule Addition Policy

新しい Validation を追加する場合は既存 Rule を変更しない。

新しい Rule を追加する。

Validation Runner は変更しない。

ValidationContext と RuleResult を利用して統合する。

---

# Directory Structure

```text
tools/
└─ validate/
   ├─ context.py
   ├─ results.py
   ├─ runner.py
   │
   └─ rules/
      ├─ addon/
      ├─ repository/
      ├─ build/
      └─ release/
```

Rule はカテゴリごとに配置する。

CLI は Validation 基盤とは分離して実装する。

---

# Future Extensions

将来的に以下を追加する可能性がある。

* Release Rule
* release_artifacts_complete
* release_version_consistent
* build_report_present
* changelog_present

Validation と Build は独立した責務を維持する。
