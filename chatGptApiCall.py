import json
import os
import time
import requests
from n_order_markov import generate_text
from n_order_markov import convert_word_list_to_string
from n_order_markov import return_corpus_text
from similarity_check import check_similarity
from colorama import init, Fore, Style
from log_config import configure_logger
from config import Config
from pprint import pprint
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

# Configure the logger
logger = configure_logger(__name__)

# Initialize colorama
init(autoreset=True)


def call_openai_api(max_tokens, input_file=None, raw_markov=False, similarity_check=False, seed_words=None):

    # If the user specified a training corpus, use that. Otherwise, use the default.
    if input_file is not None :

        TRAINING_CORPUS = input_file

    else:

        TRAINING_CORPUS = Config.TRAINING_CORPUS

    raw_markov_result_string = generate_text(TRAINING_CORPUS, Config.MARKOV_ORDER, Config.RESULT_LENGTH, seed_words)

    # Convert the word list to a string
    sentence = convert_word_list_to_string(raw_markov_result_string)
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

    if Config.VERBOSE:

        print("[" + Fore.YELLOW + "OPENAI API REQUEST" + Style.RESET_ALL + "]")

        # Convert the Python object to a formatted JSON string
        pretty_json_str = json.dumps(data, indent=4, sort_keys=True)

        # Colorize the JSON string
        colored_json_str = highlight(pretty_json_str, JsonLexer(), TerminalFormatter())

        # Print the colored JSON string
        print(colored_json_str)

    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    if response.status_code == 200:
        corrected_sentence = response.json().get("choices", [{}])[0].get("text", "").strip()

        if similarity_check:

            # TODO: How to pass reference without calling this again?
            input_text = return_corpus_text(TRAINING_CORPUS)
            output_text = corrected_sentence
            window_size = 5
            similarity_threshold = 0.35

            similarity_score, too_similar_bool = check_similarity(input_text, output_text, window_size, similarity_threshold)

            print(f"[{Fore.YELLOW}SIMILARITY ANALYSIS{Style.RESET_ALL}]")
            print(f"Window size: {window_size} words")
            print(f"Similarity threshold: {similarity_threshold}")
            print(f"Similarity score: {similarity_score:.2f}")

            if too_similar_bool == True:

                print(f"{Fore.RED}Output text is too similar.{Style.RESET_ALL}")

            else:

                print(f"{Fore.GREEN}Output text is adequately dissimilar.{Style.RESET_ALL}")

            # Sleep for a second to give the API call time to finish
            # so that this log message doesn't print below the final output
            time.sleep(1)

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
            # print("Error: Could not extract the corrected sentence.")
            logger.error("Error: Could not extract the corrected sentence.")
    else:
        # print(f"Error: API call failed with status code {response.status_code}. Response: {response.text}")
        logger.error(f"Error: API call failed with status code {response.status_code}. Response: {response.text}")
