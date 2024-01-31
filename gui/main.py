import sys
import os
from PyQt5.QtWidgets import QApplication
from tables import TableSelectionWindow
from window import MainWindow

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

def main():
    app = QApplication(sys.argv)

    # Create and display the table selection window
    table_selection_window = TableSelectionWindow()
    table_selection_window.show()

    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
