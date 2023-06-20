import re
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)


def clean_up_text(text):
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


#  Get the search query from the user
search_query = input("Enter the search query: ")

# Replace spaces with underscores and use lower case
file_name = search_query.replace(' ', '_').lower()

# Add the "wikipedia_" prefix and ".txt" extension
file_name = f"Training_Corpora/wikipedia_{file_name}.txt"

# TODO: Make a command line option to specify the language of the search query
# Set the language to English
wikipedia.set_lang("en")

# Create a variable to store the Wikipedia page object
page = None

try:
    # Send the search query to the Wikipedia API
    page = wikipedia.page(search_query)

except DisambiguationError as de:

    print(f"{Fore.RED}[-] Disambiguation error: multiple pages match the query '{search_query}'. "
          f"Suggestions: {de.options}{Style.RESET_ALL}")
    exit(1)

except PageError:

    print(f"{Fore.RED}[-] Page error: no Wikipedia page found for the query '{search_query}'{Style.RESET_ALL}")
    exit(1)

except Exception as e:
    print(f"{Fore.RED}[-] An unexpected error occurred: {e}{Style.RESET_ALL}")
    exit(1)

# Clean up the content of the Wikipedia page
cleaned_content = clean_up_text(page.content)

try:
    # Write the content to a file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    print(f"{Fore.GREEN}[+] Wrote the Wikipedia page content to '{file_name}'.{Style.RESET_ALL}")

except IOError as e:
    print(f"{Fore.RED}[-] IOError occurred while writing to the file '{file_name}': {e}{Style.RESET_ALL}")
    exit(1)
