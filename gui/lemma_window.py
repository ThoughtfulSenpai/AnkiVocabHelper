import spacy
from spacy.lang.xx import MultiLanguage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor

class LemmaWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Lemmatise wordlist")
        self.setGeometry(100, 100, 400, 200)
        self.main_window = main_window  # Reference to the Main Window

        # Create a layout
        layout = QVBoxLayout()

        # Add a label as an example content
        label = QLabel("Select language to lemmatise the words in the wordlist")
        layout.addWidget(label)

        # Create a ComboBox for language selection
        self.language_combo = QComboBox()
        self.language_combo.addItem("English")  # Add language options here
        self.language_combo.addItem("Spanish")
        self.language_combo.addItem("French")
        # Add more languages as needed
        layout.addWidget(self.language_combo)

        # Create a button to trigger lemmatization
        self.lemmatize_button = QPushButton("Lemmatize")
        self.lemmatize_button.clicked.connect(self.lemmatize_words)
        layout.addWidget(self.lemmatize_button)

        # Set the layout for the window
        self.setLayout(layout)

    def lemmatize_words(self):
        selected_language = self.language_combo.currentText()

        # Check if language is supported
        if selected_language == "English":
            nlp = spacy.load("en_core_web_sm")
        elif selected_language == "Spanish":
            nlp = spacy.load("es_core_news_sm")
        elif selected_language == "French":
            nlp = spacy.load("fr_core_news_sm")
        else:
            return  # Language not supported

        # Get the words from the Main Window's table
        words = [self.main_window.table.item(row, 0).text() for row in range(self.main_window.table.rowCount())]

        # Lemmatize the words using SpaCy
        lemmatized_words = [token.lemma_ for doc in nlp.pipe(words) for token in doc]

        # Update the Main Window's table with lemmatized words
        for row, lemma in enumerate(lemmatized_words):
            item = self.main_window.table.item(row, 0)
            if item:
                item.setText(lemma)

        # Scroll to the top of the table to see the results
        self.main_window.table.verticalScrollBar().setValue(0)
