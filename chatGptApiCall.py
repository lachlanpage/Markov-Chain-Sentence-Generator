import os
import requests
from n_order_markov import generate_text
from n_order_markov import convert_word_list_to_string

# TODO: Create a command line option to specify the training corpus

def call_openai_api(input_file=None):
    # The text to use for training the Markov model.
    TRAINING_CORPUS = "heartOfDarkness.txt"
    # TODO: Create a command line option to specify the Markov order
    # Which order of Markov model, or how many words to look backwards when predicting the next word. Generally,
    # higher-order Markov models capture more context, leading to more coherent and contextually accurate generated
    # sequences. For second order Markov set this to 2. Any higher and results can approach verbatim excerpts. Any lower
    # and it becomes less coherent.
    # TODO: Create a similarity check. Quantify and filter directly quoted phrases of too many sesquential words because 2 is too close to verbatim sometimes.
    MARKOV_ORDER = 2
    # TODO: Create a command line option to specify the result length
    # Set how long of a sentence or paragraph you want in the resulting text.
    RESULT_LENGTH = 30
    # TODO: Create a command line option to specify the temperature
    # Set how creative or determinative you want ChatGPT to be when cleaning up the sentence. The "temperature" parameter
    # Set a float between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2
    # will make it more focused and deterministic.
    TEMPERATURE = 0.7
    # TODO: Create a command line option to specify the max tokens
    # Set the maximum number of tokens to generate in the ChatGPT API response.
    # max_tokens is an integer, is optional, and defaults to 16.
    # A helpful rule of thumb is that one token generally corresponds to ~4 characters of text for common
    # English text. This translates to roughly ¾ of a word (so 100 tokens ~= 75 words).
    # If you set this too low the resulting text will be truncated accordingly.
    MAX_TOKENS = 50
    # The "n" parameter in the API call to ChatGPT is used to specify the number of different responses you want the
    # model to generate. Setting "n" to 1 means that only one version of the sentence will be returned.
    NUM_OF_RESPONSES = 1

    if input_file is not None :
        TRAINING_CORPUS = input_file


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

            # TODO: Create a command line boolean option to print the original Markov generated text
            print(sentence)

            # TODO: Strip off surrounding quotes if present. They are intermittently present in the response
            print(corrected_sentence)

        else:
            print("Error: Could not extract the corrected sentence.")
    else:
        print(f"Error: API call failed with status code {response.status_code}. Response: {response.text}")

