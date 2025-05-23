import csv


class CSVReader:

    def __init__(self, file_path=None):
        self.file_path = file_path

    def read_phrases(self):
        rows = []
        with open(self.file_path, mode="r", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row:
                    rows.append(row[0])
        return rows
