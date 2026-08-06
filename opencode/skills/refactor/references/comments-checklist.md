# コメントチェックリスト

> **基本定理**: コメントの目的は「読者に書き手と同じ知識を持たせること」。コードの動作を説明するだけが仕事ではない。書くなら**情報密度を最大化**する。

## A. 書くべきでないコメント

### A1. コードからすぐ導ける事実を書かない
- 「The class definition for Account」「Constructor」「Return the profit from this Account」の類は無価値。
- ただし「すぐ導ける」の例外: `name = '*'.join(line.split('*')[:2])` のような1行は「second '*' 以降を削除」のコメントがあると高速に読める。

### A2. コメントのためにコメントしない
- 関数宣言を言い換えただけのコメント(`// Find the Node in the given subtree, with the given name, using the given depth.`)は削除するか改善する。改善するなら、関数宣言にない情報を足す:
  ```
  // Find a Node with the given 'name' or return NULL.
  // If depth <= 0, only 'subtree' is inspected.
  ```

### A3. 悪い名前をコメントで補わない (crutch comment)
- コメントで名前の悪さを説明する代わりに**名前を直す**。例: `CleanReply()` に「Reply の制限を実施する」と書くより、`EnforceLimitsFromRequest()` に改名する。
- `DeleteRegistry()` に「レジストリは実際には変更しません」と注釈するより `ReleaseRegistryHandle()` に改名する。
- **良いコード > 悪いコード + 良いコメント**

## B. 書くべきコメント

### B1. 監督コメンタリー — なぜこの実装なのか
- `// Surprisingly, a binary tree was 40% faster than a hash table for this data.` — 読者の「最適化しなくては」という時間の浪費を防ぐ。
- `// This heuristic might miss a few words. That's OK; solving this 100% is hard.` — バグと誤解されるのを防ぐ。
- コードの状態が悪いことも記録する: `// This class is getting messy. Maybe we should create a 'ResourceNode' subclass...`

### B2. コードの欠陥を記録する
| マーカー | 意味 |
| --- | --- |
| TODO: | まだ手を付けていないこと |
| FIXME: | 既知の壊れたコード |
| HACK: | 洗練されていない解決策 |
| XXX: | 危険! 大きな問題 |

### B3. 定数の「ストーリー」を書く
- `NUM_THREADS = 8  # as long as it's >= 2 * num_processors, that's good enough.` — 調整時の指針になる。
- `// Impose a reasonable limit - no human can read that much anyway.` のように「値が重要でない」ことでも有用。
- 名前が明確な定数(`SECONDS_PER_DAY`)は不要だが、多くの定数はコメントで改善できる。

### B4. 読者の「Huh?」を予想して書く
- 奇妙に見えるが理由のあるコードを解説する: `vector<float>().swap(data);` には「STL swap trick でメモリを解放する」ことを書く。

### B5. 予想される落とし穴を宣伝する
- `// Calls an external service to deliver email. (Times out after 1 minute.)` — HTTP リクエスト内で呼ばれ得る罠を事前警告。
- `// Runtime is O(number_tags * average_tag_depth), so watch out for badly nested inputs.`

### B6. ビッグピクチャー・コメント
- ファイル/クラスレベルで全体像を: 「このファイルはファイルシステムへの便利なインターフェースを提供するヘルパー群。パーミッション等の細部を扱う。」
- 新メンバーへの口頭説明(「これはビジネスロジックとDBの糊付けコード」)をそのままコメントにする。数文で十分。

### B7. 要約コメント
- 低レベルコードの上の1行の要約:
  ```
  # Find all the items that customers purchased for themselves.
  for customer_id in all_customers:
      ...
  ```
- 長い関数内の塊の上にも。段落の見出しとしても機能し、本文を読む前に要点が分かる。塊が分離できるなら関数化を検討(良いコード > 良いコメント)。

> 「what を書くか why か how か」という格言は単純すぎる。読者の理解を助けるなら何を書いてもよい。

### B8. コメントが書けないときの対処
書き始めが一番難しい。思いついたまま(半端でも)書いて、後で磨く。例: 「Oh crap, this stuff will get tricky...」→「Careful: this code doesn't handle duplicates in the list (because that's hard to do)」。

## C. 正確で簡潔なコメントを書く

### C1. 簡潔に
- 3行の説明を1行の図式に: `// CategoryType -> (score, weight)` で `typedef hash_map<int, pair<float,float>> ScoreMap;` を説明。

### C2. 曖昧な代名詞を避ける
- `// Insert the data into the cache, but check if it's too big first.` — 「it」が data か cache か不明。`// If the data is small enough, insert it into the cache.` のように書く。

### C3. 文章を磨く
- ぐだぐだ文を直接的な文に: `Depending on whether we've already crawled this URL before, give it a different priority.` → `Give higher priority to URLs we've never crawled before.`(後者は「どちらが高い優先度か」の情報も追加している)

### C4. 関数の動作を正確に
- `// Return the number of lines in this file.` は「line」の定義が曖昧 → `// Count how many newline bytes ('\n') are in the file.` (空ファイルなら 0 を返すこと、`\r` を無視することまで伝わる)

### C5. 入出力例でコーナーケースを示す
- 例は「機能を披露」するものを選ぶ: `// Example: Strip("abba/a/ba", "ab") returns "/a/"` (chars は文字集合で、繰り返し除去することを示す)
- `Partition` の例では pivot と等しい要素・重複・非ソート結果・戻り値と値の衝突を避けた例を選ぶ。

### C6. 意図を述べる
- `// Iterate through the list in reverse order` → `// Display each price, from highest to lowest`
- 意図コメントは「コードと意図の冗長性チェック」として機能し、バグを検出できる。

### C7. 名前付き引数コメント
- 謎のリテラル引数に注釈: `Connect(/* timeout_ms = */ 10, /* use_encryption = */ false);`
- **boolean 引数は必ず値の前に**コメントを置く。後ろに置くと「false は使うのか使わないのか」が分からない。

### C8. 情報密度の高い言葉を使う
- 「DBと同じ情報を高速化のため持っていて、読み出し時にチェックして…」→ `// This class acts as a caching layer to the database.`
- 「住所の空白除去、Avenue→Ave 変換…等価判定のため」→ `// Canonicalize the street address (...)`。heuristic, brute-force, naive solution など定型的な言葉が使える。

## 診断時のチェック項目 (要約)

- [ ] コードから自明な事実を言い換えただけのコメントがある (削除・改善対象)
- [ ] 悪い名前を説明する「松葉杖コメント」がある (名前を直す)
- [ ] なぜこの実装か・意図・定数の由来が書かれていない
- [ ] 読者が「Huh?」となる箇所・落とし穴が無注釈
- [ ] コメントの「it / this」が何を指すか曖昧
- [ ] コメントが簡潔でない・情報密度が低い
- [ ] 関数の仕様に不明点がある (境界条件・エッジケースを I/O 例で示せないか)
- [ ] 謎のリテラル引数 (特に boolean) に注釈がない
