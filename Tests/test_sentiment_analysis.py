from textblob import TextBlob

from graph_utilities import display_sentiment_score
from sentiment_utilities import analyze_sentiment_of_string, interpret_sentiment
from text_utilities import TextGenerator
import config

# Positive example
positive_text = "I love this product. It's amazing!"
positive_sentiment_polarity = analyze_sentiment_of_string(positive_text)
print("Positive Example Polarity Score:", positive_sentiment_polarity)

# Negative example
negative_text = "This is the worst experience ever. I'm so disappointed."
negative_sentiment_polarity = analyze_sentiment_of_string(negative_text)
print("Negative Example Polarity Score:", negative_sentiment_polarity)

# Neutral example
neutral_text = "The package contains two items and an instruction manual."
neutral_sentiment_polarity = analyze_sentiment_of_string(neutral_text)
print("Neutral Example Polarity Score:", neutral_sentiment_polarity)



# def analyze_sentiment_by_sentence(text):
#     analysis = TextBlob(text)
#     sentences = analysis.sentences
#
#     print("Number of sentences:", len(sentences))
#     print("Length of sentence:", len(sentences[0]))
#
#     for i, sentence in enumerate(sentences):
#         sentiment_polarity = sentence.sentiment.polarity
#         sentiment = interpret_sentiment(sentiment_polarity)
#         print(f"Sentence {i + 1}: {sentence}")
#         print(f"Sentiment: {sentiment} (Polarity Score: {sentiment_polarity:.2f})\n")

def analyze_sentiment_by_sentence(text):
    analysis = TextBlob(text)
    sentences = analysis.sentences
    total_sentiment_polarity = 0

    print("Number of sentences:", len(sentences))

    if len(sentences) > 0:
        print("Length of sentence:", len(sentences[0]))

    for i, sentence in enumerate(sentences):
        sentiment_polarity = sentence.sentiment.polarity
        total_sentiment_polarity += sentiment_polarity
        sentiment = interpret_sentiment(sentiment_polarity)
        # print(f"Sentence {i + 1}: {sentence}")
        # print(f"Sentiment: {sentiment} (Polarity Score: {sentiment_polarity:.2f})\n")

        if i > 0:
            running_average_sentiment_polarity = (total_sentiment_polarity / len(sentences))
            display_sentiment_score(running_average_sentiment_polarity)

    average_sentiment_polarity = total_sentiment_polarity / len(sentences)
    print(f"Average Sentiment Polarity: {average_sentiment_polarity:.2f}")
    return average_sentiment_polarity




corpus_string = TextGenerator.return_corpus_text(config.Config.TRAINING_CORPUS)

average_polarity = analyze_sentiment_by_sentence(corpus_string)

# print(f">>>>>> Average Polarity: {average_polarity}")
display_sentiment_score(average_polarity)
