import difflib
from log_config import configure_logger

logger = configure_logger(__name__)

# For your scenario, you can use a sliding window approach along with a sequence matching
# technique to check if the generated output (30 words) is similar to any part of the input
# text (the entire novel). One possible approach is using Python's difflib.SequenceMatcher:


def get_corpus_string(corpus_as_string):

    return corpus_as_string


def check_similarity(input_text, output_text, window_size, similarity_threshold):
    # Split texts into words
    input_words = input_text.split()
    output_words = output_text.split()

    # Check if output text is shorter than the window size
    if len(output_words) < window_size:
        window_size = len(output_words)

    # Create a SequenceMatcher instance
    matcher = difflib.SequenceMatcher(None, output_words)

    # Save the highest similarity score
    # Initialize to -1 to ensure that the first comparison is always done
    highest_similarity_score = -1

    # Iterate through input text using a sliding window of size window_size
    for i in range(len(input_words) - window_size + 1):
        current_window = input_words[i:i + window_size]
        matcher.set_seq2(current_window)
        similarity_score = matcher.ratio()

        # Update the highest similarity score
        if similarity_score > highest_similarity_score:
            highest_similarity_score = similarity_score

        # If similarity_score exceeds the similarity_threshold, the output is considered too similar
        if similarity_score >= similarity_threshold:
            print("Similarity: ", similarity_score)
            print(output_words)
            print(current_window)
            # TODO: Keep track of  the similarity score and return its highest value
            return highest_similarity_score, "True"

    return highest_similarity_score, "False"

