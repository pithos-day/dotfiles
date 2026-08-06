# 名前チェックリスト

> **基本定理**: 名前は「小さなコメント」。読者は名前に詰め込まれた情報から多くのことを読み取れる。

## A. 情報を名前の中に詰め込む

### A1. 具体的な単語を選ぶ
「空っぽ」の単語(`get`, `size` など)を避け、文脈に合った具体的な単語を使う。

- `GetPage()` → 取得元がインターネットなら `FetchPage()` / `DownloadPage()`
- `BinaryTree::Size()` → `Height()` / `NumNodes()` / `MemoryBytes()` (何のサイズか不明瞭)
- `Thread::Stop()` → 取り消し不能な重い処理なら `Kill()`、再開可能なら `Pause()`

より「色鮮やか」な単語の例:

| 単語 | 代替案 |
| --- | --- |
| send | deliver, dispatch, announce, distribute, route |
| find | search, extract, locate, recover |
| start | launch, create, begin, open |
| make | create, set up, build, generate, compose, add, new |

ただし **「賢く見せる」より「明確で正確」** を優先する。

### A2. 汎用的な名前 (tmp, retval, foo) を避ける
- `retval` → 値の目的を表す名前を使う。例: 平方和の蓄積なら `sum_squares`。名前に目的が入るとバグが目立つ(`sum_squares += v[i]` はおかしいと気づける)。
- `tmp` は「短命で一時的」であること自体が最も重要な事実のときにだけ使う。それ以外は `user_info` のような名前を。型が伝わらない場合は `tmp_file` のように具体物を付ける(`SaveData(tmp, ...)` はファイルかファイル名かデータか不明)。
- ループイテレータ `i, j, k` は入れ子になると index の取り違えバグが起きやすい。配列名の先頭文字と対応する `ci, mi, ui` の形を使うと、`clubs[ci].members[ui] == users[mi]` のようなミスが一目で分かる。
- 汎用名を使うなら理由を持つこと。多くは「名前を考えるのが面倒」という怠惰から使われる。

### A3. 抽象名より具体名
- `ServerCanStart()` → `CanListenOnPort()` (何ができるのか直接表す)
- `DISALLOW_EVIL_CONSTRUCTORS` → `DISALLOW_COPY_AND_ASSIGN` (「evil」は曖昧、しかもコンストラクタ以外も禁止している)
- `--run_locally` → `--extra_logging` (使われる状況でなく動作を名前に)。直交する2つの意味を1つのフラグにまとめない — それぞれ別フラグ(`--use_local_database`)にする。

### A4. 重要な属性を名前に付け加える
変数に「読者が必ず知るべき重要なこと」があれば、名前に単語を足す。特に**単位**と**危険・見落としやすい状態**。

- 単位: `delay` → `delay_secs`, `size` → `size_mb`, `limit` → `max_kbps`, `angle` → `degrees_cw`, `start` → `start_ms`, `elapsed` → `elapsed_ms` (`getTime()` はミリ秒を返すバグを未然に防ぐ)
- 状態: `password` → `plaintext_password`, `comment` → `unescaped_comment`, `html` → `html_utf8`, `data` → `data_urlenc`, `url` → `untrustedUrl` (サニタイズ後は `trustedUrl` / `safeMessageBody`)
- これはハンガリアン記法ではなく「英語記法」— 必須の属性だけを読みやすく埋め込む。バグが潜みやすい場所ほど重要。

### A5. 名前の長さはスコープに合わせる
- スコープが小さい(見える行が少ない)名前は短くてよい。数行のブロック内の `m` は問題ないが、クラスメンバやグローバルで `m` は致命的。
- プロジェクト固有の略語(`BEManager`)は避ける。新メンバーが理解できない。`eval`, `doc`, `str` のような一般的な略語は許容。
- 不要な単語を削る: `ConvertToString()` → `ToString()`, `DoServeLoop()` → `ServeLoop()`。
- 「長くて打ちにくい」は理由にならない — エディタの補完を使う。

### A6. 名前の書式で意味を伝える
- 種類ごとに書式を統一すると「構文ハイライト」のような効果がある。例: 定数 `kMaxOpenFiles`, マクロ `MACRO_NAME`, クラスメンバ `offset_`(ローカル変数と区別できる), クラス名 `CamelCase`。
- 言語・プロジェクトの慣習に従い、プロジェクト全体で一貫させる。

## B. 誤解されない名前

### B1. 名前の別の解釈を探す
「他の人はこの名前をどう誤解するか」と能動的に検討する。

- `filter` → 「選び出す」なら `select()`、「取り除く」なら `exclude()` (filter はどちらとも取れる)
- `Clip(text, length)` → 切り詰めなら `Truncate(text, max_length)`。さらに単位を付けて `Truncate(text, max_chars)`

### B2. 上限・下限は max_ / min_ を前置
- `CART_TOO_BIG_LIMIT` → `MAX_ITEMS_IN_CART` (LIMIT は「まで」か「まで含む」か曖昧。`max_` なら `>` で比較して明確)

### B3. 範囲の命名
- **包括範囲** (両端を含む): `first` / `last` (`stop` は曖昧)
- **半開範囲** (始端含む・終端含まず): `begin` / `end` (イディオムとして最良)

### B4. 真偽値の命名
- `is` / `has` / `can` / `should` を付けて真偽値であることを明確に: `SpaceLeft()` → `HasSpaceLeft()`
- 曖昧な単語を避ける: `read_password` → `need_password` / `user_is_authenticated`
- **否定形を避ける**: `disable_ssl = false` → `use_ssl = true` (否定の否定が読みにくい)

### B5. ユーザーの期待を裏切らない
- `get*()` は「軽量アクセサ」の慣習。`getMean()` が全サンプルを走査して高コストなら `computeMean()` に改名する(または実装を軽量にする)。
- `size()` が O(n) なら、そのことを名前に反映する(`countSize()` など)。C++ の `list::size()` が O(n) だったバグの例がある。

### B6. 名前の候補を評価する
名前を決めたら、**新しくコードに触れる人**の視点で候補を検討する。
例: 別の experiment から属性を再利用する設定名の候補 `template` / `reuse` / `copy` / `inherit` を検討し、最終的に `copy_experiment` / `inherit_from_experiment_id` が最良(「何が・何から」を明確に)。

## 診断時のチェック項目 (要約)

- [ ] 汎用名 (tmp, retval, foo, data, info, it) が意味を説明していない
- [ ] 単位・状態 (エスケープ済み/未、生データ) が名前に含まれていない
- [ ] 抽象名・曖昧な動詞 (get, handle, process, do) が使われている
- [ ] 長いスコープで短すぎる名前 (1-2文字) がある
- [ ] 真偽値に is/has/can がなく、否定形 (`disable_*`, `not_*`) になっている
- [ ] 限界値・範囲の名前が min/max, first/last, begin/end を使っていない
- [ ] 名前が誤解を招く可能性を検討されていない (filter, clip, stop, length, limit など)
- [ ] プロジェクト固有の略語が新規メンバーに通じない
- [ ] 同じ概念に複数の名前が使われている (一貫性)
