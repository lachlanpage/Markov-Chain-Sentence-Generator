import random
from colorama import init, Fore, Style
from log_config import configure_logger
from config import Config

class TextGenerator:

    # This class is used to generate text from a given corpus file.

    # Initializes the class by configuring a logger with the current module's name
    # and enabling auto-reset for the terminal color output.
    def __init__(self):
        self.logger = configure_logger(__name__)
        init(autoreset=True)

    # This method is used to return the text from a given corpus file.
    def return_corpus_text(self, corpus_file_name):
        with open(corpus_file_name, 'r') as content_file:
            corpus_as_string = content_file.read()
        return corpus_as_string

    #  This method is used to convert the list of words into a string from a given corpus file.
    def convert_word_list_to_string(self, final_output_word_list):
        return ' '.join(final_output_word_list)

    def generate_text(self, corpus_file_name, prefix_length, output_words_length, seed_words=None):

        corpus_as_string = self.return_corpus_text(corpus_file_name)

        corpus_as_string = self.clean_up_corpus_string(corpus_as_string)

        output_word_list = self.markov_algorithm(corpus_as_string, output_words_length, prefix_length, seed_words)

        # TODO: Should this return the output_word_list?
        self.clean_up_markov_output(output_word_list)

        return output_word_list

    def clean_up_markov_output(self, output_word_list):
        # This method is used to clean up the output of the Markov algorithm.

        # Remove words that shouldn't be at the end of a sentence.
        if output_word_list[-1] in ["and", "i", "mr"]:
            output_word_list.pop()

        # Remove words that shouldn't be at the beginning of a sentence.
        if output_word_list[0] in ["and", "him"]:
            output_word_list.pop(0)

    def markov_algorithm(self, corpus_as_string, output_words_length, prefix_length, seed_words):
        # prefix_length determines which order of Markov
        # meaning how many words to look backwards to predict the next word.
        chain = {tuple(['.'] * prefix_length): [' ']}
        for i in range(len(corpus_as_string) - prefix_length):
            seq = tuple(corpus_as_string[i: i + prefix_length])
            if seq not in chain:
                chain[seq] = []
            chain[seq].append(corpus_as_string[i + prefix_length] if i + prefix_length < len(corpus_as_string) else '.')
        start_seq = None
        if seed_words is not None:
            start_seq = tuple(seed_words.split())
        else:
            start_seq = random.choice(list(chain.keys()))
        output_word_list = list(start_seq)
        current_seq = start_seq
        for i in range(output_words_length):
            try:
                next_word = random.choice(chain[current_seq])
            except KeyError:
                if Config.VERBOSE:
                    not_found_message = (
                        f"The exact seed word sequence {Fore.RED}"
                        f"'{seed_words}'"
                        f"{Style.RESET_ALL} was not found in the original corpus."
                    )
                    self.logger.warning(f"{not_found_message}")
                current_seq = random.choice(list(chain.keys()))
                next_word = random.choice(chain[current_seq])

            current_seq = tuple((list(current_seq) + [next_word])[1:])
            output_word_list.append(next_word)
        return output_word_list

    def clean_up_corpus_string(self, corpus_as_string):
        corpus_as_string = corpus_as_string.lower()
        for char in ["!", ".", ",", "@", "&", "?", "-"]:
            corpus_as_string = corpus_as_string.replace(char, " ")
        for char in ['"', '(', ')']:
            corpus_as_string = corpus_as_string.replace(char, "")
        corpus_as_string = corpus_as_string.split()
        return corpus_as_string
