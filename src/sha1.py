import hashlib
import struct

class sha1_expected:
    def __init__(self, input_string):
        self.input_string = input_string
    
    def hash(self):
        sha1_hash = hashlib.sha1()
        sha1_hash.update(self.input_string.encode('utf-8'))
        return sha1_hash.hexdigest()

class sha1:
    def __init__(self, input_string):
        self.input_string = input_string
    
    def hash(self):
        # 1. メッセージを整形する
        message = self._pad_message()
        
        # 2. メッセージを512bitごとのワードブロックに分割する
        words = self._generate_blocks(message)
        words_length = len(words)
        for i in range(words_length):
            # print("block", i, ":", words[i])
            # print("block", i, " bit_length :", (8 * len(words[i])) & 0xffffffffffffffff)
            pass
            
        # 3. ブロックごとに処理を行う
        h0, h1, h2, h3, h4 = self._initialize_registers() # 初期値の設定
        
        for i in range(words_length):
            # 3.1 ブロックを80ワードに拡張する
            w = self._expand_message(words[i])
            print("w:", w)
            
            # 3.2 ハッシュ値を計算する
            a, b, c, d, e = h0, h1, h2, h3, h4
            for j in range(80):
                if 0 <= j <= 19:
                    f = (b & c) | ((~b) & d)
                    k = 0x5A827999
                elif 20 <= j <= 39:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif 40 <= j <= 59:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                elif 60 <= j <= 79:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6
                
                temp = (self._left_rotate(a, 5) + f + e + k + w[j]) & 0xffffffff
                e = d
                d = c
                c = self._left_rotate(b, 30)
                b = a
                a = temp
            
            h0 = (h0 + a) & 0xffffffff
            h1 = (h1 + b) & 0xffffffff
            h2 = (h2 + c) & 0xffffffff
            h3 = (h3 + d) & 0xffffffff
            h4 = (h4 + e) & 0xffffffff
            
        hash_value = '{:08x}{:08x}{:08x}{:08x}{:08x}'.format(h0, h1, h2, h3, h4)
        return hash_value

    def _pad_message(self):
        message = bytearray(self.input_string.encode())
        bit_length = (len(message) * 8) & 0xffffffffffffffff
        
        
        # 2. パディングする
        message.append(0x80) # 0x80 = 1000 0000
        while len(message) % 64 != 56:
            message.append(0x00)
        message += struct.pack('>Q', bit_length)
        # print("after padding : ", message)
        # print("after padding_length : ", (8 * len(message)) & 0xffffffffffffffff)
        
        return message
    
    def _generate_blocks(self, message):
        return [message[i:i+64] for i in range(0, len(message), 64)]
    
    def _initialize_registers(self):
        return 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0
    
    def _expand_message(self, block):
        w = list(block[i:i+4] for i in range(0, len(block), 4))
        w += [b'\x00'] * (80 - len(w))
        
        for i in range(16, 80):
            previous_w = int.from_bytes(w[i-3], byteorder='big') \
                        ^ int.from_bytes(w[i-8], byteorder='big') \
                        ^ int.from_bytes(w[i-14], byteorder='big') \
                        ^ int.from_bytes(w[i-16], byteorder='big')
            w[i] = self._left_rotate(previous_w, 1).to_bytes(4, byteorder='big')
        
        return [int.from_bytes(word, byteorder='big') for word in w]
    
    def _left_rotate(self, value, rotation):
        return ((value << rotation) | (value >> (32 - rotation))) & 0xffffffff


# 使い方の例

if __name__ == '__main__':
  input_string = "hello" #input("文字列を入力してください:")
  hasher = sha1(input_string)
  hashed_string = hasher.hash()
  
  print("ハッシュ化された文字列:", hashed_string) 
  
  hasher_expected = sha1_expected(input_string)
  hashed_string_expected = hasher_expected.hash()
  print("期待されるハッシュ化された文字列:", hashed_string_expected)
