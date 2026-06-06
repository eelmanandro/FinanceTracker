from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout,QHBoxLayout, QWidget,QComboBox,QLineEdit, QCalendarWidget, QTextEdit, QLabel, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QDoubleValidator, QIcon
from PyQt5.QtCore import Qt, QDate
import sys
import json
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Tracker")
        self.setGeometry(100, 100, 1200, 600)

        # Create a central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        if hasattr(sys, "_MEIPASS"):
            self.setWindowIcon(QIcon(os.path.join(sys._MEIPASS, "finance-icon.ico")))
        else:
            self.setWindowIcon(QIcon("finance-icon.ico"))

        # Create buttons
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        self.transaction_tree = QTreeWidget()
        self.transaction_tree.setColumnCount(5)
        self.transaction_tree.setHeaderLabels(["ID", "Дата", "Тип", "Категорія", "Сума"])
        self.transaction_tree.setColumnWidth(0, 50)
        col1.addWidget(QLabel("Історія транзакцій"))
        col1.addWidget(self.transaction_tree)
        self.transaction_type = QComboBox()
        self.transaction_type.addItems(["Income", "Expense"])
        self.amount_input = QLineEdit()
        validator = QDoubleValidator(0.00, 999999.99, 2)
        self.amount_input.setValidator(validator)
        self.amount_input.setPlaceholderText("Введіть суму транзакції")
        self.add_button = QPushButton("Додати транзакцію")
        self.del_button = QPushButton("Видалити транзакцію")
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
        col2.addWidget(self.del_button)
        self.add_button.clicked.connect(self.add_transaction)
        self.del_button.clicked.connect(self.delete_transaction)

        # Add columns to main layout
        layout.addLayout(col1, stretch = 70)
        layout.addLayout(col2, stretch=30)

        self.transactions_filename = "transactions.json"
        self.transactions = self.load_transactions()
        self.update_transaction_list()

    def get_data(self):
        transaction_type = self.transaction_type.currentText()
        amount = self.amount_input.text()
        category = self.transaction_category.text()
        date = self.transaction_date.selectedDate().toString("yyyy-MM-dd")
        description = self.transaction_description.toPlainText()
        return{
            "type": transaction_type,
            "amount": amount,
            "category": category,
            "date": date,
            "description": description
        }
    
    def load_transactions(self):
        try:
            with open(self.transactions_filename, "r") as file:
                transactions = json.load(file)
            return transactions
        except FileNotFoundError:
            transactions = {}
            with open(self.transactions_filename, "w") as file:
                json.dump(transactions, file, ensure_ascii=False, indent=2)
            return transactions

    def get_lastID(self):
        IDs = list(map(int, self.transactions.keys()))
        if IDs:
            return IDs[-1]
        else:
            return 0

    def add_transaction(self):
        transaction_data = self.get_data()
        last_id = self.get_lastID()
        self.transactions[str(last_id + 1)] = transaction_data
        self.transactions = dict(self.sort_transactions())
        with open(self.transactions_filename, "w") as file:
            json.dump(self.transactions, file, ensure_ascii=False, indent=2)
        self.clear_inputs()
        self.update_transaction_list()

    def delete_transaction(self):
        selected_items = self.transaction_tree.selectedItems()
        if not selected_items:
            return
        selected_item = selected_items[0]
        transaction_id = selected_item.text(0)
        if transaction_id in self.transactions:
            del self.transactions[transaction_id]
            with open(self.transactions_filename, "w") as file:
                json.dump(self.transactions, file, ensure_ascii=False, indent=2)
            self.update_transaction_list()

    def sort_transactions(self):
        def get_num_key(transaction):
            return int(transaction[0])
        sorted_transactions = sorted(self.transactions.items(), key=get_num_key)
        return sorted_transactions
    
    def update_transaction_list(self):
        self.transaction_tree.clear()
        for id, transaction in self.transactions.items():
            item = QTreeWidgetItem([
                id,
                transaction.get("date", ""),
                transaction.get("type", ""),
                transaction.get("category", ""),
                transaction.get("amount", "")
            ])
            self.transaction_tree.addTopLevelItem(item)
    
    def clear_inputs(self):
        self.amount_input.clear()
        self.transaction_category.clear()
        self.transaction_description.clear()
        self.transaction_date.setSelectedDate(QDate.currentDate())
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())