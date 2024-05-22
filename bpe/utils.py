def get_stats(ids):
    counts = {}
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    return counts

def merge(ids, pair, idx):
    newids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
            newids.append(idx)
            i += 2
        else:
            newids.append(ids[i])
            i += 1

    return newids

# def get_merges(num_merges, ids):
#     merges = {}
#     for i in range(num_merges):
#         stats = self.get_stats(ids)
#         pair = max(stats, key=stats.get)
#         idx = 256 + i
#         print(f"merging {pair} into a new token {idx}")
#         ids = self.merge(ids, pair, idx)
#         merges[pair] = idx
#     return merges