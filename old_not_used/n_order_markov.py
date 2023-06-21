import random
from colorama import init, Fore, Style
from log_config import configure_logger
from config import Config

# Set up logging
logger = configure_logger(__name__)

# Initialize colorama
init(autoreset=True)


def return_corpus_text(corpus_file_name):
    """
    Read the content of a corpus file and return it as a string.

    Args:
        corpus_file_name (str): The name or path of the corpus file to read.

    Returns:
        str: A string containing the entire content of the corpus file.
    """
    with open(corpus_file_name, 'r') as content_file:
        corpus_as_string = content_file.read()

    return corpus_as_string


def convert_word_list_to_string(final_output_word_list):
    """
    Convert a list of words into a single string joined by spaces.

    Args:
        final_output_word_list (List[str]): A list of individual words.

    Returns:
        str: The combined sentence as a single string.
    """
    return ' '.join(final_output_word_list)


def generate_text(corpus_file_name, prefix_length, output_words_length, seed_words=None):
    """
    Generate random training_corpus_filename based on the input file content, and given prefix and word lengths.

    Args:
      corpus_file_name (str): The path to the input training_corpus_filename file.
      prefix_length (int): The length of the prefix as a tuple for the transition dictionary.
      output_words_length (int): The number of words in the generated training_corpus_filename.

    Returns:
      None

    Prints:
      The generated training_corpus_filename based on the provided parameters.
      :param seed_words:
    """
    # with open(corpus_file_name, 'r') as content_file:
    #     corpus_as_string = content_file.read()

    corpus_as_string = return_corpus_text(corpus_file_name)

    # Preprocessing the training_corpus_filename
    corpus_as_string = corpus_as_string.lower()
    for char in ["!", ".", ",", "@", "&amp;", "?", "-"]:
        corpus_as_string = corpus_as_string.replace(char, " ")
    for char in ['"', '(', ')']:
        corpus_as_string = corpus_as_string.replace(char, "")
    corpus_as_string = corpus_as_string.split()

    # Initialize the transition dictionary.
    # Build a transition dictionary called chain for the given training_corpus_filename represented by corpus_as_string.
    # It uses a Markov chain model, where the keys are sequences of characters (prefixes) and
    # the values are lists of characters that follow the corresponding sequence (successor characters).
    #
    # Initialize the chain by setting a tuple of dot characters (of prefix_length length) as the initial key,
    # and assign a list containing a space as its value. For example, with prefix_length equal to 3,
    # the resulting chain dictionary would look like: {('.', '.', '.'): [' ']}.
    #
    # This code snippet is typically found in implementations of Markov chain training_corpus_filename generation algorithms, where chain
    # serves as a transition dictionary. The key-value pair being set here initializes the starting state for the
    # chain with a predetermined tuple of a specific length (determined by prefix_length).
    chain = {tuple(['.'] * prefix_length): [' ']}

    # Build the transition dictionary by iterating through the training_corpus_filename in corpus_as_string, extracting
    # subsequences of length prefix_length and updating the transition dictionary:
    for i in range(len(corpus_as_string) - prefix_length):

        # Create a tuple seq from the current subsequence of characters. Extracts a substring of length prefix_length
        # from corpus_as_string starting at index i. Then, tuple() converts the resulting substring into a tuple
        # containing individual characters of the substring. Finally, the tuple is assigned to the variable seq.
        seq = tuple(corpus_as_string[i: i + prefix_length])

        # Check if the sequence seq is not in the chain dictionary yet.
        if seq not in chain:
            # If it's not, create a new empty list as the value for the key seq.
            chain[seq] = []

        # Append a character to the list of characters associated with this sequence.
        # The character is the one after the end of the sequence in the corpus_as_string
        chain[seq].append(corpus_as_string[i + prefix_length] if i + prefix_length < len(corpus_as_string) else '.')

    # Generate the training_corpus_filename
    # start_seq is a tuple that must be the length of the markov order.
    # For example, if the markov order is 2, start_seq must be a tuple of length 2.
    # Start_seq is used to initialize the Markov chain with a starting state.
    # start_seq = ('was', 'looking')

    start_seq = None

    # If seed_words was provided by the user, use it to initialize the start_seq.
    # Otherwise, initialize start_seq randomly from words in the Markov chain.
    if seed_words is not None:

        start_seq = tuple(seed_words.split())

    else:

        start_seq = random.choice(list(chain.keys()))

    output_word_list = list(start_seq)
    current_seq = start_seq

    # This loop generates a sequence of words using a Markov chain, where chain is a dictionary
    # representing the transitions between words. Loop output_words_length times
    for i in range(output_words_length):

        try:
            # Choose the next word randomly from possible words associated with current_seq
            next_word = random.choice(chain[current_seq])

        except KeyError:

            # Use the VERBOSE and QUIET flags from the Config class
            if Config.VERBOSE:
                not_found_message = (
                    f"The exact seed word sequence {Fore.RED}"
                    f"'{seed_words}'"
                    f"{Style.RESET_ALL} was not found in the original corpus."
                )

                logger.warning(f"{not_found_message}")

            # elif Config.QUIET:
            #     print("Logging is disabled.")

            current_seq = random.choice(list(chain.keys()))
            next_word = random.choice(chain[current_seq])

        # Update current_seq by adding next_word, removing the first word and converting back to tuple
        current_seq = tuple((list(current_seq) + [next_word])[1:])

        # Add the chosen next_word to output_word_list which stores the full sequence of generated words
        output_word_list.append(next_word)

    # If the last word of the sentence is "and", remove it.
    if output_word_list[-1] in ["and", "i", "mr"]:
        output_word_list.pop()

    # If the first word of the sentence is "and", remove it.
    if output_word_list[0] in ["and", "him"]:
        output_word_list.pop()

    # print(' '.join(output_word_list))

    return output_word_list
