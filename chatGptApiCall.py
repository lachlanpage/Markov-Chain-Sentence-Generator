import os
import requests

import config
from n_order_markov import generate_text
from n_order_markov import convert_word_list_to_string
from config import TRAINING_CORPUS, MARKOV_ORDER, RESULT_LENGTH, TEMPERATURE, MAX_TOKENS, NUM_OF_RESPONSES

def call_openai_api(input_file=None, raw_markov=False):


    if input_file is not None :
        TRAINING_CORPUS = input_file
    else:
        TRAINING_CORPUS = config.TRAINING_CORPUS


    final_word_list = generate_text(TRAINING_CORPUS, MARKOV_ORDER, RESULT_LENGTH)
    # Convert the word list to a string
    sentence = convert_word_list_to_string(final_word_list)
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
        if corrected_sentence:

            if raw_markov:
                # TODO: Create a command line boolean option to print the original Markov generated text
                print(sentence)

            # TODO: Strip off surrounding quotes if present. They are intermittently present in the response
            print(corrected_sentence)

        else:
            print("Error: Could not extract the corrected sentence.")
    else:
        print(f"Error: API call failed with status code {response.status_code}. Response: {response.text}")

