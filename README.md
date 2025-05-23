# Anki Flashcard Generator

This app automates the generation of flashcards in your Anki app, including audio in US English and Spanish translations, from a given PDF or CSV file containing the original English sentences.

## Project Structure

```
pdf-to-csv-translator
├── src
│   ├── main.py          # Entry point of the application
|   └── pdf_reader.py    # Module for reading phrases from PDF
│   ├── translator.py    # Module for translating phrases to Spanish
│   ├── csv_reader.py    # Module for writing phrases to CSV
│   └── utils
│          └── __init__.py  # Utility functions and constants
│
|
├── requirements.txt      # Project dependencies
├── .gitignore            # Files and directories to ignore by Git
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd anki-flashcard-generator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install `tkinter` (Ubuntu/Debian):

   ```
   sudo apt-get install python3-tk
   ```


## Usage

1. Launch your Anki app.

2. Run this app from a terminal:
   ```
   python src/main.py
   ```

3. Attach the file in PDF or CSV format with the sentences in English.

4. Wait a few minutes and you'll find the new cards in your Anki app.


## Author

Diana C. Rojas. R.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.
