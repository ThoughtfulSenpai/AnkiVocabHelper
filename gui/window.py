from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QWidget, QMessageBox, QHBoxLayout, QMenu, QAction, QApplication, QMessageBox
from PyQt5.QtCore import Qt
import sys

from db import add_word, create_connection, get_all_words, create_table, delete_word, add_column, column_exists, \
    word_exists, set_favorite, get_favorite, add_favorite_column, get_language
from wordfreqlib import get_word_difficulty
from info_window import InfoWindow

class MainWindow(QMainWindow):
    def __init__(self, table_name):
        super().__init__()
        self.setWindowTitle("AnkiVocabHelperDevelopment")
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

        self.word_sort_order = 0
        self.difficulty_sort_order = 0
        self.date_sort_order = 0

       # Set the window size
        self.setGeometry(100, 100, 800, 600)  # Parametres: x, y, width, height

        # Create a connection to the database with the specified table name
        self.conn = create_connection(table_name)

       # Create a table if it doesn't already exist
        create_table(self.conn)

       # Add a new column called date_added if it doesn't already exist
        if not column_exists(self.conn, "date_added"):
            add_column(self.conn)

       # Add a new column named favorite if it doesn't already exist
        if not column_exists(self.conn, "favorite"):
            add_favorite_column(self.conn)

        # Create widgets
        self.word_input = QLineEdit()
        self.add_button = QPushButton("Add")
        self.copyWords = QPushButton("Copy Words to clipboard")

        # Connecting the "add" button click an event handler. 
        self.add_button.clicked.connect(self.add_word)
        # Connect the event handler for pressing the Enter key
        self.word_input.returnPressed.connect(self.add_word)
        
        # Connect the event handler for clicking the "Copy Words" button.
        self.copyWords.clicked.connect(self.copy_words_to_clipboard)
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Words", "Difficulty", "Controls"])

        # Get the horizontal table header
        header = self.table.horizontalHeader()

        # Set the stretch of the last column
        header.setStretchLastSection(True)

        # Connect the event handler for clicking on the column header
        self.table.horizontalHeader().sectionClicked.connect(self.sort_table)  

       # Set the initial size of the table
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 100)

        # Connect the event handler for clicking on a table element
        self.table.itemClicked.connect(self.handle_item_clicked)

        # Create a layout and add widgets to it
        layout = QVBoxLayout()
        layout.addWidget(self.word_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.copyWords)
        layout.addWidget(self.table)

        self.info_button = QPushButton("i")
        self.info_button.clicked.connect(self.show_info)
        self.info_button.setFixedSize(30, 30)  # parameters: width, height

        self.back_button = QPushButton("Back")  # Create a new button
        self.back_button.clicked.connect(self.go_back)  #Connect the button click event handler
        self.back_button.setFixedSize(50, 30)

        # Create a horizontal layout
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.info_button)
        h_layout.addStretch()  # Add stretch between buttons
        h_layout.addWidget(self.back_button)

        layout.addLayout(h_layout)  # Add a horizontal layout to the main vertical layout

        # Create a central widget and install it in the window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_table()  

    def add_word(self):
        words = self.word_input.text().split(',')
        for word in words:
            word = word.strip()  # Удалить пробелы в начале и конце слова
            if word_exists(self.conn, word):
                # Создаем и показываем QMessageBox
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f'Word "{word}" already exists in the table.')
                msg.setWindowTitle("Error")
                msg.exec_()
            else:
                # Получите язык из базы данных
                language = get_language(self.conn)
                # Передайте язык в функцию get_word_difficulty
                difficulty = get_word_difficulty(word, language)
                add_word(self.conn, word, difficulty)
                # print(f"Added word: {word}")  # Добавьте эту строку
        self.update_table()
        self.word_input.clear()

    def toggle_favorite(self, word):
        # Получите текущее состояние избранного для слова из базы данных
        favorite = get_favorite(self.conn,
                                word)  # Замените get_favorite на имя вашей функции для получения состояния избранного

        # Переключите состояние избранного
        set_favorite(self.conn, word,
                     not favorite)  # Замените set_favorite на имя вашей функции для установки состояния избранного

        # Обновите таблицу
        self.update_table()

    def update_table(self):
        words = get_all_words(self.conn)

        #print(f"Loaded {len(words)} words from the database")  # Добавьте эту строку

        self.table.setRowCount(len(words))
        self.table.setColumnCount(5)  # Увеличьте количество столбцов до 5
        self.table.setHorizontalHeaderLabels(
            ["Words", "Difficulty", "Date", "Favorite", "Controls"])  # Добавьте заголовок "Favorite"

        for i, (id, word, frequency, date_added, favorite) in enumerate(words):  # Добавьте favorite в список переменных
            #print(f"Adding word: {word}")  # Добавьте эту строку

            self.table.setItem(i, 0, QTableWidgetItem(word))
            self.table.setItem(i, 1, NumericTableWidgetItem(str(frequency)))
            self.table.setItem(i, 2, QTableWidgetItem(date_added))

            # Создайте кнопку "Избранное" и установите ее иконку в зависимости от значения favorite
            favorite_button = QPushButton()
            favorite_button.setIcon(QIcon(
                "star_filled.png" if favorite else "star_empty.png"))  # Замените "star_filled.png" и "star_empty.png" на пути к вашим файлам иконок
            favorite_button.clicked.connect(lambda checked, word=word: self.toggle_favorite(word))

            # Добавьте кнопку в таблицу
            self.table.setCellWidget(i, 3, favorite_button)

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda checked, word=word: self.delete_word(word))
            self.table.setCellWidget(i, 4, delete_button)

        # Устанавливаем ширину столбцов
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 100)  # Установите ширину столбца для кнопки "Избранное"

    def handle_item_clicked(self, item):
        # Проверяем, является ли элемент кнопкой "Удалить"
        if item.column() == 2 and item.text() == "Delete":
            # Получаем слово из таблицы
            word = self.table.item(item.row(), 0).text()

            # Удаляем слово из базы данных
            delete_word(self.conn, word)

            # Обновляем таблицу
            self.update_table()
            
    def delete_word(self, word):
       # Remove the word from the database
        delete_word(self.conn, word)
        # Update the table
        self.update_table()

    def sort_table(self, column):
        if column == 0:
            if self.word_sort_order == 0:
                # Сортируем слова в алфавитном порядке
                self.word_sort_order = 1
            elif self.word_sort_order == 1:
                # Сортируем слова в обратном алфавитном порядке
                self.word_sort_order = -1
            else:
                # Возвращаемся к исходному порядку
                self.word_sort_order = 0

            self.sort_words(self.word_sort_order)

        elif column == 1:
            if self.difficulty_sort_order == 0:
                # Сортируем по сложности от легких к сложным
                self.difficulty_sort_order = 1
            elif self.difficulty_sort_order == 1:
                # Сортируем по сложности от сложных к легким
                self.difficulty_sort_order = -1
            else:
                # Возвращаемся к исходному порядку
                self.difficulty_sort_order = 0

            self.sort_difficulty(self.difficulty_sort_order)

        elif column == 2:
            if self.date_sort_order == 0:
                # Сортируем по дате от ранних к поздним
                self.date_sort_order = 1
            elif self.date_sort_order == 1:
                # Сортируем по дате от поздних к ранним
                self.date_sort_order = -1
            else:
                # Возвращаемся к исходному порядку
                self.date_sort_order = 0

            self.sort_date(self.date_sort_order)

        # Store the current sort column and order
        self.current_sort_column = column
        if column == 0:
            self.current_sort_order = Qt.AscendingOrder if self.word_sort_order == 1 else Qt.DescendingOrder
        elif column == 1:
            self.current_sort_order = Qt.AscendingOrder if self.difficulty_sort_order == 1 else Qt.DescendingOrder
        elif column == 2:
            self.current_sort_order = Qt.AscendingOrder if self.date_sort_order == 1 else Qt.DescendingOrder

    def sort_date(self, order):
        if order == 0:
            # Сортируем по дате от ранних к поздним
            self.table.sortItems(2, Qt.AscendingOrder)
        elif order == 1:
            # Сортируем по дате от поздних к ранним
            self.table.sortItems(2, Qt.DescendingOrder)

    def sort_words(self, order):
        if order == 0:
            # Сортируем слова в алфавитном порядке
            self.table.sortItems(0, Qt.AscendingOrder)
        elif order == 1:
            # Сортируем слова в обратном алфавитном порядке
            self.table.sortItems(0, Qt.DescendingOrder)

    def sort_difficulty(self, order):
        if order == 0:
            # Сортируем по сложности от легких к сложным
            self.table.sortItems(1, Qt.AscendingOrder)
        elif order == 1:
            # Сортируем по сложности от сложных к легким
            self.table.sortItems(1, Qt.DescendingOrder)

    def show_info(self):
        self.info_window = InfoWindow()
        self.info_window.show()

    def go_back(self):
        # Закройте MainWindow
        self.close()

        # Создайте и покажите TableSelectionWindow
        from tables import TableSelectionWindow  # Импортируйте здесь
        self.table_selection_window = TableSelectionWindow()
        self.table_selection_window.show()

    def copy_words_to_clipboard(self):
        # Get the words from the first column
        words = [self.table.item(row, 0).text() for row in range(self.table.rowCount())]

        # Join the words into a string, separated by a comma and a space
        words_text = ", ".join(words)

        # Create a QClipboard object
        clipboard = QApplication.clipboard()

        # Set the text to the clipboard
        clipboard.setText(words_text)

        # Show a message to indicate that the words are copied
        QMessageBox.information(self, "Copy Words", "Words copied to clipboard.")


class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        return float(self.text()) < float(other.text())

# # Create the application and the main window
    
# app = QApplication(sys.argv)
# window = MainWindow()
# window.update_table()
# window.show()
    
# # Start the application event loop
# sys.exit(app.exec_())