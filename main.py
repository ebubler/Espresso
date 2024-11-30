import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6.uic import loadUi
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)

        self.database = sqlite3.connect('coffee.db')
        self.display_data()

    def display_data(self):

        curs = self.database.cursor()

        curs.execute(f"""
        SELECT * from coffees
        """)

        data = curs.fetchall()
        print(data)

        num_rows = len(data)
        num_cols = len(data[0]) if data else 0

        self.tableWidget.setRowCount(num_rows)
        self.tableWidget.setColumnCount(num_cols)

        for i in range(len(data)):
            for j in range(len(data[i])):
                item = QTableWidgetItem(str(data[i][j]))
                self.tableWidget.setItem(i, j, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())