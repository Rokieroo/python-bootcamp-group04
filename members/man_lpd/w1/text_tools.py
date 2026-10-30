def word_count(text: str) -> dict[str, int]:
    """Count lowercase words after removing the specified punctuation."""
    table = str.maketrans("","",".!?;:")
    lowertext = text.lower().translate(table)
    words = lowertext.split()
    wordlist = {}
    for w in words:
        if w in wordlist:
            wordlist[w] += 1
        else:
            wordlist[w] = 1
    return wordlist

# top_k does the following  things:
# 1. Sort the word list by count in descending order.
# 2. Sort each same-count group by alphabetical ascending order.
# 3. Return the top k words as a list of tuples, or first k tuples of the sorted list.
def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return the k most common words, breaking ties alphabetically."""
    wordlist = word_count(text)
    result = sorted(wordlist.items(), key=lambda x: (-x[1], x[0]))[:k]
    return result

