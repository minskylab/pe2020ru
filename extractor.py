import pandas as pd


def extract_tweets_from_csv(filename: str = "file.csv") -> str:
    df = pd.read_csv(filename)

    text = df["tweet"].str.cat(sep=". ")

    text = text.replace("pic.twitter.com", "")
    text = text.replace("pic.twitter", "")
    text = text.replace("twitter.com", "")
    text = text.replace("twitter", "")
    text = text.replace(".com", "")
    text = text.replace("https", "")
    text = text.replace("http", "")

    return text
