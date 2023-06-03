import difflib
from log_config import configure_logger
from typing import Tuple

logger = configure_logger(__name__)

# Use a sliding window approach along with a sequence matching
# technique to check if the generated output is similar to any part of the input
# text (the entire corpus). Use Python's difflib.SequenceMatcher.


def get_corpus_string(corpus_as_string):

    return corpus_as_string


def check_similarity(input_text, output_text, window_size, similarity_threshold) -> Tuple[float, float, bool, str]:
    """
    Check if the generated output is similar to any part of the input text (the entire novel).
    One possible approach is using Python's difflib.SequenceMatcher:

    :param input_text:
    :param output_text:
    :param window_size:
    :param similarity_threshold:
    :return: Tuple of highest similarity score, average similarity score, flag indicating output is too similar,
    and the overly similar phrase.
    :rtype: Tuple[float, float, bool, str]
    """

    # # Check if input text is shorter than the window size
    # if len(input_text) < window_size:
    #     window_size = len(input_text)

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

    # Initialize variables to track the sum and count of similarity scores
    sum_similarity_score = 0
    count_similarity_score = 0

    # Iterate through input text using a sliding window of size window_size
    for i in range(len(input_words) - window_size + 1):
        current_window = input_words[i:i + window_size]
        matcher.set_seq2(current_window)
        similarity_score = matcher.ratio()



        # Update the highest similarity score
        if similarity_score > highest_similarity_score:
            highest_similarity_score = similarity_score

        # Update the sum and count of similarity scores
        # Update the sum and count of the highest similarity scores
        sum_similarity_score += highest_similarity_score
        count_similarity_score += 1

        # # If similarity_score exceeds the similarity_threshold, the output is considered too similar
        # if similarity_score >= similarity_threshold:
        #     # Join the current window into a single string
        #     overly_similar_phrase = ' '.join(current_window)
        #
        #     # Return the highest similarity score, a flag indicating that the
        #     # generated output is too similar to the original training corpus, and the overly similar phrase.
        #     return highest_similarity_score, True, overly_similar_phrase

    # Compute the average similarity score
    average_similarity_score = sum_similarity_score / count_similarity_score

    # If the average similarity score is greater than the similarity_threshold, the output is considered too similar
    if average_similarity_score >= similarity_threshold:

        return highest_similarity_score, average_similarity_score, True, None

    # Return the highest and average similarity scores, and a flag indicating output is not too similar to the original text.
    return highest_similarity_score, average_similarity_score, False, None


