---
name: commit
description: >-
  変更をステージして Conventional Commits 形式でコミットする。ステージング (対象ファイルを 1 つずつ明示指定)、コミットメッセージ生成、type 自動判定、Commit-Model トレイラー付与に使用。「コミットして」「commit」「変更をコミット」「コミットメッセージ」で起動する。push は依頼されない限り行わない。
---

# Commit Skill

## 前提チェック
- コミット対象のファイルが特定できない場合は中断してユーザーに確認
- `.env` など秘密情報を含むファイルが staged にあれば即中断

## ステージング
- ステージは対象ファイルを 1 つずつ明示指定する (`git add <file>`)
- `git add -u` / `git add -A` / `git add .` は使わない
  (コミットし忘れた変更・無関係なファイルを巻き込むため)
- コミット前に `git status --short` で untracked と変更の一覧を確認し、
  コミット対象外の変更・新規ファイルがステージされていないことを確認する

## コミットメッセージの形式

```
<type>: <subject>
```

### type (必須・小文字)
- `build | chore | ci | docs | feat | fix | perf | refactor | revert | style | test` のいずれか
- 判定は `references/type-criteria.md` を参照

## 実行手順
1. `git status --short` と `git diff --staged` を取得
   (ステージングセクションに従い、対象ファイルのみステージ済みであること)
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
- 新規ファイルは `git status --short` で `??` として表示される。
  ステージ時に `??` のファイルがないか確認し、コミット対象なら明示的に add する
  (ステージし忘れると、後から「コミット漏れ」の追補コミットが増える温床になる)
- コミット後に `git status --short` がクリーンであることを確認する
  (untracked や未ステージ変更が残っていたらコミット漏れ)
- 型チェック・テストが失敗した場合はコミットしない (修正してから)
- 複数のtypeに該当する場合は、最も主要なものを選択
- マージコミットにはこのスキルを使用しない
- スクワッシュコミットの場合は、全体の変更内容からtypeを判定
- 初期コミットなど全ファイルが未ステージの場合は中断し、ステージング方針をユーザーに確認する
- `.env` ファイルの検出は文字列一致ではなく、ファイル名パターンで行う
- フッターは件名から空行で区切らないとトレイラーとして解釈されない
- `--author` は使用しない（作者は git config の実在の値に従う）

## 禁止事項
- `--no-verify` の使用
- `git add .` / `git add -A` / `git add -u`
- force push
