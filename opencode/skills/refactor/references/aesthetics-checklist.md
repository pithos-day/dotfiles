# 見た目チェックリスト

> **基本定理**: 良いコードは「目に優しい」。読者はスキム(走り読み)が速いほど良い。三原則:
> 1. **一貫したレイアウト** — 読者が慣れるパターンを使う
> 2. **類似コードは類似の見た目に** — 同じ形のコードは同じシルエットに
> 3. **関連する行をブロックにまとめる**

## 1. 改行を揃えてシルエットを統一する

複数の類似ブロックがあるとき、1つだけ形が崩れている(改行の位置が違う)と、理由なく視線を引く。

Before (80桁制限のため `t3_fiber` だけ形が崩れている):
```java
public static final TcpConnectionSimulator wifi = new TcpConnectionSimulator(
    500, /* Kbps */
    80, /* millisecs latency */ ...);
public static final TcpConnectionSimulator t3_fiber =
    new TcpConnectionSimulator(
        45000, ...);
```

After (共通コメントを上に移し、データを揃えたコンパクトな表に):
```java
// TcpConnectionSimulator(throughput, latency, jitter, packet_loss)
//                            [Kbps]   [ms]    [ms]    [percent]
public static final TcpConnectionSimulator wifi =
    new TcpConnectionSimulator(500,    80,     200,    1);
public static final TcpConnectionSimulator t3_fiber =
    new TcpConnectionSimulator(45000,  10,     0,      0);
```

## 2. メソッドで不規則さを掃除する

長くて不揃いな繰り返しは、ヘルパーメソッドにまとめると見た目が整う。

Before: 4回続く `assert(ExpandFullName(database_connection, "…", &error) == …)` の重複。
After:
```cpp
CheckFullName("Doug Adams", "Mr. Douglas Adams", "");
CheckFullName("No Such Guy", "", "no match found");
```

> 見た目を整える変更は結果的に「重複コードの排除」「重要な値が一目で見える」「新規テストが書きやすい」など構造的改善をもたらすことが多い。

## 3. 列揃えを活用する

直線のエッジはスキムの「視覚的な手すり」になる。

```python
details  = request.POST.get('details')
location = request.POST.get('location')
phone    = equest.POST.get('phone')   # タイポが目立つ(副次効果)
email    = request.POST.get('email')
url      = request.POST.get('url')
```

- 欠点: 整列の維持コスト、diff が大きくなる(1行変更で周囲の空白が変わる)。しかし試す価値がある。

## 4. 意味のある順序を選び、一貫して使う

順序に意味を持たせる: HTML フォームの順 / 重要度順 / アルファベット順。
- 同じコード内で A, B, C の順で使ったら、以後も同じ順で。`if details: … if phone: … if email: … if location: …` のように途中で順序が変わるのは混乱の元。

## 5. 宣言をブロックにまとめる

役割ごとにグループ化し、必要ならグループに短いコメントを付ける。

```cpp
class FrontendServer {
  public:
    FrontendServer();
    ~FrontendServer();
    // Handlers
    void ViewProfile(HttpRequest* request);
    void SaveProfile(HttpRequest* request);
    // Request/Reply Utilities
    string ExtractQueryParam(HttpRequest* request, string param);
    // Database Helpers
    void OpenDatabase(string location, string user);
};
```

## 6. コードを段落に分ける

長い関数は、空行 + 要約コメントで論理的な段落に分割する(文章の段落と同じ効果)。

```python
def suggest_new_friends(user, email_password):
    # Get the user's friends' email addresses.
    friends = user.friends()
    friend_emails = set(f.email for f in friends)
    # Import all email addresses from this user's email account.
    contacts = import_contacts(user.email, email_password)
    ...
```

## 7. 個人の好みより一貫性

- ブレースの位置(`class Logger {` vs `class Logger\n{`)のような趣味の違いはどちらでもよいが、**混在すると悪い**。
- 「正しい」スタイルよりも、プロジェクトで採用されているスタイルを守る。

> **一貫性は「正しい」スタイルよりも重要**

## 診断時のチェック項目 (要約)

- [ ] 類似ブロックのシルエット(改行位置・構造)が揃っているか
- [ ] 列揃えが使える場面で使われているか (変数定義・引数・表データ)
- [ ] 順序が意味を持ち、コード全体で一貫しているか
- [ ] 宣言・処理が役割ごとにブロック化されているか
- [ ] 長い関数が段落(空行+要約コメント)で区切られているか
- [ ] プロジェクトの書式規約と一貫しているか (個人の好みで別スタイルを混在させていないか)
- [ ] 不要な行内空白・乱れたインデント・不揃いの括弧がないか
