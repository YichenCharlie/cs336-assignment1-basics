import regex as re

PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""


# text = "low low low low low lower lower widest widest widest newest newest newest newest newest newest"

text = "low<|endoftext|>newest<|endoftext|>"
special_tokens = ["<|endoftext|>","<|startoftext|>"]

if special_tokens:
    escaped_tokens = [re.escape(token) for token in special_tokens]
    special_pattern = "|".join(escaped_tokens)
    sege = re.split(special_pattern, text)
else:
    sege = [text]

chars = []
for se in sege:
    for macth in re.finditer(PAT,se):
        chars.append(macth.group())
# dic = {}
# for char in chars:
#     dic[char] = dic.get(char,0) + 1

# pair_dic = {}
# for char in chars:
#     for i in range(1,len(char)):
#         pair_dic[((char[i-1]).encode("utf-8") , (char[i]).encode("utf-8"))] = pair_dic.get(((char[i-1]).encode("utf-8") , (char[i]).encode("utf-8")),0) + 1

# print(pair_dic)

# pair_char= max(pair_dic,key= lambda pair: (pair_dic[pair], pair))

#初始化

vocab_size = 260

#将文本化成字节token
token_words = []
for word in chars:
    tokens = []
    for byte_value in word.encode("utf-8"):
        tokens.append(bytes([byte_value]))
    token_words.append(tokens)

#初始化词表
vocab = {}
for i in range(256):
    vocab[i] = bytes([i])

for special_token in special_tokens:
    vocab[len(vocab)] = special_token.encode("utf-8")
start = len(vocab)

#报错判断
if vocab_size < len(vocab):
    raise ValueError("vocab_size cannot be smaller than the initial vocabulary.")

nums_merge = vocab_size - len(vocab)

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

# pair_once = [apply_merge(tokens, pair_char) for tokens in token_words]

# print("Selected pair:", pair_char)
# print("Before:", chars[-1])
# print("After:", pair_once[-1])

# pair_dic = {}

# for tokens in pair_once:
#     for i in range(1,len(tokens)):
#         pair_dic[(tokens[i-1] , tokens[i])] = pair_dic.get((tokens[i-1] , tokens[i]),0) + 1

# pair_char= max(pair_dic,key= lambda pair: (pair_dic[pair], pair))
# pair_twice = [apply_merge(tokens,pair_char) for tokens in pair_once]

# print("Selected pair:", pair_char)
# print("Before:", chars[-1])
# print("After:", pair_twice)

def count_pair(token_words):
    count_dic = {}
    for token in token_words:
        for index in range(1,len(token)):
            pair = (token[index -1] , token[index])
            count_dic[pair] = count_dic.get(pair, 0) + 1
    return count_dic



# count_dic1 = count_pair(pair_twice)
# max_feq = max(count_dic1, key =lambda kv:(count_dic1[kv] , kv))
# print(max_feq)


curr = token_words
merges = []
for num in range(nums_merge):

    count = count_pair(curr)
    if not count:
        break
    best_freq = max(count, key = lambda kv:(count[kv],kv))
    merges.append(best_freq)
    curr = [apply_merge(tokens, best_freq) for tokens in curr]
    print((num + 1))
    print("count",best_freq)
    print("curr:",curr)
    
print("final_res", curr)
print(merges)



def broaden_vocab(start,merges):

    for i , pair in enumerate(merges):
        a , b =pair
        vocab[start + i] = (a + b)

    return vocab

print(broaden_vocab(start,merges))
recovered = b"".join(b"".join(tokens) for tokens in curr).decode("utf-8")
print(recovered == "".join(sege))