# sha1アルゴリズムの概要
https://ja.wikipedia.org/wiki/SHA-1


## 手順
https://brilliant.org/wiki/secure-hashing-algorithms/

1. メッセージを整形(パディング等)
2. ブロックに分割
   1. ブロックごとにハッシュ値を計算


## 疑似コード
https://ja.wikipedia.org/wiki/SHA-1

```python
# 注意1 : すべての変数は符号なし32ビットで、計算時にモジュロ232でラップされる。messageLenは64ビットのメッセージ長、そしてhhは160ビットのメッセージ・ダイジェスト。
# 注意2 : この疑似コード中の定数はすべてビッグエンディアンである。各単語の中で、最上位バイトは左端のバイト位置に格納される。

# 初期値
h0 = 0x67452301
h1 = 0xEFCDAB89
h2 = 0x98BADCFE
h3 = 0x10325476
h4 = 0xC3D2E1F0

messageLen = メッセージのビット長(常に文字のビット数の倍数(utf-8なら8倍))

# 前処理
utf-8なら、448(mod 512)となるまで、メッセージの末尾に0x80を追加する。
さらに末尾にmessageLenを64ビットのビッグエンディアン整数として追加する。
これでメッセージ長は512ビットの倍数となる。

# メッセージを512bit(64byte)ずつのブロックに分割する
for each block
  break ブロックを16個の32ビットのワードに分割する
  w[i] (i = 15)
  # 16個のワードを80個のワードに拡張する
  w[i] = (w[i-3] xor w[i-8] xor w[i-14] xor w[i-16]) leftrotate 1 (i = 16..79)

  # このブロックのハッシュ値を計算する
  # 定数の設定
  a = h0
  b = h1
  c = h2
  d = h3
  e = h4

  # 80回のループ メインループ
  for i from 0 to 79
    if 0~19
      f = (b and c) or ((not b) and d)
      k = 0x5A827999
    else if 20~39
      f = b xor c xor d
      k = 0x6ED9EBA1
    else if 40~59
      f = (b and c) or (b and d) or (c and d)
      k = 0x8F1BBCDC
    else if 60~79
      f = b xor c xor d
      k = 0xCA62C1D6
    
    temp = (a leftrotate 5) + f + e + k + w[i]
    e = d
    d = c
    c = b leftrotate 30
    b = a
    a = temp
  
  # このブロックのハッシュ値を現在の計算値に追加する
  h0 = h0 + a
  h1 = h1 + b
  h2 = h2 + c
  h3 = h3 + d
  h4 = h4 + e

# ハッシュ値を出力する
hash = (h0 leftshift 128) or (h1 leftshift 96) or (h2 leftshift 64) or (h3 leftshift 32) or h4
```