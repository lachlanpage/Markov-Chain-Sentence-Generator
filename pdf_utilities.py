import PyPDF4
from colorama import Fore, Style


def extract_pdf_text(pdf_file_path):
    """
    Extracts text from a given PDF file and returns it as a single string.

    Args:
        pdf_file_path (str): The path of the PDF file to extract text from.

    Returns:
        str: The extracted text from the PDF file as a single string.

    Raises:
        Exception: Any exceptions raised during PDF file opening or text extraction will propagate.
    """
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF4.PdfFileReader(pdf_file)
        pdf_text = []

        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            pdf_text.append(page.extractText())

    return "".join(pdf_text)



def convert_pdf_to_text_file(pdf_file_path):
    """
    Extracts text from a given PDF file, saves the extracted text to a new text file,
    and returns the path to the newly created text file.

    Args:
        pdf_file_path (str): The path of the PDF file to be converted to text.

    Returns:
        str: The path of the new text file containing the extracted text from the PDF.

    Raises:
        Exception: Any exceptions raised during text extraction or file writing will propagate.
    """
    # Save the text to a file with the same name as the PDF file, but with a .txt extension.
    text_file_path = pdf_file_path.replace('.pdf', '.txt')

    with open(text_file_path, 'w', encoding='utf-8', ) as text_file:

        text_file.write(extract_pdf_text(pdf_file_path))

        print(f"{Fore.GREEN}[+] Saved the training corpus to '{text_file_path}'{Style.RESET_ALL}.")

    return text_file_path