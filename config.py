#  This file contains the configuration and default values for the mimic.py application.
# It is used to set the various options for the application.
#
# The configuration options are set in the Config class.
class Config:
    VERBOSE = False
    QUIET = False

    # The training_corpus_filename to use for training the Markov model.
    TRAINING_CORPUS = "Training_Corpora/heartOfDarkness.txt"

    # TODO: Create a command line option to specify the Markov order
    # Which order of Markov model, or how many words to look backwards when predicting the next word. Generally,
    # higher-order Markov models capture more context, leading to more coherent and contextually accurate generated
    # sequences. For second order Markov set this to 2. Any higher and results can approach verbatim excerpts. Any lower
    # and it becomes less coherent.
    #
    # A note about "overfitting". Overfitting in this context means that the Markov model may learn the training
    # corpus too well, resulting in output training_corpus_filename that closely resembles or repeats sequences directly from the
    # training data. This can be an issue because the goal is to generate diverse and creative training_corpus_filename based on the
    # patterns learned from the training data, rather than simply reproducing the training data. In other words,
    # an overfitted model will have low generalization capability, meaning it performs well on the training data but
    # poorly on new, previously unseen data. Lower order models are less susceptible to overfitting since they
    # capture less context, making it more challenging for them to reproduce long, verbatim quotes from the training
    # corpus. However, higher order models, if not trained with enough data, can easily capture very specific
    # sequences from the training data and reproduce them in the generated training_corpus_filename. That's why it's essential to strike
    # a balance between context capture and avoiding overfitting.
    MARKOV_ORDER = 2

    # Set how long of a sentence or paragraph you want in the resulting training_corpus_filename.
    RESULT_LENGTH = 30

    # Adjust the temperature with --temp or --temperature. Set how creative or determinative you want ChatGPT to be
    # when cleaning up the sentence. The "temperature" parameter Set a float between 0 and 2. Higher values like 0.8
    # will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    TEMPERATURE = 0.7

    # Set the maximum number of tokens to generate in the ChatGPT API response.
    # max_tokens is an integer, is optional, and defaults to 16.
    # A helpful rule of thumb is that one token generally corresponds to ~4 characters of training_corpus_filename for common
    # English training_corpus_filename. This translates to roughly ¾ of a word (so 100 tokens ~= 75 words).
    # If you set this too low the resulting training_corpus_filename will be truncated accordingly.
    MAX_TOKENS = 50

    # The "n" parameter in the API call to ChatGPT is used to specify the number of different responses you want the
    # model to generate. Setting "n" to 1 means that only one version of the sentence will be returned.
    NUM_OF_RESPONSES = 1

    # Within each similarity window, set the maximum allowable similarity between the generated training_corpus_filename and the original
    # training_corpus_filename. This is used to prevent the model from generating training_corpus_filename that is too similar to the original training_corpus_filename.
    # This is a float between 0 and 1.
    SIMILARITY_THRESHOLD = 0.35

    # Set the window size (as the number of words) for the similarity check.
    # This is used to prevent the model from generating training_corpus_filename that is too similar to the original training_corpus_filename.
    # This is an integer.
    SIMILARITY_WINDOW = 5
