# Validation

このドキュメントは Prelude Vanilla の Validation システムの設計方針を定義する。

## 目的

Validation は Minecraft の仕様検証を目的としない。

Validation は以下を目的とする。

* アドオンとして認識できること
* ビルド可能であること
* 配布可能であること
* リポジトリ全体で整合性が保たれていること

Validation はビルド前の品質ゲートとして機能する。

---

# 対象外

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

Validation はビルド前に実行する。

```text
Addon Discovery
 ↓
Validation
 ↓
Workspace Creation
 ↓
Build
 ↓
Build Report
```

Validation に失敗した場合はビルドを実行しない。

---

# Validation の分類

Validation Rule は以下の分類を持つ。

## Addon Rule

単一アドオンを対象とする。

目的:

* アドオンとして認識できること
* ビルド入力として扱えること

---

## Repository Rule

リポジトリ全体を対象とする。

目的:

* アドオン間の整合性確認
* リポジトリ構成確認

---

## Release Rule

リリース対象を対象とする。

目的:

* 配布成果物の整合性確認
* リリース前チェック

---

# Validation Context

Validation は ValidationContext を利用して実行する。

想定保持情報:

```python
repo_root: Path
addons_root: Path | None
addon: Addon | None
version: str | None
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

# Rule 設計方針

Rule は単一責務とする。

1つの Rule は1つの問題のみを検証する。

---

## Rule ID

すべての Rule は一意な rule_id を持つ。

例:

```text
manifest_exists
addon_recognizable
repository_structure
addon_name_unique
artifact_name_collision
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

# 現在実装済みの Rule

## Addon Rule

### manifest_exists

対象:

単一アドオン

責務:

manifest.json が存在すること

---

### addon_recognizable

対象:

単一アドオン

責務:

tools.shared.addons.is_addon() が True を返すこと

---

## Repository Rule

### repository_structure

対象:

リポジトリ全体

責務:

以下が存在すること

```text
addons/
docs/
tools/
LICENSE
```

---

### addon_name_unique

対象:

リポジトリ全体

責務:

アドオン名が一意であること

Windows の大小文字差異を考慮する。

例:

```text
Prelude_Vanilla_Main
prelude_vanilla_main
```

は重複とみなす。

---

## Release Rule

### artifact_name_collision

対象:

リリース対象

責務:

生成される成果物名が衝突しないこと

例:

```text
<addon_name>_<version>.mcpack
```

---

# 将来追加予定の Rule

優先度順。

## addon_uuid_unique

manifest.json の UUID が重複していないこと。

確認対象:

* header.uuid
* modules[].uuid

---

## license_source_exists

ビルド時に利用する LICENSE が存在すること。

---

## build_report_writable

Build Report の出力先へ書き込み可能であること。

---

## dist_directory_writable

成果物出力先へ書き込み可能であること。

---

# Rule の追加方針

新しい Validation を追加する場合は既存 Rule を変更しない。

新しい Rule を追加する。

Validation Runner は変更しない。

ValidationContext と RuleResult を利用して統合する。

---

# ディレクトリ構成

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
      └─ release/
```

Rule はカテゴリごとに配置する。

CLI は Validation 基盤とは分離して実装する。

---

# 将来の統合

Validation Report は将来的に Build Report と統合する可能性がある。

例:

```json
{
  "validation": {
    "successful": 5,
    "failed": 0
  },
  "build": {
    "successful": 6,
    "failed": 0
  }
}
```

Validation と Build は独立した責務を維持する。
