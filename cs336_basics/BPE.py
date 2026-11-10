import regex as re
from pathlib import Path




#导入文本

basic_path = Path(__file__).resolve().parent.parent
file_path = basic_path/"data"/"tiny_test.txt"



#初始化特殊tokens
special_tokens = ["<|endoftext|>","<|startoftext|>"]

#初始化

vocab_size = 260

#预分词正则化初始
PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""


#合并频率token
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

#统计最高频率组合
def count_pair(token_words):
    count_dic = {}
    for token , freq in token_words.items():
        for index in range(1,len(token)):
            pair = (token[index -1] , token[index])
            count_dic[pair] = count_dic.get(pair, 0) + freq
    return count_dic

#将合并后的组合扩展词表
def broaden_vocab(vocab,start,merges):

    for i , pair in enumerate(merges):
        a , b =pair
        vocab[start + i] = (a + b)

    return vocab

def train_bpe(file_path,vocab_size,special_tokens):

    text = Path(file_path).read_text(encoding="utf-8")
    if special_tokens:
        escaped_tokens = [re.escape(token) for token in special_tokens]
        special_pattern = "|".join(escaped_tokens)
        sege = re.split(special_pattern, text)
    else:
        sege = [text]



    #分割special token
    chars = {}
    for se in sege:
        for macth in re.finditer(PAT,se):
            chars[macth.group()] = chars.get(macth.group(),0) + 1




    #将文本化成字节token
    token_words = {}
    for word , freq  in chars.items():
        tokens = []
        for byte_value in word.encode("utf-8"):
            tokens.append(bytes([byte_value]))
        token_words[tuple(tokens)] = freq

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


    #循环合并
    curr = token_words
    merges = []
    for num in range(nums_merge):

        count = count_pair(curr)
        if not count:
            break
        best_freq = max(count, key = lambda kv:(count[kv],kv))
        merges.append(best_freq)
        new_curr = {}

        for tokens, freq in curr.items():
            merged_tokens = tuple(apply_merge(tokens, best_freq))
            new_curr[merged_tokens] = new_curr.get(merged_tokens, 0) + freq

        curr = new_curr
        # print((num + 1))
        # print("count",best_freq)
        # print("curr:",curr)

    vocab = broaden_vocab(vocab,start,merges)

    return vocab,merges

if __name__ == "__main__":
    after_vocab, learned_merges = train_bpe(file_path, vocab_size, special_tokens)

    print("Vocabulary size:", len(after_vocab))
    print("Merges:", learned_merges)

    vocab2, merges2 = train_bpe(file_path, vocab_size, special_tokens)
    print(after_vocab == vocab2, learned_merges == merges2)