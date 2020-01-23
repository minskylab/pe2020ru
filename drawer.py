from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import pandas as pd


def draw_word_cloud(text: str, with_download: bool = False, filename: str = "example.png"):
    if with_download:
        nltk.download('stopwords')

    stopWords = set(stopwords.words('spanish'))

    wordcloud = WordCloud(stopwords=stopWords,
                          background_color="white", width=1440, height=960, margin=4).generate(text)

    wordcloud.to_file(filename)
