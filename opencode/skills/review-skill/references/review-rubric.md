# Skillレビュー基準

記事「[Lessons from building Claude Code: How we use skills](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills)」の実践知を、チーム運用向けのレビュー観点に整理した基準。

## 1. まず主カテゴリを1つ選ぶ

優れたSkillは主目的が明確で、次のカテゴリのどれかに自然に収まる。

1. **Library and API reference**: ライブラリ、CLI、SDK、内部APIの正しい使い方と落とし穴。
2. **Product verification**: UI、CLI、業務フロー、状態遷移を検証する手順やドライバ。元記事では、最も測定可能な品質改善効果があった領域とされており、投資価値が高い。
3. **Data fetching and analysis**: データ基盤、監視、ログ、ダッシュボード、分析手順。
4. **Business process and team automation**: チケット、日報、週報、連絡、定型業務の自動化。
5. **Code scaffolding and templates**: コード生成、テンプレート、ボイラープレート、マイグレーション。
6. **Code quality and review**: レビュー、品質基準、テスト方針、スタイル、静的検査。
7. **CI/CD and deployment**: PR監視、リリース、デプロイ、ロールバック、cherry-pick。
8. **Runbooks**: 障害、アラート、エラー症状から調査レポートへ進む手順。
9. **Infrastructure operations**: 保守、クリーンアップ、依存関係管理、コスト調査などの運用。

複数カテゴリにまたがる場合は、混乱の兆候として扱う。ただし、明確な主カテゴリと補助的な参照関係がある場合は許容する。

## 2. 採点観点

各観点を 0〜2 点で採点する。最大20点。

| 観点 | 0点 | 1点 | 2点 |
| --- | --- | --- | --- |
| Triggerability | descriptionが要約で、起動条件が不明 | 一部トリガーはあるが曖昧 | 入力、成果物、トリガー語、使わないケースが明確 |
| Focus | 目的が広すぎる | 主目的はあるが隣接領域が混在 | 1カテゴリに収まり、境界が明確 |
| Non-obvious value | 一般論だけ | 一部固有知識がある | Claudeが通常知らない制約、手順、判断基準がある |
| Workflow | 手順がない/硬すぎる | 手順はあるが自由度調整が弱い | 脆弱な箇所は具体的、判断が必要な箇所は柔軟 |
| Gotchas | 失敗例がない | 注意点はあるが抽象的 | 実際の失敗点、footgun、確認方法が具体的 |
| Progressive disclosure | 本文に詳細を詰め込みすぎ/資材が発見不能 | 分離はあるが参照条件が弱い | SKILL.mdは短く、必要時に読むreferences/scripts/assetsが明確 |
| Deterministic assets | 反復作業を毎回モデルに書かせる | 一部テンプレートや手順がある | スクリプト、テンプレート、検査コマンドで再現性を高めている |
| Setup and safety | 設定・権限・破壊的操作が無防備 | 一部注意がある | 未設定時の質問、dry-run、承認、境界条件が明確 |
| Team distribution | 個人用メモに留まる | 共有方法はあるが運用が弱い | 導入対象、PR/marketplace、依存Skill、更新責任が明確 |
| Measurement and iteration | 改善サイクルがない | フィードバック方法が曖昧 | 使用ログ、期待起動頻度、改善ループ、Gotchas追加方針がある |

### descriptionの書き方原則

元記事の核心: **"Write descriptions for the model, not for humans."** セッション開始時、モデルは全スキルの name + description 一覧をスキャンし、「このリクエストに使えるスキルがあるか？」を判断する。description は人間向けの要約ではなく、**モデルのトリガー判断材料**として書く。

- `name` と `description` だけが常にコンテキストに載る（約100語以内）。本文はトリガー後にしか読み込まれないため、「いつ使うか」の情報は全て description に集約する。
- description の長さは**混同リスクに比例**させる。目的が一意なスキルは短くてよく、類似スキルと紛らわしいスキルは長くする。

#### Anthropic公式スキルに見る4パターン

**Pattern A — 動詞句 + 使い分け（短い）**: 目的が一意で混同リスクが低いスキル向け。短くてもスコープと境界が明確。

> `review`: "Review a GitHub pull request; for your working diff use /code-review"
> `init`: "Initialize a new CLAUDE.md file with codebase documentation"

**Pattern B — What + "Use when" + トリガー語（中程度）**: "Use when" で起動条件を列挙し、ユーザーが言いそうなフレーズを含める。日本語では「〜時に使用する。「〜」「〜」で起動する」が対応する。

> `verify`: "Verify that a code change actually does what it's supposed to by running the app and observing behavior. Use when asked to verify a PR, confirm a fix works, test a change manually, check that a feature works, or validate local changes before pushing."

**Pattern C — What + 使い分け + Anti-trigger（中〜長）**: 類似スキルとの混同リスクがあるため、**使わないケース**を明示する。

> `simplify`: "Review the changed code for reuse, simplification, efficiency, and altitude cleanups, then apply the fixes. Quality only — it does not hunt for bugs; use /code-review for that."
> `loop`: "Run a prompt or slash command on a recurring interval (e.g. /loop 5m /foo). Omit the interval to let the model self-pace. - When the user wants to set up a recurring task, poll for status, or run something repeatedly on an interval. Do NOT invoke for one-off tasks."

**Pattern D — Trigger-heavy + ルール（長い）**: 誤起動/起動漏れのコストが高いスキル。TRIGGER/SKIP ルールや具体例で精密に制御する。

> `claude-api`: "Reference for the Claude API / Anthropic SDK — model ids, pricing, params, streaming, tool use, MCP, agents, caching, token counting, model migration. TRIGGER — read BEFORE opening the target file — whenever: the prompt names Claude/Anthropic in any form (...); the user asks about an LLM — never answer from memory; OR the task is LLM-shaped with provider unstated (...). SKIP only when another provider is being worked on (...)"

#### 良い簡潔さ vs 悪い簡潔さ

短い description でも、トリガー判断に必要な情報があれば問題ない。

| 例 | 評価 | 理由 |
| --- | --- | --- |
| "Review a GitHub pull request; for your working diff use /code-review" | 良い | 短いが、スコープ（GitHub PR）と境界（/code-review との使い分け）が明確 |
| "ユーザーが現在の変更をローカルでgitコミットしたい時に使用する。作業ツリー差分、関連issue、ユーザーの意図から、意図したファイルだけのステージングとConventional Commits形式の日本語description付きコミットを作る。「コミットして」「commit」「変更をコミット」「コミットメッセージ」で起動する。pushも依頼されている場合はgit-pushを使用し、このスキルは使用しない。" | 良い | 入力・成果物・トリガー語・使わないケースが全て含まれている |
| "gitでcommitするときに使用する" | 悪い | 成果物不明、使わないケースなし、トリガー語不足。pushも含む？コミットメッセージ生成？ステージング？が判断できない |
| "Commits code changes" | 悪い | 同上。スコープと境界が不明 |

日本語スキルでは「〜時に使用する。…から、〜を作る。「〜」で起動する。〜には〜を使用し、このスキルは使用しない」のパターンで、入力・成果物・トリガー語・境界を1文にまとめられる。英語スキルでは "Use when ..." や "; for X use /other-skill"、"Do NOT use for ..." で同様の効果を得る。

補足: 元記事は「スキル内で最もシグナルが高いのはGotchasセクション」としている。GotchasとNon-obvious valueの不足は、他観点が高得点でも最優先の改善対象として扱う。

## 3. 総合判定

- **A / 16〜20点**: チーム共有してよい。小さな改善で継続運用可能。
- **B / 12〜15点**: 実用可能。共有前に高優先の改善を行う。
- **C / 8〜11点**: パイロット向け。目的、description、Gotchas、資材設計の見直しが必要。
- **D / 0〜7点**: 再設計推奨。Skillとして切り出す価値または境界を再確認する。

補足: 元記事は「優れたスキルの多くは数行と1つのGotchaから始まり、追記されて育った」としている。低得点でも目的とトリガーが健全なら、再設計ではなくGotchas追加と計測を軸にした成長ロードマップを提案する。

## 4. ブロッカー判定

点数に関わらず、以下は重要指摘（Critical）にする。

- `name` とディレクトリ名が一致しない、またはfrontmatterが壊れている。
- descriptionに起動条件がなく、モデルがいつ使うか判断できない。
- 破壊的操作、外部送信、push、デプロイ、チケット作成を伴うのに事前確認や安全ルールがない。
- APIキー、パスワード、個人情報などの秘密情報をSkillに直接含めている。
- 1つのSkillが3カテゴリ以上を主目的として扱い、成果物も分岐している。

## 5. 改善提案の型

レビューでは、単に「不足」と書かず、次の形で改善案にする。

- **description改善**: 上記「descriptionの書き方原則」のPattern A〜Dから、スキルの混同リスクに応じたパターンを選び、改訂案を提示する。改訂時のチェックリスト:
  - 動詞句で始まっているか（英語: verb phrase / 日本語: 動詞句 or「〜時に使用する」）
  - モデルがいつ使うか判断できるか（トリガー条件）
  - 類似スキルとの境界が明確か（Anti-trigger: "〜には使用しない" / "use /other for that"）
  - ユーザーが言いそうなトリガー語を含むか（日本語・英語どちらでも）
  - 長さがスキルの混同リスクに見合っているか（一意なら短く、紛らわしいなら長く）
- **Gotchas追加**: Claudeが間違えやすい具体例、検出方法、回避策を書く。
- **段階的開示**: 本文から詳細を `references/` に移し、読む条件をSKILL.mdへ残す。
- **スクリプト化**: 毎回同じ検査・変換・集計をしている箇所を `scripts/` に寄せる。
- **テンプレート化**: 成果物の書式が決まっている場合は `assets/` または `references/` に置く。
- **設定導線**: SlackチャンネルやプロジェクトIDなど、未設定だと失敗する値は設定ファイル（`config.json` など）または質問導線（AskUserQuestion など）を作る。
- **状態の永続化**: 定期実行・差分実行する業務自動化スキルでは、前回実行の結果をappend-onlyログやJSON/SQLiteへ残し、差分だけ処理できるようにする。プラグイン配布なら保存先は `${CLAUDE_PLUGIN_DATA}` の安定ディレクトリを使う。
- **フック化**: 破壊的操作を伴うSkillには、Skill起動時だけ有効になるPreToolUseフックで危険コマンド（`rm -rf`、force-push、`DROP TABLE` など）をブロックするオンデマンドガードレールを提案する。
- **運用設計**: 共有先、所有者、更新タイミング、利用ログ（例: PreToolUseフックで使用を記録し、人気と起動不足を把握する）、採用基準を明示する。
