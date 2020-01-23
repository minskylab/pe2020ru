from nltk.corpus import stopwords


def freq_str(text: str, minimal_counts=1) -> list:

    str_list = text.lower().split()
    str_list = [word.strip(".:;,@ …")
                for word in str_list if not len(word) < 2]

    unique_words = set(str_list)

    freqs = []

    for word in unique_words:
        # print('Frequency of ', word, 'is :', str_list.count(word))
        # word = word[0:len(word)-1] if word.endswith(":") else word
        freqs.append((str_list.count(word), word))

    s_words = set(stopwords.words('spanish'))

    freqs = [f for f in freqs if f[1]
             not in s_words and not f[1].isdigit() and not f[1].startswith("//")]

    freqs = [f for f in freqs if f[0] >= minimal_counts]

    freqs.sort(key=lambda f: f[0], reverse=True)

    return freqs
