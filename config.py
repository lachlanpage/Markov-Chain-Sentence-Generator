#  This file contains the configuration and default values for the mimic.py application.
# It is used to set the various options for the application.
#
# The configuration options are set in the Config class.
class Config:
    VERBOSE = False
    QUIET = False

    # The text to use for training the Markov model.
    TRAINING_CORPUS = "heartOfDarkness.txt"

    # TODO: Create a command line option to specify the Markov order
    # Which order of Markov model, or how many words to look backwards when predicting the next word. Generally,
    # higher-order Markov models capture more context, leading to more coherent and contextually accurate generated
    # sequences. For second order Markov set this to 2. Any higher and results can approach verbatim excerpts. Any lower
    # and it becomes less coherent.
    MARKOV_ORDER = 2

    # Set how long of a sentence or paragraph you want in the resulting text.
    RESULT_LENGTH = 30

    # TODO: Create a command line option to specify the temperature
    # Set how creative or determinative you want ChatGPT to be when cleaning up the sentence. The "temperature" parameter
    # Set a float between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2
    # will make it more focused and deterministic.
    TEMPERATURE = 0.7

    # Set the maximum number of tokens to generate in the ChatGPT API response.
    # max_tokens is an integer, is optional, and defaults to 16.
    # A helpful rule of thumb is that one token generally corresponds to ~4 characters of text for common
    # English text. This translates to roughly ¾ of a word (so 100 tokens ~= 75 words).
    # If you set this too low the resulting text will be truncated accordingly.
    MAX_TOKENS = 50

    # TODO: Create a command line option to specify the number of responses
    # TODO: When this is > 1, increase the temperature parameter above to get more creative responses.
    # The "n" parameter in the API call to ChatGPT is used to specify the number of different responses you want the
    # model to generate. Setting "n" to 1 means that only one version of the sentence will be returned.
    NUM_OF_RESPONSES = 2

    # Within each similarity window, set the maximum allowable similarity between the generated text and the original
    # text. This is used to prevent the model from generating text that is too similar to the original text.
    # This is a float between 0 and 1.
    SIMILARITY_THRESHOLD = 0.35

    # Set the window size (as the number of words) for the similarity check.
    # This is used to prevent the model from generating text that is too similar to the original text.
    # This is an integer.
    SIMILARITY_WINDOW = 5