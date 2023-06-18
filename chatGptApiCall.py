import json
import os
import time
import requests
from colorama import init, Fore, Style
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import JsonLexer
from config import Config
from log_config import configure_logger
from pdf_utilities import convert_pdf_to_text_file
from similarity_check import check_similarity
from text_utilities import TextGenerator

# Create an instance of TextGenerator
text_generator = TextGenerator()

# Configure the logger
logger = configure_logger(__name__)

# Initialize colorama
init(autoreset=True)


def call_openai_api(max_tokens, input_file_name=None, raw_markov=False, similarity_check=False, seed_words=None):

    # If the user specified a training corpus, use that. Otherwise, use the default.
    try:
        if input_file_name is not None:

            # If the user specified a PDF file, extract the text from it.
            if input_file_name.lower().endswith('.pdf'):

                # Use the VERBOSE and QUIET flags from the Config class
                if Config.VERBOSE:
                    print(f"{Fore.GREEN}[+] Extracting text from '{input_file_name}'{Style.RESET_ALL}")

                # Extract the text from the PDF file.
                input_file_name = convert_pdf_to_text_file(input_file_name)

            # Otherwise, use the user-specified .txt file.
            elif input_file_name.lower().endswith('.txt'):

                # training_corpus = input_file_name
                pass

        else:

            # If the user did not specify a training corpus, use the default.
            input_file_name = Config.TRAINING_CORPUS

    except FileNotFoundError:
        print(f"File not found: '{input_file_name}'")
        exit(1)

    except IOError as e:
        print(f"IOError occurred while reading the file '{input_file_name}': {e}")
        exit(1)

    # Use the VERBOSE and QUIET flags from the Config class
    if Config.VERBOSE:
        print(f"{Fore.GREEN}[+] Using training corpus: '{input_file_name}'{Style.RESET_ALL}")

    raw_markov_result_string = text_generator.generate_text(
        input_file_name, Config.MARKOV_ORDER, Config.RESULT_LENGTH, seed_words)

    # Convert the word list to a string
    sentence = text_generator.convert_word_list_to_string(raw_markov_result_string)

    # Prepare the API request
    data, headers = setup_api_request(max_tokens, sentence)

    print_verbose_api_request(data) if Config.VERBOSE else None

    make_api_request(input_file_name, data, headers, raw_markov, sentence, similarity_check)


def make_api_request(training_corpus, data, headers, raw_markov, sentence, similarity_check):
    """
    Sends a POST request to the OpenAI API, processes the response and prints various outputs and analysis.

    Args:
    training_corpus (list): A corpus used for training.
    data (dict): The request payload containing prompt and other parameters.
    headers (dict): The request headers containing API key.
    raw_markov (bool): If True, prints raw Markov chain generated input.
    sentence (str): The input sentence on which completion will be performed.
    similarity_check (bool): If True, performs and prints similarity analysis of the output with the given corpus.

    Response JSON structure:
    {
        "choices": [
            {
                "text": "<corrected_sentence>",
                ...
            },
            ...
        ],
        ...
    }

    """
    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    if response.status_code == 200:

        corrected_sentences_list = []
        corrected_sentence = ""

        # Loop through and grab each response if Config.NUM_OF_RESPONSES > 1
        if Config.NUM_OF_RESPONSES > 1:
            for i in range(Config.NUM_OF_RESPONSES):
                corrected_sentences_list.append(response.json().get("choices", [{}])[i].get("text", "").strip())

                corrected_sentence = corrected_sentence + corrected_sentences_list[i] + "\n\n"

        else:

            corrected_sentence = response.json().get("choices", [{}])[0].get("text", "").strip()

        print_similarity_check(training_corpus, corrected_sentence, similarity_check)

        print_corrected_sentence(corrected_sentence, raw_markov, response, sentence)
    else:

        if response.status_code == 429:
            logger.error("Error: Too many requests. Please try again later.")

        logger.error(f"Error: API call failed with status code {response.status_code}.")
        logger.error(f"Response: {response.text}")


def print_corrected_sentence(corrected_sentence, raw_markov, response, sentence):
    if corrected_sentence:

        if raw_markov:
            print(f"[{Fore.YELLOW}RAW MARKOV{Style.RESET_ALL}]\n'{sentence}'\n")

        # TODO: Strip off surrounding quotes if present. They are intermittently present in the response

        if Config.VERBOSE:
            print(f"[{Fore.YELLOW}OPENAI API RESPONSE{Style.RESET_ALL}]")

            # Convert the Python object to a formatted JSON string
            pretty_json_str = json.dumps(response.json(), default=str, indent=4, sort_keys=True)

            # Colorize the JSON string
            colored_json_str = highlight(pretty_json_str, JsonLexer(), TerminalFormatter())

            # Print the colored JSON string
            print(colored_json_str)

        print(f"{Fore.LIGHTGREEN_EX}{corrected_sentence}{Fore.RESET}")

    else:

        logger.error("Error: Could not extract the corrected sentence.")


def print_similarity_check(TRAINING_CORPUS, corrected_sentence, similarity_check):
    if similarity_check:

        # TODO: How to pass reference without calling this again?
        input_text = text_generator.return_corpus_text(TRAINING_CORPUS)
        output_text = corrected_sentence

        highest_similarity_score, average_similarity_score, too_similar_bool, list_overly_similar_phrases = check_similarity(
            input_text, output_text, Config.SIMILARITY_WINDOW, Config.SIMILARITY_THRESHOLD)

        print(f"[{Fore.YELLOW}SIMILARITY ANALYSIS{Style.RESET_ALL}]")
        print(f"    Window size: {Fore.LIGHTCYAN_EX}{Config.SIMILARITY_WINDOW}{Style.RESET_ALL} words")
        print(f"    Similarity threshold: {Fore.LIGHTCYAN_EX}{Config.SIMILARITY_THRESHOLD}{Style.RESET_ALL}")

        if not too_similar_bool:
            print(f"    Average similarity score: {Fore.GREEN}{average_similarity_score:.2f}{Style.RESET_ALL}")
            print(f"    Highest similarity score: {Fore.GREEN}{highest_similarity_score:.2f}{Style.RESET_ALL}")

        if too_similar_bool:

            print(
                f"    Average exceeding similarity score: {Fore.RED}{average_similarity_score:.2f}{Style.RESET_ALL}")
            print(
                f"    Highest exceeding similarity score: {Fore.RED}{highest_similarity_score:.2f}{Style.RESET_ALL}")

            # Create a string with list elements on separate lines, indented by four spaces
            formatted_list = '\n        '.join(list_overly_similar_phrases)

            print(
                f"    Output text is too similar to these phrases:\n        {Fore.RED}{formatted_list}{Style.RESET_ALL}")

        else:

            print(f"    {Fore.GREEN}Output text is adequately dissimilar.{Style.RESET_ALL}")

        # Sleep for a second to give the API call time to finish
        # so that this log message doesn't print below the final output
        time.sleep(1)


def print_verbose_api_request(data):
    print("[" + Fore.YELLOW + "OPENAI API REQUEST" + Style.RESET_ALL + "]")
    # Convert the Python object to a formatted JSON string
    pretty_json_str = json.dumps(data, indent=4, sort_keys=True)
    # Colorize the JSON string
    colored_json_str = highlight(pretty_json_str, JsonLexer(), TerminalFormatter())
    # Print the colored JSON string
    print(colored_json_str)


def setup_api_request(max_tokens, sentence):
    """
    Prepare data and headers for calling the OpenAI GPT API with a specific prompt.

    Args:
        max_tokens (int): Maximum number of tokens to include in the model's response.
        sentence (str): The input sentence to be processed by the API.

    Returns:
        tuple: A tuple containing two dictionaries:
               1. data - Dictionary with parameters to be sent to the GPT API.
               2. headers - Dictionary with authorization information needed to make the API request.
    """
    api_key = os.environ["GPT_API_KEY"]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "text-davinci-003",
        "prompt": "The following sentence may be missing something: \"" + sentence + "\". "
                                                                                     "Please make the sentence make more sense"
                                                                                     "And don't return anything but a single sentence. I only want to see one version of the sentence.",
        "temperature": Config.TEMPERATURE,
        "max_tokens": max_tokens,
        "n": Config.NUM_OF_RESPONSES,
    }
    return data, headers
