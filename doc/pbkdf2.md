# pbkdf2もやってみる

導出鍵DKは、

DK = PBKDF2(PRF, Password, Salt, c, dkLen)
* PRFは、出力値の長さがhLenの、2つの引数を持つ疑似乱数関数(HMACなど)
* Passwordは、鍵導出のためのマスターパスワード
* Saltは、鍵導出のためのソルト
* cは、ストレッチング回数
* dkLenは、導出鍵のビット長

導出鍵DKは、以下のように求められる。

DK = T_1 + T_2 + ... + T_(dkLen/hLen) (ここで+は文字列の連結を意味する)
T_i = F(Password, Salt, c, i)
F(Password, Salt, c, i) = U_1 ^ U_2 ^ ... ^ U_c (関数FはPRFのc回のXORの繰り返しである)
U_1 = PRF(Password, Salt + INT_32_BE(i))
U_2 = PRF(Password, U_1)
...
U_c = PRF(Password, U_(c-1))

## WPA2の攻略

WPA2では、以下のように求められる。

DK = PBKDF2(PRF=HMAC-SHA1, Password=PASS, Salt=SSID, c=4096, dkLen=256)
hLenは、HMAC-SHA1の出力値の長さ160ビットなので、hLen=160となる。
DK = T_1 + T_2 + ... + T_(256/160)

F(Password=PASS, Salt=SSID, c=4096, i) = U_1 ^ U_2 ^ ... ^ U_c
U_1 = HMAC-SHA1(Password=PASS, Salt=SSID + INT_32_BE(i))
U_2 = HMAC-SHA1(Password=PASS, U_1)
...
U_c = HMAC-SHA1(Password=PASS, U_(c-1))