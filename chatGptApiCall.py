import os
import requests

api_key = os.environ["GPT_API_KEY"]
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

data = {
    "model": "text-davinci-003",
    "prompt": "The following sentence may be missing something: \"addressing mr george as general she gave him her\". "
              "Please make the sentence make more sense. Please make the language sound even more 18th century in "
              "style. And don't return anything but the corrected sentence.",
    "temperature": 0.7,
    "max_tokens": 50,
    "n": 1,
}

response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)

# corrected_sentence = response.json()["choices"][0]["text"].strip()

if response.status_code == 200:
    corrected_sentence = response.json().get("choices", [{}])[0].get("text", "").strip()
    if corrected_sentence:
        print(corrected_sentence)
    else:
        print("Error: Could not extract the corrected sentence.")
else:
    print(f"Error: API call failed with status code {response.status_code}. Response: {response.text}")

# print(corrected_sentence)

