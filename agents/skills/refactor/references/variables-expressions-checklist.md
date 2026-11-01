# 式と変数チェックリスト

## A. 巨大な式を分解する

> 人間は同時に「3〜4個のもの」しか考えられない。巨大な式はより小さな消化しやすい断片に分解する。

### A1. 説明変数 (explaining variable)
大きな部分式を変数に捕まえると、式が分解され、名前が説明になり、概念が識別できる。

```python
username = line.split(':')[0].strip()
if username == "root":
```

### A2. 要約変数 (summary variable)
説明の必要はないが、概念を1つの名前にまとめると考えやすい。

```cpp
final boolean user_owns_document = (request.user.id == document.owner_id);
if (user_owns_document) { ... }       // 5変数の比較を1つの概念に
...
if (!user_owns_document) { ... }
```

### A3. ド・モルガンの法則
「not を分配して and/or を反転」すると読みやすくなることがある。

```cpp
if (!(file_exists && !is_protected))   // →  if (!file_exists || is_protected)
```

### A4. 短絡評価を悪用しない
- 賢い1行 `assert((!(bucket = FindBucket(key))) || !bucket->IsOccupied());` は「頭の速度バンプ」。同じことを2行で書ける。
- **「賢い」コードに注意 — 後で読む人を混乱させる**。
- 短絡評価の健全な使用例: `if (object && object->method()) ...`、`x = a || b || c`(最初の truthy 値)。

### A5. 複雑なロジックは「反対」から考える
`OverlapsWith()` の実装が場合分けだらけになったら、「重ならない場合」を考えると単純化できる。

```cpp
bool Range::OverlapsWith(Range other) {
    if (other.end <= begin) return false;  // They end before we begin
    if (other.begin >= end) return false;  // They begin after we end
    return true;  // Only possibility left: they overlap
}
```

> 改善された例の if 文はすべて「2個以下の値」しか比較していない。これが理想形。複雑になったら「もっと簡単な方法があるはず」と疑う。

### A6. 巨大な文も分解する
- 繰り返される部分式は共通部分を先に抽出(DRY):
  ```javascript
  var thumbs_up = $("#thumbs_up" + message_num);
  var vote_value = $("#vote_value" + message_num).html();
  ```
  → タイポ回避・行幅縮小・変更箇所が1つになる。
- 長く似た行の繰り返しはマクロ等で本質を明示できる場合がある(C++ の `ADD_FIELD` の例。ただしマクロは通常避ける)。

## B. 変数の扱い

> 変数に関する3つの問題: ①変数の数が多い ②スコープが大きい ③変化の回数が多い。それぞれを減らす。

### B1. 役に立たない変数を消す
- **無用な一時変数**: 式を分解せず・明確化せず・重複を圧縮もしない変数。
  ```python
  now = datetime.datetime.now()          # 不要
  root_message.last_view_time = now      # → datetime.datetime.now() を直接
  ```
- **中間結果**: 結果をすぐ処理できれば変数は不要。「タスクをできるだけ早く完了する」。
  ```javascript
  // before: index_to_remove を探してから splice
  // after:
  for (var i = 0; i < array.length; i += 1) {
      if (array[i] === value_to_remove) {
          array.splice(i, 1);
          return;
      }
  }
  ```
- **制御フロー変数** (`done`, `found` など実データを含まない変数): 構造化プログラミングで排除できることが多い(`break` で置き換え)。複数ループで難しい場合は関数に切り出す。

### B2. スコープを縮める
> **変数を「見える行ができるだけ少ない」場所に置く。見えないものは考えなくて済む。**

- クラスメンバは「クラス内のミニグローバル」。使うメソッドが少なければローカル変数(引数渡し)に降格させる。
- メソッドを static にする(「このコードはあの変数から独立している」と伝える)。
- 大きなクラス・ファイル・関数の分割もデータ(変数)を隔離するのが動機。
- C++ なら if 条件内で宣言: `if (PaymentInfo* info = database.ReadPaymentInfo()) { ... }`
- JavaScript: グローバルを避ける(クロージャで private スコープ化、`var` キーワード必須)。
- Python/JavaScript にはブロックスコープがない — ブロック内で定義された変数は関数全体に漏れる。初期化忘れバグ(`example_value` が未定義の NameError)に注意。共通祖先(使用箇所に最も近い共通ネスト)で定義するか、変数ごと排除する。
- **定義を最初の使用場所の直前へ移動**する(旧 C の「先頭に全部定義」は読者に全変数をいきなり覚えさせる)。
- 定義の移動と「変数を消せるか」を両方検討する。

### B3. write-once 変数を好む
- 一度しか設定されない変数(定数・`const`・`final`・immutable)は考えやすい。
- **変数が操作される場所が多いほど、現在値を推論するのが難しい**。変化回数を減らす。
- 構造の変更で write-once にできることが多い(例: `found` + `elem` を early return と `for` ループで整理し、`elem` をループ内の write-once 変数にする)。

## 診断時のチェック項目 (要約)

**式:**
- [ ] 巨大な式・複数行にまたがる条件があるか (説明変数・要約変数で分解)
- [ ] if の条件が3個以上の値を比較しているか (2個までを目指す)
- [ ] 否定の否定 `!(a && !b)` があるか (ド・モルガン)
- [ ] 短絡評価を利用した「賢い」1行があるか
- [ ] 複雑な場合分けのロジックを「反対」から考えると単純になるか

**変数:**
- [ ] 不要な一時変数・中間結果・制御フロー変数があるか
- [ ] スコープが不必要に大きい変数があるか (ブロック内・関数内へ移動、メンバ→ローカル、グローバル除去)
- [ ] 定義が最初の使用場所よりずっと前にあるか (移動できる)
- [ ] 何度も書き換えられる変数があるか (write-once にできるか)
- [ ] クラスメンバ変数が少数のメソッドでしか使われていないか (ローカルへ降格)
