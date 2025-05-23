import re

import pdfplumber


class PDFReader:
    def __init__(self, pdf_path, filter_from="", fielter_to=""):
        self.pdf_path = pdf_path
        self.filter_from = filter_from
        self.fielter_to = fielter_to

    def _filter_text(self, text):

        match = re.search(f"{self.filter_from}(.*?){self.fielter_to}", text, re.DOTALL)
        if match:
            filtered_text = match.group(1)
            return filtered_text.strip()

        return ""

    def read_phrases(self):
        text = ""
        with pdfplumber.open(self.pdf_path) as reader:
            for page in reader.pages:
                page_text = page.extract_text()
                # add a line break at the end between pages to avoid
                # phrases getting merged
                if text and text[-1] != "\n" and page_text[0] != "\n":
                    page_text = "\n" + page_text
                text += page_text

        if self.filter_from and self.fielter_to:
            text = self._filter_text(text)

        if not text:
            return []

        phrases = []
        for phrase in text.split("\n"):
            if phrase:
                phrase = phrase.strip()
                last_phrase = phrases[-1] if phrases else ""
                if last_phrase and last_phrase[-1] not in (".", "!"):
                    phrases[-1] += " " + phrase
                    continue
                phrases.append(phrase)
        return phrases
