# 制御フローチェックリスト

> **基本定理**: 条件・ループ・制御フローの変更は「自然」に書く — 読者が立ち止まって読み返さずに済むように。

## 1. 比較の引数の順序

**変化する値(調べられている値)を左に、比較対象の安定した値(定数・限界値)を右に**置く。英語の語順に合う。

- `while (bytes_received < bytes_expected)` が自然で、`while (bytes_expected > bytes_received)` は不自然。
- 例外: 「Yoda 記法」(`if (NULL == obj)`)は代入と比較の取り違え防止のための旧来の手法。現代のコンパイラは警告するので不要。

## 2. if/else ブロックの順序

以下を優先する。競合する場合は判断する:

1. **正のケース**を先に: `if (debug)` を `if (!debug)` の前に
2. **簡単なケース**を先に: 先に片付ける。else も同時に画面に収まる利点がある
3. **面白い・目立つケース**を先に: 「ピンクの象」効果 — `if (!url.HasQueryParameter("expand_all")) { … } else { … }` では、読者の頭は最初から expand_all のことを考えてしまう。expand_all を先に処理する

例外: 負のケースがより簡単で重要(エラー処理など)なら、それを先にする:
```python
if not file:
    # Log the error ...
else:
    # ...
```

## 3. 三項演算子 (`?:`) は単純な場合のみ

- 単純な値の選択(`time_str += (hour >= 12) ? "pm" : "am";`)は可読で許容。
- 複雑な式(`return exponent >= 0 ? mantissa * (1 << exponent) : mantissa / (1 << -exponent);`)は理解時間がかかる。
- **デフォルトは if/else。三項演算子は最も単純なケースだけ。**

## 4. do/while ループを避ける

- 条件がコードの「下」にあるのは不自然。if/while/for では条件が保護するコードの上に来る(上下読みの習慣に合う)。
- 多くの do/while は while に書き換えられる:
  ```
  while (node != null && max_length-- > 0) { ... }
  ```
- do/while 内の `continue` は特に混乱を招く。「do 文はエラーと混乱の元。条件は目の前にある方がいい」

## 5. 関数から早く返す (guard clause)

- 「関数は return を1つだけにすべき」は迷信。**複数 return はまったく問題ない**。
- 前提条件のチェック(ガード節)を先頭に:
  ```java
  public boolean Contains(String str, String substr) {
      if (str == null || substr == null) return false;
      if (substr.equals("")) return true;
      ...
  }
  ```
- クリーンアップの保証は return 単一化ではなく言語の構造で実現する: C++ はデストラクタ、Java/Python は try/finally、Python は with、C# は using。
- 純 C で大きな関数の場合のみ、`goto cleanup;`(単一出口)が選択肢になり得る。

## 6. goto を避ける

- 単一の `exit` ラベル(関数末尾の共通クリーンアップ)なら害が少ないが、**複数の goto ターゲット、特に上向きの goto** はスパゲッティコードになる。ループで置き換える。

## 7. ネストを最小化する

- ネストの深さは読者の「メンタルスタック」に条件を積む。閉じブレースで何が閉じたか思い出させ、`}` を見たときの「ポップ」が難しい。
- **失敗ケースを先に処理して early return**:
  ```cpp
  if (user_result != SUCCESS) {
      reply.WriteErrors(user_result); reply.Done(); return;
  }
  if (permission_result != SUCCESS) {
      reply.WriteErrors(permission_result); reply.Done(); return;
  }
  reply.WriteErrors("");
  reply.Done();
  ```
- **ループ内は `continue` でガード**:
  ```cpp
  for (...) {
      if (results[i] == NULL) continue;
      non_null_count++;
      if (results[i]->name == "") continue;
      ...
  }
  ```
- 変更を加えるときは**新しい視点**でコード全体を見直す。挿入時に自分には「太字」に見えたコードも、後から見る人には全体の一部にしか見えない(ネストがこうして蓄積する)。

## 8. 高レベルの実行フローを追いやすく保つ

コードの「背後」で実行される構造の過剰使用に注意:

| 構造 | フローがどう曖昧になるか |
| --- | --- |
| スレッド | いつどのコードが実行されるか不明 |
| シグナル/割り込みハンドラ | いつでも実行され得る |
| 例外 | 複数の関数呼び出しを遡って伝播する |
| 関数ポインタ・無名関数 | 実行時に何が呼ばれるか不明 |
| 仮想メソッド | サブクラスのコードが呼ばれる可能性 |

有用な構造もあるが、コードの大部分をこれらの構造にしない。乱用すると「三カードモンテ」のように追跡不能になる。

## 診断時のチェック項目 (要約)

- [ ] 比較の左右が「変化する値 vs 安定した値」の順になっているか
- [ ] if/else の順序が正・簡単・目立つケース優先になっているか (否定が先頭に来ていないか)
- [ ] 複雑な三項演算子・do/while・goto が使われているか
- [ ] 深いネストがあるか (early return / continue ガードで浅くできるか)
- [ ] ガード節(前提条件の先頭チェック)がないか
- [ ] 制御フロー変数 (`done`, `found`, `success`) が break/return で置き換えられるか
- [ ] 実行フローを曖昧にする構造が過剰でないか
