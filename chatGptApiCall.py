import os
import requests
import logging
import coloredlogs
import config
from n_order_markov import generate_text
from n_order_markov import convert_word_list_to_string
from n_order_markov import return_corpus_text
from similarity_check import check_similarity
from config import TRAINING_CORPUS, MARKOV_ORDER, RESULT_LENGTH, TEMPERATURE, MAX_TOKENS, NUM_OF_RESPONSES
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# print(f"{Fore.RED}This is red text.")
# print(f"{Fore.GREEN}This is green text.")
# print(f"{Fore.YELLOW}This is yellow text.")
# print(f"{Fore.CYAN}This is cyan text.")
# print(f"{Fore.MAGENTA}This is magenta text.")
# print(f"{Fore.BLUE}This is blue text.")

# Set up colored logging
logger = logging.getLogger(__name__)
fmt = "[%(levelname)s] %(message)s"
coloredlogs.install(level='DEBUG', logger=logger, fmt=fmt)

# logger.error("This is an error message in red color.")
# logger.warning("This is a warning message in yellow color.")
# logger.info("This is an info message in green color.")
# logger.debug("This is a debug message in white color.")

def call_openai_api(input_file=None, raw_markov=False, similarity_check=False, seed_words=None):

    if input_file is not None :
        TRAINING_CORPUS = input_file
    else:
        TRAINING_CORPUS = config.TRAINING_CORPUS

    raw_markov_result_string = generate_text(TRAINING_CORPUS, MARKOV_ORDER, RESULT_LENGTH, seed_words)
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
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "n": NUM_OF_RESPONSES,
    }
    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    if response.status_code == 200:
        corrected_sentence = response.json().get("choices", [{}])[0].get("text", "").strip()

        if similarity_check:

            # TODO: How to pass reference without calling this again?
            input_text = return_corpus_text(TRAINING_CORPUS)
            output_text = corrected_sentence
            window_size = 5
            similarity_threshold = 0.35



            too_similar = check_similarity(input_text, output_text, window_size, similarity_threshold)
            # print("Is the generated text too similar?", too_similar)
            logger.info("Is the generated text too similar? {}".format(too_similar) )

            # Replace input_text and output_text with your actual texts. Adjust window_size and
            # similarity_threshold as needed. This code checks if there's any part of the input
            # text with a similarity ratio above the defined threshold when compared to the
            # output text. The sliding window size determines how many words you want to consider
            # at once while scanning the entire corpus.



        if corrected_sentence:

            if raw_markov:

                print("[RAW MARKOV] '{}'".format(sentence) )

            # TODO: Strip off surrounding quotes if present. They are intermittently present in the response
            print("[MIMICKED QUOTE] '{}'".format(corrected_sentence) )



        else:
            # print("Error: Could not extract the corrected sentence.")
            logger.error("Error: Could not extract the corrected sentence.")
    else:
        # print(f"Error: API call failed with status code {response.status_code}. Response: {response.text}")
        logger.error(f"Error: API call failed with status code {response.status_code}. Response: {response.text}")
