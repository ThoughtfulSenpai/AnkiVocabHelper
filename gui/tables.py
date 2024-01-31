import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMessageBox, QListWidget, QDialog, QFormLayout, QComboBox

from window import MainWindow
from db import create_connection, add_language


class TableSelectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select a table")

        self.setStyleSheet("""
            QMainWindow {
                background-color: #282828;
                color: #ffffff;
            }
            QPushButton {
                background-color: #333333;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QLineEdit {
                background-color: #333333;
                color: #ffffff;
            }
            QListWidget {
                background-color: #333333;
                color: #ffffff;
            }
            QTableWidget {
                background-color: #333333;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #ffffff;
            }
            QTableCornerButton::section {
                background-color: #333333;
                border: none;
            }
            QTableView {
                gridline-color: #333333;
            }
        """)

        self.table_list = QListWidget()

        self.table_list.itemDoubleClicked.connect(self.open_table)

        self.new_table_button = QPushButton("New table")
        self.new_table_button.clicked.connect(self.create_new_table)

        layout = QVBoxLayout()
        layout.addWidget(self.table_list)
        layout.addWidget(self.new_table_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_table_list()  # Добавьте эту строку

        self.main_window = None  # Добавьте это поле

    def create_new_table(self):
        dialog = NewTableDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            table_name = dialog.table_name_input.text()

            # Получите полное название языка из language_input
            full_language_name = dialog.language_input.currentText()

            # Получите двухбуквенный код языка из словаря languages
            language_code = dialog.languages[full_language_name]

            # Создайте новую базу данных с указанным именем таблицы
            conn = create_connection(table_name)

            # Добавьте двухбуквенный код языка в базу данных
            add_language(conn, language_code)

            # Добавьте новую таблицу в table_list
            self.update_table_list()

    def update_table_list(self):
        # Clear the table_list
        self.table_list.clear()
        # Get the current working directory
        current_directory = os.getcwd()
        # Load the list of existing tables and add them to table_list
        for file in os.listdir(current_directory):
            if file.endswith(".db"):
                self.table_list.addItem(file[:-3])  # Remove the file

    def open_table(self, item):
        # Получаем имя выбранной таблицы
        table_name = item.text()

        #print(f"Opening table: {table_name}")  # Добавьте эту строку

        # Создаем и показываем MainWindow для выбранной таблицы
        self.main_window = MainWindow(table_name)  # Сохраняем ссылку на MainWindow
        self.main_window.show()

       #print("Table opened")  # Добавьте эту строку

        # Закрываем окно выбора таблицы
        self.close()


class NewTableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("New table")

        self.setStyleSheet("""
            QDialog {
                background-color: #282828;
                color: #ffffff;
            }
            QPushButton {
                background-color: #333333;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QLineEdit {
                background-color: #333333;
                color: #ffffff;
            }
            QComboBox {
                background-color: #333333;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
        """)

        self.table_name_input = QLineEdit()
        self.language_input = QComboBox()

        # Создайте словарь для сопоставления полных названий языков и их двухбуквенных кодов
        self.languages = {
            'Arabic': 'ar',
            'Bengali': 'bn',
            'Bosnian(small)': 'sh',
            'Bulgarian(small)': 'bg',
            'Catalan': 'ca',
            'Chinese': 'zh',
            'Croatian(small)': 'sh',
            'Czech': 'cs',
            'Danish(small)': 'da',
            'Dutch': 'nl',
            'English': 'en',
            'French': 'fr',
            'German': 'de',
            'Greek(small)': 'el',
            'Hebrew': 'he',
            'Hindi(small)': 'hi',
            'Hungerian(small)': 'hu',
            'Icelandic(small)': 'is',
            'Indonesian(small)': 'id',
            'Italian': 'it',
            'Japanese': 'ja',
            'Korean(small)': 'ko',
            'Latvian(small)': 'lv',
            'Lithuanian(small)': 'lt',
            'Malay(small)': 'ms',
            'Norwegian Bokmål': 'nb',
            'Persian(small)': 'fa',
            'Polish': 'pl',
            'Portuguese': 'pt',
            'Romanian(small)': 'ro',
            'Russian': 'ru',
            'Serbian(small)': 'sh',
            'Spanish': 'es',
            'Swedish': 'sv',
            'Tagalog(small)': 'fil',
            'Tamil(small)': 'ta',
            'Turkish(small)': 'tr',
            'Ukrainian': 'uk',
            'Urdu(small)': 'ur',
            'Vietnamese(small)': 'vi'
        }

        # Добавьте полные названия языков в language_input
        self.language_input.addItems(self.languages.keys())

        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.accept)

        layout = QFormLayout()
        layout.addRow("Table name:", self.table_name_input)
        layout.addRow("Language:", self.language_input)
        layout.addRow(self.create_button)

        self.setLayout(layout)

    def get_table_info(self):
        return self.table_name_input.text(), self.language_input.currentText()

# app = QApplication(sys.argv)
# window = TableSelectionWindow()
# window.show()
# sys.exit(app.exec_())
