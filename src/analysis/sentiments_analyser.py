from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment_textblob(text):
    analysis = TextBlob(str(text))
    return {
        'polarity': analysis.sentiment.polarity,
        'subjectivity': analysis.sentiment.subjectivity,
        'sentiment': 'positive' if analysis.sentiment.polarity > 0.1 
                    else 'negative' if analysis.sentiment.polarity < -0.1 
                    else 'neutral'
    }

def analyze_sentiment_vader(text):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(str(text))
    return {
        'vader_compound': vs['compound'],
        'vader_sentiment': 'positive' if vs['compound'] > 0.05 
                          else 'negative' if vs['compound'] < -0.05 
                          else 'neutral'
    }