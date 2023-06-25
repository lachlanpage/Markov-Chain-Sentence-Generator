from graph_utilities import display_sentiment_score
from sentiment_utilities import analyze_sentiment_of_string, analyze_sentiment_by_sentence
from text_utilities import TextGenerator
import config

# Positive example
positive_text = "I love this product. It's amazing!"
print("Positive Example:", positive_text)
positive_sentiment_polarity = analyze_sentiment_of_string(positive_text)
print("Positive Example Polarity Score:", positive_sentiment_polarity)

# Negative example
negative_text = "This is the worst experience ever. I'm so disappointed."
print("Negative Example:", negative_text)
negative_sentiment_polarity = analyze_sentiment_of_string(negative_text)
print("Negative Example Polarity Score:", negative_sentiment_polarity)

# Neutral example
neutral_text = "The package contains two items and an instruction manual."
print("Neutral Example:", neutral_text)
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


corpus_string = TextGenerator.return_corpus_text(config.Config.TRAINING_CORPUS)

average_polarity = analyze_sentiment_by_sentence(corpus_string)

display_sentiment_score(average_polarity)
