import re
import wikipedia
from wikipedia import WikipediaPage
from wikipedia.exceptions import DisambiguationError, PageError


def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove references, e.g., [1], [2], etc.
    text = re.sub(r'\[\d+\]', '', text)

    # The regex pattern ^===.*$ matches any line that starts with '===' and replaces it with an empty string. The
    # flags=re.MULTILINE parameter ensures the regex operates on a per-line basis.
    text = re.sub(r'^={2,3}.*$', '', text, flags=re.MULTILINE)
    # match any line containing only whitespace or being completely empty and replace it with an empty string.
    text = re.sub(r'^\s*$', '', text, flags=re.MULTILINE)

    return text


# TODO: Replace this with the actual user input
# search_query = "Watergate scandal"  # Replace this with the actual user input
search_query = input("Enter the search query: ")

# Replace spaces with underscores and use lower case
file_name = search_query.replace(' ', '_').lower()

# Add the "wikipedia_" prefix and ".txt" extension
file_name = f"Training_Corpora/wikipedia_{file_name}.txt"

wikipedia.set_lang("en")

page = None

try:
    page = wikipedia.page(search_query)
except DisambiguationError as de:
    print(f"Disambiguation error: multiple pages match the query '{search_query}'. Suggestions: {de.options}")
    exit(1)
except PageError:
    print(f"Page error: no Wikipedia page found for the query '{search_query}'")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)

raw_content = page.content
clean_content = clean_text(raw_content)

# print(clean_content)

with open(file_name, 'w', encoding='utf-8') as file:
    file.write(clean_content)
