# Versioning

このドキュメントは Prelude Vanilla のバージョン番号ルールを定義する。

---

# 目的

Prelude Vanilla では、リリース時期が分かりやすく、運用しやすいバージョン番号を採用する。

Semantic Versioning は採用しない。

代わりに、リリース年月とリリース順を表す独自形式を使用する。

---

# バージョン形式

バージョン番号は以下の形式とする。

```text
YY.M.N
```

---

## YY

西暦の下2桁。

例:

```text
26 = 2026
27 = 2027
```

---

## M

リリース月。

範囲:

```text
1 - 12
```

例:

```text
1  = January
6  = June
10 = October
12 = December
```

先頭ゼロは付与しない。

例:

```text
26.1.1
26.6.1
26.10.1
```

---

## N

その月に実施したリリースの通し番号。

例:

```text
26.6.1
26.6.2
26.6.3
```

月が変わると 1 へ戻る。

例:

```text
26.6.10
↓
26.7.1
```

---

# 例

2026年6月のリリース:

```text
26.6.1
26.6.2
26.6.3
```

2026年7月の最初のリリース:

```text
26.7.1
```

2026年10月の最初のリリース:

```text
26.10.1
```

2027年1月の最初のリリース:

```text
27.1.1
```

---

# Git Tag

Git Tag は以下の形式とする。

```text
v<version>
```

例:

```text
v26.6.1
v26.6.2
v26.7.1
```

Release Workflow は Git Tag を起点に実行される。

---

# 成果物

成果物にはバージョン番号を含める。

形式:

```text
<addon_name>_<version>.mcpack
```

例:

```text
Prelude_Vanilla_Main_26.6.1.mcpack
Prelude_Vanilla_Clear_Water_26.6.1.mcpack
```

---

# リリース単位

Prelude Vanilla はリポジトリ単位でリリースする。

すべてのアドオンは同じバージョン番号を共有する。

例:

```text
Prelude_Vanilla_Main_26.6.1.mcpack
Prelude_Vanilla_Clear_Water_26.6.1.mcpack
Prelude_Vanilla_Glowing_Ores_26.6.1.mcpack
```

---

# バージョン比較

バージョン番号は文字列としてではなく、各要素を数値として比較する。

例:

```text
26.6.2
26.6.10
```

文字列比較ではなく、

```text
(26, 6, 2)
(26, 6, 10)
```

として比較する。

---

# 採用しないもの

Prelude Vanilla では以下を採用しない。

* Semantic Versioning
* Major / Minor / Patch
* pre-release
* build metadata

例:

```text
1.2.3
1.2.3-beta
1.2.3+build
```

は使用しない。

---

# 将来の変更

このルールは Prelude Vanilla の運用方針に基づく。

将来的に運用上の問題が発生した場合は見直す可能性があるが、既存のリリース履歴との互換性を考慮して変更する。
