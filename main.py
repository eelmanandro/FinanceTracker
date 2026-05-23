from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout,QHBoxLayout, QWidget,QComboBox,QLineEdit, QCalendarWidget, QTextEdit, QLabel
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt, QDate
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Tracker")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Create buttons
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        self.transaction_type = QComboBox()
        self.transaction_type.addItems(["Income", "Expense"])
        self.amount_input = QLineEdit()
        validator = QDoubleValidator(0.00, 999999.99, 2)
        self.amount_input.setValidator(validator)
        self.amount_input.setPlaceholderText("Введіть суму транзакції")
        self.add_button = QPushButton("Add Transaction")       
        self.transaction_category = QLineEdit()
        self.transaction_category.setPlaceholderText("Введіть категорію транзакції")
        self.transaction_date = QCalendarWidget()
        self.transaction_date.setGridVisible(True)
        self.transaction_date.setNavigationBarVisible(True)
        self.transaction_description = QTextEdit()
        self.transaction_description.setPlaceholderText("Введіть опис транзакції")

        self.transaction_type_label = QLabel("Додайте тип транзакції")
        self.transaction_amount_label = QLabel("Додайте суму")
        self.transaction_category_label = QLabel("Додайте категорію")
        self.transaction_date_label = QLabel("Дoдайте дату")
        self.transaction_description_label = QLabel("Дoдайте опис")

        col2.addWidget(self.transaction_type_label)
        col2.addWidget(self.transaction_type)
        col2.addWidget(self.transaction_amount_label)
        col2.addWidget(self.amount_input)
        col2.addWidget(self.transaction_category_label)
        col2.addWidget(self.transaction_category)
        col2.addWidget(self.transaction_date_label)
        col2.addWidget(self.transaction_date)
        col2.addWidget(self.transaction_description_label)
        col2.addWidget(self.transaction_description)
        col2.addWidget(self.add_button)
        self.add_button.clicked.connect(self.get_data)

        # Add columns to main layout
        layout.addLayout(col1, stretch = 70)
        layout.addLayout(col2, stretch=30)

    def get_data(self):
        transaction_type = self.transaction_type.currentText()
        amount = self.amount_input.text()
        category = self.transaction_category.text()
        date = self.transaction_date.selectedDate()
        description = self.transaction_description.toPlainText()
        print( {
            "type": transaction_type,
            "amount": amount,
            "category": category,
            "date": date,
            "description": description
        })
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())