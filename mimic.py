import argparse
from chatGptApiCall import call_openai_api


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="A command line tool to generate random phrases that imitate a literary style based on a training text.")

    # Add arguments
    # parser.add_argument("input_file", help="Path to the input file")
    # Add the optional input file argument
    parser.add_argument("-i", "--input-file", help="Path to the input file (optional)", default=None)
    parser.add_argument("-r", "--raw-markov", action="store_true", help="Print the raw Markov result (optional)")
    parser.add_argument("-c", "--similarity-check", action="store_true", help="Quantify how similar the output is to the original text (optional)")
    parser.add_argument("-s", "--seed-words", help="Word(s) to seed the Markov search. If not found it will be added to the resulting output. (optional)", default=None)
    # parser.add_argument("-o", "--output", default="output.txt", help="Path to the output file")
    # parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    # Parse arguments
    args = parser.parse_args()

    # Print the results
    # print("Input file:", args.input_file)
    # print("Output file:", args.output)
    # print("Verbose mode:", args.verbose)

    if args.input_file is None :
        call_openai_api(None, args.raw_markov, args.similarity_check, args.seed_words)
    else:
        call_openai_api(args.input_file, args.raw_markov, args.similarity_check, args.seed_words)

if __name__ == "__main__":
    main()