# Addon guidance

`addons/*` の各子ディレクトリは、独立して配布可能な Resource Pack として扱う。

## 互換性

- Minecraft が参照するディレクトリ構成、ファイル名、大文字小文字を維持する。
- 他のアドオンへの依存を追加しない。
- 依頼に含まれない画像の一括変換、圧縮、リサイズを行わない。
- アドオンの追加や削除では、名前と UUID が既存アドオンと重複しないことを検証する。

## 生成ファイル

次のファイルはビルド時に生成または配置されるため、配布元のアドオン内へ直接追加・編集しない。

- `contents.json`
- `textures/textures_list.json`
- `LICENSE`

生成規則は `docs/build/generated-files.md` を正本とする。
