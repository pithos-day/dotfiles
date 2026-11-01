# Skillレビュー出力テンプレート

````markdown
# Skillレビュー結果

## 総合判定
- 対象: `{path_or_name}`
- 主カテゴリ: `{category}`
- 判定: `{A|B|C|D}` / `{score}/20`
- 共有可否: `{チーム共有可|改善後に共有|パイロット推奨|再設計推奨}`
- 一言: `{最重要ポイント}`

## 良い点
- `{再利用性・非自明な価値・運用上よい点}`

## 重要指摘
- [Critical|High|Medium|Low] `{指摘}`
  - 根拠: `{ファイル:行、description、構成、スクリプト結果など}`
  - 影響: `{起動漏れ、誤起動、品質低下、安全リスク、運用負荷など}`
  - 改善案: `{具体的な変更}`

## 採点内訳
| 観点 | 点 | コメント |
| --- | ---: | --- |
| Triggerability | `{0-2}` | `{コメント}` |
| Focus | `{0-2}` | `{コメント}` |
| Non-obvious value | `{0-2}` | `{コメント}` |
| Workflow | `{0-2}` | `{コメント}` |
| Gotchas | `{0-2}` | `{コメント}` |
| Progressive disclosure | `{0-2}` | `{コメント}` |
| Deterministic assets | `{0-2}` | `{コメント}` |
| Setup and safety | `{0-2}` | `{コメント}` |
| Team distribution | `{0-2}` | `{コメント}` |
| Measurement and iteration | `{0-2}` | `{コメント}` |

## 改訂description案
```yaml
description: >-
  `{モデルがいつ使うか判断できるdescription案}`
```

## 改善ロードマップ
1. `{今すぐ直す}`
2. `{共有前に直す}`
3. `{運用開始後に計測して改善する}`

## 追加で確認したいこと
- `{ユーザーやSkill所有者への質問}`
````

短縮版を求められた場合は「総合判定」「重要指摘」「改訂description案」「次アクション」の4項目に圧縮する。
