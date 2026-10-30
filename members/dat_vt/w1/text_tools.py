"""W1-2: Word counter."""

import string


def word_count(text: str) -> dict[str, int]:
    """Count occurrences of each lowercase word, ignoring punctuation."""
    clean_text = text.translate(str.maketrans('', '', string.punctuation))
    words = clean_text.lower().split()

    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return the top k words sorted by descending count, then alphabetically."""
    counts = word_count(text)
    sorted_items = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return sorted_items[:k]


if __name__ == "__main__":
    user_input = input("Please input a text: ")
    k = int(input("Please input a number: "))
    print(top_k(user_input, k))
