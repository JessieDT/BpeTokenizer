from utils import get_stats, merge

class BasicTokenizer:
    def __init__(self):
        super().__init__()
        # self.vocab_size = vocab_size
        # self.num_merges = vocab_size - 256
        # self.merges = self.get_merges(self.num_merges, )

    def train(self, text, vocab_size, verbose=False):
        assert vocab_size >= 256 # the desired final vocabulary size
        num_merges = vocab_size - 256

        tokens = text.encode("utf-8") # raw bytes
        # tokens = list(map(int, tokens))
        ids = list(tokens)

        merges = {} # (int, int) -> int
        vocab = {idx: bytes([idx]) for idx in range(256)}
        for i in range(num_merges):
            stats = get_stats(ids)
            pair = max(stats, key=stats.get)
            idx = 256 + i
            # print(f"merging {pair} into a new token {idx}")
            ids = merge(ids, pair, idx)
            merges[pair] = idx
            vocab[idx] = vocab[pair[0]] + vocab[pair[1]]

            if verbose:
                print(f"merge {i+1}/{num_merges}: {pair} -> {idx} ({vocab[idx]}) had {stats[pair]} occurrences")

        self.merges = merges # used in encode()
        self.vocab = vocab   # used in decode()
    
    def encode(self, text):
        tokens = text.encode('utf-8')
        ids = list(tokens)
        while len(ids) >= 2:
            stats = get_stats(tokens)
            pair = min(stats, key=lambda p: self.merges.get(p, float('inf'))) # in python, the min function will iterate the key of "stats" (dict), and find the key has min idx in "merges"
            if pair not in self.merges:
                break
            idx =self.merges[pair]
            tokens = merge(tokens, pair, idx)
        return tokens
    
    def decode(self, ids):
        tokens = b"".join(self.vocab[idx] for idx in ids)
        text = tokens.decode('utf-8', errors='replace')
        return text