# Before/After 例集

診断結果の説明や修正提案のとき、このファイルの例を参照すると読者に意図を伝えやすい。例は言語非依存で示す。

## 1. 名前: retval → 値の目的を表す名前

```javascript
// BEFORE
var euclidean_norm = function (v) {
    var retval = 0.0;
    for (var i = 0; i < v.length; i += 1)
        retval += v[i] * v[i];
    return Math.sqrt(retval);
};

// AFTER
var euclidean_norm = function (v) {
    var sum_squares = 0.0;
    for (var i = 0; i < v.length; i += 1)
        sum_squares += v[i] * v[i];
    return Math.sqrt(sum_squares);
};
```

ポイント: `sum_squares += v[i]` の書き間違いが一目で気づくようになる。

## 2. 名前: 限界値は max_ 前置で

```python
# BEFORE: LIMIT が「10まで」か「10まで含む」か曖昧 → off-by-one バグの温床
CART_TOO_BIG_LIMIT = 10
if shopping_cart.num_items() >= CART_TOO_BIG_LIMIT:
    Error("Too many items in cart.")

# AFTER
MAX_ITEMS_IN_CART = 10
if shopping_cart.num_items() > MAX_ITEMS_IN_CART:
    Error("Too many items in cart.")
```

## 3. 名前: 真偽値の否定形を避ける

```cpp
// BEFORE
bool disable_ssl = false;

// AFTER
bool use_ssl = true;
```

## 4. コメント: 自明な言い換えコメントを具体化

```cpp
// BEFORE: 関数宣言の言い換えに過ぎない
// Find the Node in the given subtree, with the given name, using the given depth.
Node* FindNodeInSubtree(Node* subtree, string name, int depth);

// AFTER: 宣言にない情報を追加
// Find a Node with the given 'name' or return NULL.
// If depth <= 0, only 'subtree' is inspected.
// If depth == N, only 'subtree' and N levels below are inspected.
Node* FindNodeInSubtree(Node* subtree, string name, int depth);
```

## 5. コメント: 意図を述べる

```cpp
// BEFORE: コードの動作を言い換えるだけ
    // Iterate through the list in reverse order
    for (list<Product>::reverse_iterator it = products.rbegin(); it != products.rend(); ++it)
        DisplayPrice(it->price);

// AFTER: 意図を述べる(実際は「高い順に表示」のはずだった — バグも検出できる)
    // Display each price, from highest to lowest
    for (list<Product>::reverse_iterator it = products.rbegin(); ... )
```

## 6. 制御フロー: ネスト → early return

```cpp
// BEFORE: 2重ネスト。読者は閉じブレースで「どの条件が閉じたか」を思い出す必要がある
if (user_result == SUCCESS) {
    if (permission_result != SUCCESS) {
        reply.WriteErrors("error reading permissions");
        reply.Done();
        return;
    }
    reply.WriteErrors("");
} else {
    reply.WriteErrors(user_result);
}
reply.Done();

// AFTER: 失敗ケースを先に処理。ネストは1段で、各 if は return で終わる
if (user_result != SUCCESS) {
    reply.WriteErrors(user_result);
    reply.Done();
    return;
}
if (permission_result != SUCCESS) {
    reply.WriteErrors(permission_result);
    reply.Done();
    return;
}
reply.WriteErrors("");
reply.Done();
```

## 7. 制御フロー: do/while → while

```java
// BEFORE: 条件がコードの下にあり不自然
public boolean ListHasNode(Node node, String name, int max_length) {
    do {
        if (node.name().equals(name)) return true;
        node = node.next();
    } while (node != null && --max_length > 0);
    return false;
}

// AFTER: while なら max_length=0 や node=null でも正しく動く
public boolean ListHasNode(Node node, String name, int max_length) {
    while (node != null && max_length-- > 0) {
        if (node.name().equals(name)) return true;
        node = node.next();
    }
    return false;
}
```

## 8. 式: 短絡評価の悪用を分解

```cpp
// BEFORE: 賢い1行 — 読者は立ち止まって考える
assert((!(bucket = FindBucket(key))) || !bucket->IsOccupied());

// AFTER: 同じ処理を2行で
bucket = FindBucket(key);
if (bucket != NULL) assert(!bucket->IsOccupied());
```

## 9. 式: 複雑な場合分けは「反対」から

```cpp
// BEFORE: 場合分けが爆発し、バグ(包含ケースの見落とし)も潜む
return (begin >= other.begin && begin <= other.end) ||
       (end > other.begin && end <= other.end) ||
       (begin <= other.begin && end >= other.end);

// AFTER: 「重ならない場合」を判定すると各 if は単純比較1つになる
bool Range::OverlapsWith(Range other) {
    if (other.end <= begin) return false;  // They end before we begin
    if (other.begin >= end) return false;  // They begin after we end
    return true;  // Only possibility left: they overlap
}
```

## 10. 変数: 中間結果の排除

```javascript
// BEFORE: index_to_remove は中間結果
var remove_one = function (array, value_to_remove) {
    var index_to_remove = null;
    for (var i = 0; i < array.length; i += 1) {
        if (array[i] === value_to_remove) {
            index_to_remove = i;
            break;
        }
    }
    if (index_to_remove !== null) {
        array.splice(index_to_remove, 1);
    }
};

// AFTER: early return で「タスクをできるだけ早く完了」
var remove_one = function (array, value_to_remove) {
    for (var i = 0; i < array.length; i += 1) {
        if (array[i] === value_to_remove) {
            array.splice(i, 1);
            return;
        }
    }
};
```

## 11. 変数: 複数回書き換えられる変数を整理

```javascript
// BEFORE: found / i / elem の3変数が関数全体で生き、何度も書き換えられる
var setFirstEmptyInput = function (new_value) {
    var found = false;
    var i = 1;
    var elem = document.getElementById('input' + i);
    while (elem !== null) {
        if (elem.value === '') { found = true; break; }
        i++;
        elem = document.getElementById('input' + i);
    }
    if (found) elem.value = new_value;
    return elem;
};

// AFTER: found を排除し、elem はループ内の write-once 変数に
var setFirstEmptyInput = function (new_value) {
    for (var i = 1; true; i++) {
        var elem = document.getElementById('input' + i);
        if (elem === null)
            return null;  // Search Failed. No empty input found.
        if (elem.value === '') {
            elem.value = new_value;
            return elem;
        }
    }
};
```

## 12. 構造: 無関係なサブ問題の抽出

```python
# BEFORE: URL 生成の詳細が業務ロジックに混ざっている
business = Business()
business.name = request.POST["name"]
url_path_name = business.name.lower()
url_path_name = re.sub(r"['\.]", "", url_path_name)
url_path_name = re.sub(r"[^a-z0-9]+", "-", url_path_name)
url_path_name = url_path_name.strip("-")
business.url = "/biz/" + url_path_name
business.date_created = datetime.datetime.utcnow()
business.save_to_database()

# AFTER: 「名前をURLにする」を抽出(正規表現も名前付きで事前コンパイル)
CHARS_TO_REMOVE = re.compile(r"['\.]+")
CHARS_TO_DASH = re.compile(r"[^a-z0-9]+")
def make_url_friendly(text):
    text = text.lower()
    text = CHARS_TO_REMOVE.sub('', text)
    text = CHARS_TO_DASH.sub('-', text)
    return text.strip("-")

business = Business()
business.name = request.POST["name"]
business.url = "/biz/" + make_url_friendly(business.name)
business.date_created = datetime.datetime.utcnow()
business.save_to_database()
```

## 13. 構造: 一度に1つのタスク

```cpp
// BEFORE: デフォルト値の処理と抽出が織り交ざっている(簡略版)
void UpdateCounts(HttpDownload hd) {
    if (!hd.has_event_log() || !hd.event_log().has_exit_state()) {
        counts["Exit State"]["unknown"]++;
    } else {
        string state_str = ExitStateTypeName(hd.event_log().exit_state());
        counts["Exit State"][state_str]++;
    }
    ...
}

// AFTER: ①デフォルト定義 ②値の抽出 ③集計 の3領域に分離
void UpdateCounts(HttpDownload hd) {
    string exit_state = "unknown";
    string http_response = "unknown";
    string content_type = "unknown";

    if (hd.has_event_log() && hd.event_log().has_exit_state()) {
        exit_state = ExitStateTypeName(hd.event_log().exit_state());
    }
    if (hd.has_http_headers() && hd.http_headers().has_response_code()) {
        http_response = StringPrintf("%d", hd.http_headers().response_code());
    }
    if (hd.has_http_headers() && hd.http_headers().has_content_type()) {
        content_type = ContentTypeMime(hd.http_headers().content_type());
    }

    counts["Exit State"][exit_state]++;
    counts["Http Response"][http_response]++;
    counts["Content-Type"][content_type]++;
}
```

## 14. 構造: 考えを言葉にしてからコードに

```php
// BEFORE: 否定が3つもありロジックツリーが深い
$is_admin = is_admin_request();
if ($document) {
    if (!$is_admin && ($document['username'] != $_SESSION['username'])) {
        return not_authorized();
    }
} else {
    if (!$is_admin) {
        return not_authorized();
    }
}
// continue rendering the page ...

// AFTER: 説明「管理者であるか、文書の所有者であるか」に合わせる
if (is_admin_request()) {
    // authorized
} elseif ($document && ($document['username'] == $_SESSION['username'])) {
    // authorized
} else {
    return not_authorized();
}
// continue rendering the page ...
```

## 15. テスト: 詳細の多いテストを1行に

```cpp
// BEFORE: セットアップの詳細に埋もれ、追加も大変
void Test1() {
    vector<ScoredDocument> docs;
    docs.resize(5);
    docs[0].url = "http://example.com";
    docs[0].score = -5.0;
    docs[1].url = "http://example.com";
    docs[1].score = 1;
    ... // (8つの問題を含む)
}

// AFTER: 本質は1行に。エラーメッセージも役立つ
void CheckScoresBeforeAfter(string input, string expected_output) {
    vector<ScoredDocument> docs = ScoredDocsFromString(input);
    SortAndFilterDocs(&docs);
    string output = ScoredDocsToString(docs);
    assert(output == expected_output);
}
// テスト呼び出し:
CheckScoresBeforeAfter("2, 1, 3", "3, 2, 1");    // Basic sorting
CheckScoresBeforeAfter("0, -0.1, -10", "0");     // All values < 0 removed
CheckScoresBeforeAfter("1, -2, 1, -2", "1, 1");  // Duplicates not a problem
CheckScoresBeforeAfter("", "");                  // Empty input OK
```
