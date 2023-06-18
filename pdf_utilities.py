import PyPDF4
from colorama import Fore, Style


def extract_pdf_text(pdf_file_path):
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF4.PdfFileReader(pdf_file)
        pdf_text = []

        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            pdf_text.append(page.extractText())

    return "".join(pdf_text)

# TODO: implement the extract_pdf_text function in mimic.py with --input-file

def convert_pdf_to_text_file(pdf_file_path):

    # Save the text to a file with the same name as the PDF file, but with a .txt extension.
    text_file_path = pdf_file_path.replace('.pdf', '.txt')

    with open(text_file_path, 'w', encoding='utf-8', ) as text_file:

        text_file.write(extract_pdf_text(pdf_file_path))

        print(f"{Fore.GREEN}[+] Saved the training corpus to '{text_file_path}'{Style.RESET_ALL}.")

    return text_file_path