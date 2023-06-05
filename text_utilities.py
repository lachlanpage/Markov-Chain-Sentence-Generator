import random
from colorama import init, Fore, Style
from log_config import configure_logger
from config import Config

class TextGenerator:

    def __init__(self):
        self.logger = configure_logger(__name__)
        init(autoreset=True)

    def return_corpus_text(self, corpus_file_name):
        with open(corpus_file_name, 'r') as content_file:
            corpus_as_string = content_file.read()
        return corpus_as_string

    def convert_word_list_to_string(self, final_output_word_list):
        return ' '.join(final_output_word_list)

    def generate_text(self, corpus_file_name, prefix_length, output_words_length, seed_words=None):
        corpus_as_string = self.return_corpus_text(corpus_file_name)
        corpus_as_string = corpus_as_string.lower()
        for char in ["!", ".", ",", "@", "&", "?", "-"]:
            corpus_as_string = corpus_as_string.replace(char, " ")
        for char in ['"', '(', ')']:
            corpus_as_string = corpus_as_string.replace(char, "")
        corpus_as_string = corpus_as_string.split()

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

        if output_word_list[-1] in ["and", "i", "mr"]:
            output_word_list.pop()

        if output_word_list[0] in ["and", "him"]:
            output_word_list.pop()

        return output_word_list
