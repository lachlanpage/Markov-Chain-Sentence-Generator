import random


def generate_text(file_name, prefix_length, word_length):
    """
    Generate random text based on the input file content, and given prefix and word lengths.

    Args:
      file_name (str): The path to the input text file.
      prefix_length (int): The length of the prefix as a tuple for the transition dictionary.
      word_length (int): The number of words in the generated text.

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

    # Initialize the transition dictionary
    chain = {}
    chain[tuple(['.'] * prefix_length)] = [' ']

    # Build the transition dictionary
    for i in range(len(file_string) - prefix_length):
        seq = tuple(file_string[i: i + prefix_length])
        if seq not in chain:
            chain[seq] = []
        chain[seq].append(file_string[i + prefix_length] if i + prefix_length < len(file_string) else '.')

    # Generate the text
    # TODO: Choose the first word of the sentence from a list instead
    # start_seq = ("one", "is")
    # start_seq is a tuple that must be the length of the markov order, eg. 3
    start_seq = random.choice(list(chain.keys()))
    print(start_seq)
    final_word_list = list(start_seq)
    current_seq = start_seq

    for i in range(word_length):
        next_word = random.choice(chain[current_seq])
        current_seq = tuple((list(current_seq) + [next_word])[1:])
        final_word_list.append(next_word)

    # If the last word of the sentence is "and", remove it.
    if final_word_list[-1] in ["and", "i", "mr"]:
        final_word_list.pop()

    # If the first word of the sentence is "and", remove it.
    if final_word_list[0] in ["and", "him"]:
        final_word_list.pop()

    print(' '.join(final_word_list))

    return final_word_list

def convert_word_list_to_string(final_word_list):
    return ' '.join(final_word_list)


generate_text("bleak-house.txt", 4, 5)
