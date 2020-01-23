from wordcloud import WordCloud


import pandas as pd
import stopwords


def draw_word_cloud(text: str, with_download: bool = False, filename: str = "example.png"):
    stopWords = set(stopwords.stopwords)
    wordcloud = WordCloud(stopwords=stopWords,
                          background_color="white", width=1440, height=960, margin=4).generate(text)
    wordcloud.to_file(filename)
