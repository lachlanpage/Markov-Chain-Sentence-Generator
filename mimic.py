import argparse
import math

from chatGptApiCall import call_openai_api
from log_config import configure_logger
from config import Config


def parse_args():

    # Create the argument parser
    parser = argparse.ArgumentParser(description="A command line tool to generate random phrases that imitate a literary style based on a training text.")

    # Add arguments
    # Add the optional input file argument
    parser.add_argument("-i", "--input-file", help="Path to the input file (optional)", default=Config.TRAINING_CORPUS)
    parser.add_argument("-r", "--raw-markov", action="store_true", help="Print the raw Markov result (optional)")
    parser.add_argument("-c", "--similarity-check", action="store_true", help="Quantify how similar the output is to the original text (optional)")
    parser.add_argument("-s", "--seed-words", help="Word(s) to seed the Markov search. If not found it will be added to the resulting output. (optional)", default=None)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-q", "--quiet", action="store_true", help="Disable logging completely")
    parser.add_argument("-l", "--length", help="Approximate length of the output (optional)", default=Config.RESULT_LENGTH)
    parser.add_argument("-m", "--max-tokens", help="Maximum number of tokens to generate. If not specified, "
                                                   "it increases automatically if you specify length. (optional)",
                                                    default=Config.MAX_TOKENS)
    parser.add_argument("-st", "--similarity-threshold", help="Similarity threshold for the similarity check (optional)",
                                                    default=Config.SIMILARITY_THRESHOLD)
    # TODO:  Add the optional test argument
    # parser.add_argument("-t", "--test", action="store_true", help="Test the API call")

    return parser.parse_args()


def main():

    args = parse_args()

    # Update the config based on the parsed arguments
    Config.VERBOSE = args.verbose
    Config.QUIET = args.quiet
    Config.RESULT_LENGTH = int(args.length)
    # Adjust the max_tokens value based on the length
    # 1 token ~= 0.75 of a word, or about 4 characters
    Config.MAX_TOKENS = int(Config.RESULT_LENGTH * (4 / 3))

    # But if the user specified a max_tokens value, update the config
    if args.max_tokens:
        Config.MAX_TOKENS = int(args.max_tokens)

    # If the user specified a similarity threshold, update the config
    if args.similarity_threshold:
        Config.SIMILARITY_THRESHOLD = float(args.similarity_threshold)

    logger = configure_logger(__name__)

    if args.input_file is None :
        call_openai_api(Config.MAX_TOKENS, None, args.raw_markov, args.similarity_check, args.seed_words)
    else:
        call_openai_api(Config.MAX_TOKENS, args.input_file, args.raw_markov, args.similarity_check, args.seed_words)

if __name__ == "__main__":
    main()