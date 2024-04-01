import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()


class Sentiment:
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"


def analyze_sentiment(message):
    # Analyze the sentiment of the message
    sentiment_scores = sia.polarity_scores(message)

    # Determine the overall sentiment
    if sentiment_scores["compound"] >= 0.05:
        sentiment = Sentiment.POSITIVE
    elif sentiment_scores["compound"] <= -0.05:
        sentiment = Sentiment.NEGATIVE
    else:
        sentiment = Sentiment.NEUTRAL

    return sentiment
