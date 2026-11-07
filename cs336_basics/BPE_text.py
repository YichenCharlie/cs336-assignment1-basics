text = "low low low low low lower lower widest widest widest newest newest newest newest newest newest"
chars = text.split(" ")

dic = {}
for char in chars:
    dic[char] = dic.get(char,0) + 1

pair_dic = {}
for char in chars:
    for i in range(1,len(char)):
        pair_dic[((char[i-1]).encode("utf-8") , (char[i]).encode("utf-8"))] = pair_dic.get(((char[i-1]).encode("utf-8") , (char[i]).encode("utf-8")),0) + 1

print(pair_dic)

pair_char= max(pair_dic,key= lambda pair: (pair_dic[pair], pair))

token_words = []

for word in chars:
    tokens = []
    for byte_value in word.encode("utf-8"):
        tokens.append(bytes([byte_value]))
    token_words.append(tokens)


def apply_merge(bs,pair):
    
    res = []
    i = 0
    while i < len(bs):
        if i + 1 < len(bs) and (bs[i] , bs[i+1]) == pair:
            res.append((bs[i] + bs[i+1]))
            i += 2

        else:
            res.append(bs[i])
            i += 1

    return res

pair_once = [apply_merge(tokens, pair_char) for tokens in token_words]

print("Selected pair:", pair_char)
print("Before:", chars[-1])
print("After:", pair_once[-1])

pair_dic = {}

for tokens in pair_once:
    for i in range(1,len(tokens)):
        pair_dic[(tokens[i-1] , tokens[i])] = pair_dic.get((tokens[i-1] , tokens[i]),0) + 1

pair_char= max(pair_dic,key= lambda pair: (pair_dic[pair], pair))
pair_twice = [apply_merge(tokens,pair_char) for tokens in pair_once]

print("Selected pair:", pair_char)
print("Before:", chars[-1])
print("After:", pair_twice[-1])