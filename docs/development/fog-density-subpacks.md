# Fog Density Subpacks

このドキュメントは、`Prelude_Vanilla_Main` の fog JSON を元にして `Prelude_Vanilla_Cinematic_Fog` の fog JSON を生成する方法をまとめる。

---

## 目的

Cinematic Fog では、subpack ごとに `air.max_density` を変えた fog JSON を配置する。

Main Addon 側の fog JSON を元にすることで、fog の色、距離、`media_coefficients` などの設定を保ったまま、密度だけを段階的に変更できるようにする。

---

## 入力

入力は `Prelude_Vanilla_Main/fogs/` 配下の fog JSON ファイルとする。

対象ファイルは次の 3 つとする。

* `default_fog_setting.json`
* `pale_garden_fog_setting.json`
* `sulfur_cave_fog_setting.json`

---

## 出力先

出力先は次の 2 系統とする。

```text
addons/Prelude_Vanilla_Cinematic_Fog/fogs/
addons/Prelude_Vanilla_Cinematic_Fog/subpacks/<name>/fogs/
```

---

## 書き込み先

各 JSON の次の値を書き換える。

```text
minecraft:fog_settings > volumetric > density > air > max_density
```

---

## 基準値

`fogs/` に配置するファイルと `subpacks/10` の値は基準値とする。

```text
default_fog_setting.json: 0.005000
pale_garden_fog_setting.json: 0.010000
sulfur_cave_fog_setting.json: 0.010000
```

---

## Subpack 構成

`subpacks` 配下には次のフォルダを配置する。

```text
subpacks/
├─ 0/
├─ 1/
├─ ...
├─ 20/
└─ default/
```

各フォルダの下には `fogs/` を作成し、対象ファイルを配置する。

```text
subpacks/0/fogs/default_fog_setting.json
subpacks/0/fogs/pale_garden_fog_setting.json
subpacks/0/fogs/sulfur_cave_fog_setting.json
```

---

## 密度計算

番号 `10` を基準とする。

* `0` は基準値の 10 分の 1 とする。
* `10` は基準値とする。
* `20` は基準値の 10 倍とする。
* `default` は `15` と同じ値とする。

番号 `n` の値は次の式で計算する。

```text
value = base_value * 10 ^ ((n - 10) / 10)
```

書き込む値は小数点以下 6 桁に四捨五入する。

---

## 代表値

`default_fog_setting.json` の代表値は次のとおりとする。

```text
subpacks/0: 0.000500
subpacks/10: 0.005000
subpacks/15: 0.015811
subpacks/20: 0.050000
subpacks/default: 0.015811
```

`pale_garden_fog_setting.json` と `sulfur_cave_fog_setting.json` の代表値は次のとおりとする。

```text
subpacks/0: 0.001000
subpacks/10: 0.010000
subpacks/15: 0.031623
subpacks/20: 0.100000
subpacks/default: 0.031623
```

---

## CLI

生成ツールは `tools/development/generate-fog-density-subpacks.py` とする。

例:

```bash
uv run python tools/development/generate-fog-density-subpacks.py \
  addons/Prelude_Vanilla_Main/fogs/default_fog_setting.json \
  --mode both
```

`--mode` は次から選ぶ。

* `fogs`
* `subpacks`
* `both`

`--mode fogs` は `Prelude_Vanilla_Cinematic_Fog/fogs/` に同名の JSON を生成する。

`--mode subpacks` は `Prelude_Vanilla_Cinematic_Fog/subpacks/<name>/fogs/` に `0` から `20` と `default` の JSON を生成する。

`--mode both` は両方を生成する。

---

## 文字コード

読み書きは UTF-8 とする。

---

## 補足

このドキュメントは、fog の値の考え方と CLI の使い方を一つにまとめる。
