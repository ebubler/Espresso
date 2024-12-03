import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6.uic import loadUi
import sqlite3


class AddEditCoffeeForm(QMainWindow):
    def __init__(self, parent=None, record_id=None):
        super().__init__(parent)
        loadUi('addEditCoffeeForm.ui', self)

        self.database2 = sqlite3.connect('coffee.db')

        self.record_id = record_id
        self.saveButton.clicked.connect(self.save_record)

        if self.record_id:
            self.load_record()

    def load_record(self):
        curs = self.database2.cursor()
        curs.execute(f"SELECT * FROM coffees WHERE id = {self.record_id}")
        coffee = curs.fetchone()
        curs.close()
        self.nameLineEdit.setText(coffee[1])
        self.roastLineEdit.setText(coffee[2])
        self.grindLineEdit.setText(coffee[3])
        self.descriptionTextEdit.setText(coffee[4])
        self.priceSpinBox.setText(coffee[5])
        self.volumeSpinBox.setText(coffee[6])

    def save_record(self):
        name = self.nameLineEdit.text()
        roast = self.roastLineEdit.text()
        grind = self.grindLineEdit.text()
        description = self.descriptionTextEdit.toPlainText()
        price = self.priceSpinBox.text()
        volume = self.volumeSpinBox.text()
        print(name, roast, grind, description, price, volume)
        curs = self.database2.cursor()

        if self.record_id:
            curs.execute(f"""
                UPDATE coffees
                SET name = '{name}', roasting = '{roast}', type = '{grind}', 
                description = '{description}', price = '{price}', package = '{volume}'
                WHERE id = {self.record_id}
            """)
        else:
            curs.execute(f"""
                INSERT INTO coffees (name, roasting, type, description, price, package)
                VALUES ('{name}', '{roast}', '{grind}', '{description}', '{price}', '{volume}')
            """)
        self.database2.commit()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)

        self.database = sqlite3.connect('coffee.db')

        self.addButton.clicked.connect(self.add_record)
        self.editButton.clicked.connect(self.edit_record)
        self.upButton.clicked.connect(self.display_data)

        self.display_data()

    def display_data(self):
        self.tableWidget.clearContents()

        curs = self.database.cursor()
        curs.execute("SELECT * FROM coffees")
        data = curs.fetchall()
        curs.close()

        num_rows = len(data)
        num_cols = len(data[0]) if data else 0

        self.tableWidget.setRowCount(num_rows)
        self.tableWidget.setColumnCount(num_cols)

        for i in range(num_rows):
            for j in range(num_cols):
                item = QTableWidgetItem(str(data[i][j]))
                self.tableWidget.setItem(i, j, item)

    def add_record(self):
        form = AddEditCoffeeForm(self)
        form.show()

    def edit_record(self):
        selected_row = self.tableWidget.currentRow()

        record_id = int(self.tableWidget.item(selected_row, 0).text())
        form = AddEditCoffeeForm(self, record_id)
        form.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
