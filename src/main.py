# main.py

import os
from tkinter import filedialog

from environs import Env

from anki_connector import AnkiConnector
from csv_reader import CSVReader
from pdf_reader import PDFReader

env = Env()
env.read_env()


def main():

    origin_file_path = filedialog.askopenfilename(
        title="Select a PDF or CSV file",
        filetypes=[("PDF File", "*.pdf"), ("CSV File", "*.csv")],
    )

    if not origin_file_path:
        print("No file selected. Exiting...")
        return

    phrases = []
    if origin_file_path.endswith(".pdf"):
        start_keyword = env.str("FILTER_PDF_FROM")
        end_keyword = env.str("FILTER_PDF_TO")
        pdf_reader = PDFReader(origin_file_path, start_keyword, end_keyword)
        phrases = pdf_reader.read_phrases()

    elif origin_file_path.endswith(".csv"):
        csv_reader = CSVReader(origin_file_path)
        phrases = csv_reader.read_phrases()

    else:
        print("The selected file is neither a PDF nor a CSV. Exiting...")
        return

    audios_path = env.str("AUDIOS_PATH", "./src/files/audios")
    os.makedirs(audios_path, exist_ok=True)

    deck_name = env.str("DECK_NAME")
    tags = env.str("TAGS")
    tags = tags.split(",") if tags else []
    add_tag_question = env.bool("ADD_TAG_QUESTION")
    anki_connector = AnkiConnector(
        audios_path, deck_name=deck_name, add_tag_question=add_tag_question
    )
    anki_connector.add_cards(phrases, tags=tags)


if __name__ == "__main__":
    main()
