import random


def generate_text(file_name, prefix_length, output_words_length):
    """
    Generate random text based on the input file content, and given prefix and word lengths.

    Args:
      file_name (str): The path to the input text file.
      prefix_length (int): The length of the prefix as a tuple for the transition dictionary.
      output_words_length (int): The number of words in the generated text.

    Returns:
      None

    Prints:
      The generated text based on the provided parameters.
    """
    with open(file_name, 'r') as content_file:
        file_string = content_file.read()

    # Preprocessing the text
    file_string = file_string.lower()
    for char in ["!", ".", ",", "@", "&amp;", "?", "-"]:
        file_string = file_string.replace(char, " ")
    for char in ['"', '(', ')']:
        file_string = file_string.replace(char, "")
    file_string = file_string.split()

    # Initialize the transition dictionary.
    # Build a transition dictionary called chain for the given text represented by file_string.
    # It uses a Markov chain model, where the keys are sequences of characters (prefixes) and
    # the values are lists of characters that follow the corresponding sequence (successor characters).
    #
    # Initialize the chain by setting a tuple of dot characters (of prefix_length length) as the initial key,
    # and assign a list containing a space as its value. For example, with prefix_length equal to 3,
    # the resulting chain dictionary would look like: {('.', '.', '.'): [' ']}.
    #
    # This code snippet is typically found in implementations of Markov chain text generation algorithms, where chain
    # serves as a transition dictionary. The key-value pair being set here initializes the starting state for the
    # chain with a predetermined tuple of a specific length (determined by prefix_length).
    chain = {}
    chain[tuple(['.'] * prefix_length)] = [' ']

    # Build the transition dictionary by iterating through the text in file_string, extracting
    # subsequences of length prefix_length and updating the transition dictionary:
    for i in range(len(file_string) - prefix_length):

        # Create a tuple seq from the current subsequence of characters. Extracts a substring of length prefix_length
        # from file_string starting at index i. Then, tuple() converts the resulting substring into a tuple
        # containing individual characters of the substring. Finally, the tuple is assigned to the variable seq.
        seq = tuple(file_string[i: i + prefix_length])

        # Check if the sequence seq is not in the chain dictionary yet.
        if seq not in chain:

            # If it's not, create a new empty list as the value for the key seq.
            chain[seq] = []

        # Append a character to the list of characters associated with this sequence.
        # The character is the one after the end of the sequence in the file_string
        chain[seq].append(file_string[i + prefix_length] if i + prefix_length < len(file_string) else '.')

    # Generate the text
    # TODO: Choose the first word of the sentence from STDIN so you can direct the output a bit.
    # start_seq = ("one", "is")
    # start_seq is a tuple that must be the length of the markov order, eg. 3
    start_seq = random.choice(list(chain.keys()))
    # print(start_seq)
    final_word_list = list(start_seq)
    current_seq = start_seq

    # This loop generates a sequence of words using a Markov chain, where chain is a dictionary
    # representing the transitions between words. Loop output_words_length times
    for i in range(output_words_length):
        # Choose the next word randomly from possible words associated with current_seq
        next_word = random.choice(chain[current_seq])

        # Update current_seq by adding next_word, removing the first word and converting back to tuple
        current_seq = tuple((list(current_seq) + [next_word])[1:])

        # Add the chosen next_word to final_word_list which stores the full sequence of generated words
        final_word_list.append(next_word)

    # If the last word of the sentence is "and", remove it.
    if final_word_list[-1] in ["and", "i", "mr"]:
        final_word_list.pop()

    # If the first word of the sentence is "and", remove it.
    if final_word_list[0] in ["and", "him"]:
        final_word_list.pop()

    # print(' '.join(final_word_list))

    return final_word_list

def convert_word_list_to_string(final_word_list):
    return ' '.join(final_word_list)

