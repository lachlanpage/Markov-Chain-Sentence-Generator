import difflib

# For your scenario, you can use a sliding window approach along with a sequence matching
# technique to check if the generated output (30 words) is similar to any part of the input
# text (the entire novel). One possible approach is using Python's difflib.SequenceMatcher:


def check_similarity(input_text, output_text, window_size, threshold):
    # Split texts into words
    input_words = input_text.split()
    output_words = output_text.split()

    # Check if output text is shorter than the window size
    if len(output_words) < window_size:
        window_size = len(output_words)

    # Create a SequenceMatcher instance
    matcher = difflib.SequenceMatcher(None, output_words)

    # Iterate through input text using a sliding window of size window_size
    for i in range(len(input_words) - window_size + 1):
        current_window = input_words[i:i + window_size]
        matcher.set_seq2(current_window)
        similarity = matcher.ratio()

        # If similarity exceeds the threshold, the output is considered too similar
        if similarity >= threshold:
            return True

    return False

# Example usage
input_text = "The entire corpus content goes here..."
output_text = "A generated sequence of about 30 words..."
window_size = 30
similarity_threshold = 0.8

too_similar = check_similarity(input_text, output_text, window_size, similarity_threshold)
print("Is the generated text too similar?", too_similar)

# Replace input_text and output_text with your actual texts. Adjust window_size and
# similarity_threshold as needed. This code checks if there's any part of the input
# text with a similarity ratio above the defined threshold when compared to the
# output text. The sliding window size determines how many words you want to consider
# at once while scanning the entire corpus.