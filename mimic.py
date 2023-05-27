import argparse
from chatGptApiCall import call_openai_api

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="A simple command line tool")

    # Add arguments
    # parser.add_argument("input_file", help="Path to the input file")
    # Add the optional input file argument
    parser.add_argument("-i", "--input-file", help="Path to the input file", default=None)
    parser.add_argument("-o", "--output", default="output.txt", help="Path to the output file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    # Parse arguments
    args = parser.parse_args()

    # Print the results
    # print("Input file:", args.input_file)
    # print("Output file:", args.output)
    # print("Verbose mode:", args.verbose)

    if args.input_file is None :
        call_openai_api()
    else:
        call_openai_api(args.input_file)

if __name__ == "__main__":
    main()