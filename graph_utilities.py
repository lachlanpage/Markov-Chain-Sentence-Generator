def display_sentiment_score(sentiment_polarity):
    bar_width = 20
    scaled_value = int((sentiment_polarity + 1) / 2 * bar_width)  # Scale value to fit the bar width
    bar = '|' + '█' * scaled_value + '░' * (bar_width - scaled_value) + '|'

    print(f"Sentiment Polarity: {sentiment_polarity:.4f}")
    print(f"{-1 :<5} {bar} {1 :>5}")
