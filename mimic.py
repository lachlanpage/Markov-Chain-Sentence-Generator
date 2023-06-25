import argparse

import sentiment_utilities
from chatGptApiCall import call_openai_api
from config import Config
from log_config import configure_logger


def parse_args():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="A command line tool to generate random phrases that imitate a literary style based on a training "
                    "training_corpus_filename.")

    # Add arguments
    # Add the optional input file argument
    parser.add_argument("-i", "--input-file",
                        help="Path to the input file. .txt or .pdf (optional)",
                        default=Config.TRAINING_CORPUS)
    # TODO: Create a command line option to specify a directory containing several related training_corpus_filename files.
    parser.add_argument("-r", "--raw-markov",
                        action="store_true",
                        help="Print the raw Markov result (optional)")
    parser.add_argument("-sc", "--similarity-check",
                        action="store_true",
                        help="Quantify how similar the output is to the original training_corpus_filename (optional)")
    parser.add_argument("-sw", "--seed-words",
                        help="Word(s) to seed the Markov search. "
                             "If not found in the original training_corpus_filename, it will be prepended to the output. (optional)",
                        default=None)
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Enable verbose mode")
    parser.add_argument("-q", "--quiet",
                        action="store_true",
                        help="Disable logging completely")
    parser.add_argument("-l", "--length",
                        help="Approximate length of the output (optional)",
                        default=Config.RESULT_LENGTH)
    parser.add_argument("-m", "--max-tokens",
                        help="Maximum number of tokens to generate. If not specified, "
                             "it increases automatically if you specify length. (optional)",
                        default=Config.MAX_TOKENS)
    parser.add_argument("-st", "--similarity-threshold",
                        help="Floating point similarity threshold for the similarity check (optional)",
                        default=Config.SIMILARITY_THRESHOLD)
    parser.add_argument("-w", "--similarity-window",
                        help="Number of consecutive words in the sliding window used for the similarity check ("
                             "optional)",
                        default=Config.SIMILARITY_WINDOW)
    parser.add_argument("-n", "--number_of_responses",
                        help="Number of responses to generate. Higher number also increases temperature and increases "
                             "likelihood of repetition(optional)",
                        default=Config.NUM_OF_RESPONSES)
    parser.add_argument("-temp", "--temperature", help="Specify the AI temperature (creativity). "
                                                       "Float between 0 and 2.0 (optional)")
    parser.add_argument('--sentiment', action='store_true', help="Perform sentiment analysis on input data.")

    # TODO: Create a command line option to not call the ChatGPT API

    # TODO: Add an optional test argument to test the API call
    # parser.add_argument("-t", "--test", action="store_true", help="Test the API call")

    return parser.parse_args()


def clamp(value, min_value, max_value):
    """
    Clamp a given value between a minimum and maximum value.

    Args:
        value (float): The value to be clamped.
        min_value (float): The lower bound for the clamped value.
        max_value (float): The upper bound for the clamped value.

    Returns:
        float: The clamped value limited to the range [min_value, max_value].
    """
    return max(min(value, max_value), min_value)


def main():
    args = parse_args()

    # Update the config based on the parsed arguments
    Config.VERBOSE = args.verbose
    Config.QUIET = args.quiet
    Config.RESULT_LENGTH = int(args.length)
    # Adjust the max_tokens value based on the length
    # 1 token ~= 0.75 of a word, or about 4 characters
    Config.MAX_TOKENS = int(Config.RESULT_LENGTH * (4 / 3))

    # If the user specified a temperature value, update the config
    if args.temperature:
        Config.TEMPERATURE = float(args.temperature)

    # But if the user specified a max_tokens value, update the config
    if int(args.max_tokens) > Config.RESULT_LENGTH:
        Config.MAX_TOKENS = int(args.max_tokens)

    # If the user specified a similarity threshold, update the config
    if args.similarity_threshold:
        Config.SIMILARITY_THRESHOLD = float(args.similarity_threshold)

    # If the user specified a similarity window, update the config
    if args.similarity_window:
        Config.SIMILARITY_WINDOW = int(args.similarity_window)

    # If the user specified a number of responses, update the config
    if args.number_of_responses:

        Config.NUM_OF_RESPONSES = int(args.number_of_responses)

        # Adjust the temperature value based on the number of responses
        # Higher number also increases temperature and increases likelihood of repetition
        # Config.TEMPERATURE = Config.TEMPERATURE * 1.75

        if Config.NUM_OF_RESPONSES > 1:
            # Increase temperature proportionally to the number of responses or by any custom factor
            Config.TEMPERATURE += Config.NUM_OF_RESPONSES * 0.25

        # Clamp the temperature to be within the range [0, 2]
        Config.TEMPERATURE = clamp(Config.TEMPERATURE, 0, 2)

    configure_logger(__name__)

    if args.input_file is None:

        # If  the user specified a sentiment analysis, update the config and perform sentiment analysis
        if args.sentiment:
            Config.SENTIMENT = True

            # TODO: Fix bug where sentiment analysis always uses the default training_corpus_filename
            sentiment_utilities.analyze_sentiment(Config.TRAINING_CORPUS)

        call_openai_api(Config.MAX_TOKENS, None, args.raw_markov, args.similarity_check, args.seed_words)

    else:
        # If  the user specified a sentiment analysis, update the config and perform sentiment analysis
        if args.sentiment:
            Config.SENTIMENT = True

            sentiment_utilities.analyze_sentiment(args.input_file)

        call_openai_api(Config.MAX_TOKENS, args.input_file, args.raw_markov, args.similarity_check, args.seed_words)

if __name__ == "__main__":
    main()
