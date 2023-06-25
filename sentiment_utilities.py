from textblob import TextBlob
from text_utilities import TextGenerator
from colorama import Fore, Style
from config import Config
from graph_utilities import display_sentiment_score


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

    average_polarity = analyze_sentiment_by_sentence(corpus_string)

    print(f"{Fore.GREEN}[+] Sentiment analysis of {training_corpus_filename}: {average_polarity:.4f}{Style.RESET_ALL}")

    display_sentiment_score(average_polarity)

    return average_polarity


def analyze_sentiment_of_string(text_string):
    """
    **This function is optimized for analyzing shorter strings.**

    Analyze the overall sentiment of a text string and display the sentiment score.

    The function uses the TextBlob library to analyze the sentiment polarity
    of a text string. It then interprets the sentiment, prints the sentiment and its
    polarity score, and displays the sentiment score graphically.

    Parameters:
        text_string (str): The text string to analyze.

    Returns:
        float: The sentiment polarity of the text string.
    """

    # Instantiate TextBlob and analyze sentiment
    analysis = TextBlob(text_string)

    # Return the polarity score of the analyzed the corpus text string
    sentiment_polarity: float = analysis.sentiment.polarity

    # Interpret the sentiment based on the polarity score
    sentiment = interpret_sentiment(sentiment_polarity)

    # Print the sentiment and its polarity score
    print(f"Sentiment: {sentiment} (Polarity Score: {sentiment_polarity})")

    # TODO: Distinguish between sentiment of corpus and output text
    # Display the sentiment score graphically
    display_sentiment_score(sentiment_polarity)

    return sentiment_polarity


def analyze_sentiment_by_sentence(corpus_as_string):
    """
    **This function is optimized for analyzing longer strings.**

    Analyze the sentiment of each sentence in a text and return the average sentiment.

    The function uses the TextBlob library to split the text into sentences, analyze the sentiment polarity
    of each sentence, and then average the sentiment polarity scores for the whole text.

    Parameters:
        corpus_as_string (str): The text to analyze.

    Returns:
        float: The average sentiment polarity of the sentences in the text.
    """

    # Create a TextBlob object for the given text
    analysis = TextBlob(corpus_as_string)

    # Split the text into sentences
    sentences = analysis.sentences

    # Initialize a variable to keep track of total sentiment polarity
    total_sentiment_polarity = 0

    # Loop through each sentence in the text
    for i, sentence in enumerate(sentences):
        # Get the sentiment polarity of the sentence
        sentiment_polarity = sentence.sentiment.polarity

        # Add the sentiment polarity of the sentence to the total sentiment polarity
        total_sentiment_polarity += sentiment_polarity

        # Interpret and print the sentiment based on the polarity
        # print(interpret_sentiment(sentiment_polarity))

    # Calculate the average sentiment polarity
    average_sentiment_polarity = total_sentiment_polarity / len(sentences)

    return average_sentiment_polarity


def interpret_sentiment(sentiment_polarity):
    """
    Interpret the sentiment based on the polarity score.

    Polarity typically ranges from -1 (very negative) to +1 (very positive),
    with 0 being neutral. This function adds granularity by distinguishing
    somewhat positive and somewhat negative values.

    Parameters:
        sentiment_polarity (float): A sentiment polarity score from -1 to 1.

    Returns:
        str: The interpreted sentiment which can be 'Positive', 'Somewhat Positive',
    'Neutral', 'Somewhat Negative', or 'Negative'.
    """

    if sentiment_polarity > 0.5:
        sentiment = "Positive"
    elif 0 < sentiment_polarity <= 0.5:
        sentiment = "Somewhat Positive"
    elif 0 > sentiment_polarity >= -0.5:
        sentiment = "Somewhat Negative"
    elif sentiment_polarity < -0.5:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment