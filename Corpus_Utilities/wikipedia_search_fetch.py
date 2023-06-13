import re
import wikipedia

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
search_query = "Watergate scandal"  # Replace this with the actual user input

# Replace spaces with underscores and use lower case
file_name = search_query.replace(' ', '_').lower()

# Add the "wikipedia_" prefix and ".txt" extension
file_name = f"wikipedia_{file_name}.txt"

wikipedia.set_lang("en")
page = wikipedia.page(search_query)
raw_content = page.content
clean_content = clean_text(raw_content)

# print(clean_content)

with open(file_name, 'w', encoding='utf-8') as file:
    file.write(clean_content)