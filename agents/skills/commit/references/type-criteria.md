# Type 判定基準

`@commitlint/config-conventional` の type-enum に準拠する。type は小文字のみ。

## 各typeの定義と例

### feat (新機能追加)
- 新しい機能やAPIの追加
- 例: `feat: add user authentication endpoint`

### fix (バグ修正)
- 既存機能のバグ修正
- 例: `fix: resolve login timeout issue`

### build (ビルド・依存関係)
- ビルドシステムや外部依存関係（npm, pip 等）の変更
- 例: `build: bump typescript to 5.0`

### ci (CI設定)
- CI の設定ファイルやスクリプトの変更
- 例: `ci: cache node_modules in workflow`

### chore (その他)
- 分類不能な雑務（ツール設定、生成物の更新など）
- 例: `chore: update editorconfig`

### docs (ドキュメント)
- ドキュメントの追加や修正
- 例: `docs: update API documentation`

### perf (パフォーマンス改善)
- 挙動を変えずに処理速度やリソース使用量を改善
- 例: `perf: cache directory listing`

### refactor (リファクタリング)
- 挙動変更なしのコード整理
- 例: `refactor: extract validation logic`

### revert (コミット取り消し)
- 以前のコミットの取り消し
- 例: `revert: feat: add user authentication endpoint`

### style (書式)
- 空白・セミコロン・インデントなど、ロジックに影響しない書式修正
- 例: `style: format with prettier`

### test (テスト)
- テストの追加や修正
- 例: `test: add unit tests for auth module`

## 判定の優先順位

1. 新機能追加 → feat
2. バグ修正 → fix
3. パフォーマンス改善 → perf
4. リファクタ → refactor
5. ドキュメント → docs
6. テスト → test
7. ビルド → build
8. CI → ci
9. 書式 → style
10. 取り消し → revert
11. その他 → chore

## 注意点

- 「機能修正（バグではない）」は標準typeに存在しないため、変更内容から feat / fix / refactor / perf のいずれかに分類する
- 複数typeに該当する場合は、最も主要なものを選択
- マージコミットには使用しない
- スクワッシュコミットの場合は、全体の変更内容から判定
