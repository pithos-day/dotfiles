---
name: commit
description: ステージ済みの変更をConventional Commits形式でコミットする。git commit、コミットメッセージ生成、type自動判定に使用。
---

# Commit Skill

## 前提チェック
- 未ステージの変更がある場合は中断してユーザーに確認
- `.env` など秘密情報を含むファイルが staged にあれば即中断

## コミットメッセージの形式

```
<type>: <subject>
```

### type (必須・小文字)
- `build | chore | ci | docs | feat | fix | perf | refactor | revert | style | test` のいずれか
- 判定は `references/type-criteria.md` を参照

## 実行手順
1. `git status --short` と `git diff --staged` を取得
2. 差分から type を判定（詳細は `references/type-criteria.md` を参照）
3. コミットメッセージのフッター（トレイラー）にモデル名を追加して `git commit` する
   - フッター形式: `Commit-Model: <現行モデルの表示名>`
   - 例: `Commit-Model: DeepSeek V4 Flash`
   - 例: `Commit-Model: MiMo V2.5`
   - `-m` を2回指定すると git が間に空行を挿入し、2個目がトレイラーになる:
     ```
     git commit -m "fix: resolve login timeout" -m "Commit-Model: DeepSeek V4 Flash"
     ```

## Gotchas
- `git diff --staged` が空の場合、コミットしない
- 複数のtypeに該当する場合は、最も主要なものを選択
- マージコミットにはこのスキルを使用しない
- スクワッシュコミットの場合は、全体の変更内容からtypeを判定
- `.env` ファイルの検出は文字列一致ではなく、ファイル名パターンで行う
- フッターは件名から空行で区切らないとトレイラーとして解釈されない
- `--author` は使用しない（作者は git config の実在の値に従う）

## 禁止事項
- `--no-verify` の使用
- `git add .` / `git add -A`
- force push
