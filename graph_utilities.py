def display_sentiment_score(sentiment_polarity):
    bar_width = 20
    scaled_value = int((sentiment_polarity + 1) / 2 * bar_width)  # Scale value to fit the bar width
    bar = '|' + '█' * scaled_value + '░' * (bar_width - scaled_value) + '|'

    print(f"Sentiment Polarity: {sentiment_polarity:.2f}")
    print(f"{-1 :<5} {bar} {1 :>5}")

# sentiment_polarity = analyze_sentiment("Your input text goes here")
# display_sentiment_score(sentiment_polarity)


# from termgraph import termgraph
#
# def display_sentiment_score(sentiment_polarity: float):
#     categories = ['Sentiment Polarity']
#     # data = [{'color': termgraph.AVAILABLE_COLORS, 'label': 'Score', 'data': [sentiment_polarity]}]
#     datalist = [sentiment_polarity]
#
#     min_scale = -1
#     max_scale = 1
#
#     termgraph.chart(
#         colors=termgraph.AVAILABLE_COLORS,
#         data=[datalist],
#         labels=categories,
#         args={
#             'title': 'Sentiment Analysis',
#             'width': 20,
#             'format': '{:.2f}',
#             'suffix': '',
#             'no_labels': True,
#             'min_scale': min_scale,
#             'max_scale': max_scale,
#             'stacked': False,
#             'different_scale': False,
#             'histogram': False,
#         }
#     )
#
