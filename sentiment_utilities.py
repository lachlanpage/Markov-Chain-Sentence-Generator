from textblob import TextBlob
from text_utilities import TextGenerator
from colorama import Fore, Style
from config import Config


def analyze_sentiment(training_corpus_filename):
    """
    Analyzes the sentiment of the given text using TextBlob and returns a sentiment polarity score.

    Args:
        training_corpus_filename (str): The input text to analyze for sentiment.

    Returns:
        float: The sentiment polarity score, which ranges from -1.0 (most negative) to 1.0 (most positive).

    Raises:
        Exception: Any exceptions raised during TextBlob analysis will propagate.
    """
    if Config.VERBOSE:

        print(f"{Fore.GREEN}[+] Analyzing sentiment of {training_corpus_filename}{Style.RESET_ALL}")

    # Convert the corpus text to a string and pass it to TextBlob
    corpus_string = TextGenerator.return_corpus_text(training_corpus_filename)

    # Instantiate TextBlob and analyze sentiment
    analysis = TextBlob(corpus_string)

    # Return the polarity score of the analyzed the corpus text string
    sentiment_polarity = analysis.sentiment.polarity

    # print(f"{Fore.GREEN}[+] Sentiment polarity score: {sentiment_polarity}{Style.RESET_ALL}")

    # sentiment_polarity = analyze_sentiment("Your input text goes here")
    sentiment = interpret_sentiment(sentiment_polarity)

    print(f"Sentiment: {sentiment} (Polarity Score: {sentiment_polarity})")

    # TODO: Do we need to return the sentiment polarity score?
    return sentiment_polarity

def interpret_sentiment(sentiment_polarity):
    if sentiment_polarity > 0:
        sentiment = "Positive"
    elif sentiment_polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment
