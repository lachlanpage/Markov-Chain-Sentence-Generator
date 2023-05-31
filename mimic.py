import argparse
from chatGptApiCall import call_openai_api
from log_config import configure_logger
from config import Config

# Set up colored logging
# logger = configure_logger(__name__)
# Configure logging based on --verbose flag
# logger = configure_logger(__name__, args.verbose)
# import logging
# import coloredlogs
#
# # Set up colored logging
# logger = logging.getLogger(__name__)
# fmt = "[%(levelname)s] %(message)s"
# # Customize field color of INFO level as well (for the [INFO] part)
# coloredlogs.DEFAULT_FIELD_STYLES["levelname"]["info"] = {"color": "white"}
# # Customizing the error level color
# coloredlogs.DEFAULT_LEVEL_STYLES["info"] = {"color": "white"}
# coloredlogs.install(level='DEBUG', logger=logger, fmt=fmt)


def parse_args():

    # Create the argument parser
    parser = argparse.ArgumentParser(description="A command line tool to generate random phrases that imitate a literary style based on a training text.")

    # Add arguments
    # Add the optional input file argument
    parser.add_argument("-i", "--input-file", help="Path to the input file (optional)", default=None)
    parser.add_argument("-r", "--raw-markov", action="store_true", help="Print the raw Markov result (optional)")
    parser.add_argument("-c", "--similarity-check", action="store_true", help="Quantify how similar the output is to the original text (optional)")
    parser.add_argument("-s", "--seed-words", help="Word(s) to seed the Markov search. If not found it will be added to the resulting output. (optional)", default=None)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-q", "--quiet", action="store_true", help="Disable logging completely")

    return parser.parse_args()


def main():
    args = parse_args()

    # Update the config based on the parsed arguments
    Config.VERBOSE = args.verbose
    Config.QUIET = args.quiet

    # Configure logging based on --verbose flag
    # logger = configure_logger(__name__, args.verbose, args.quiet)
    logger = configure_logger(__name__)

    # Test logging levels
    logger.critical("Critical level message")
    logger.error("Error level message")
    logger.warning("Warning level message")
    logger.info("Info level message")
    logger.debug("Debug level message")

    if args.input_file is None :
        call_openai_api(None, args.raw_markov, args.similarity_check, args.seed_words)
    else:
        call_openai_api(args.input_file, args.raw_markov, args.similarity_check, args.seed_words)

if __name__ == "__main__":
    main()