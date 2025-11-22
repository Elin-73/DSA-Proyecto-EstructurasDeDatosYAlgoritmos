from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton,
                            QLabel, QTextEdit,
                            QLineEdit, QMessageBox)
from PyQt6.QtGui import QFont

class ArrayPage(QWidget):
    def __init__(self):
        super().__init__()
        self.array = []
        self.sorted = True
        
        layout = QVBoxLayout()
        
        title = QLabel("📊 Array (Fixed/Dynamic List)")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("An Array stores elements in contiguous memory locations with index-based access!")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Input area
        input_layout = QHBoxLayout()
        self.array_input = QLineEdit()
        self.array_input.setPlaceholderText("Enter a value")
        input_layout.addWidget(self.array_input)
        
        self.index_input = QLineEdit()
        self.index_input.setPlaceholderText("Index")
        self.index_input.setMaximumWidth(80)
        input_layout.addWidget(self.index_input)
        
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_element)
        add_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        input_layout.addWidget(add_btn)
        
        insert_btn = QPushButton("Insert at Index")
        insert_btn.clicked.connect(self.insert_element)
        insert_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 10px;")
        input_layout.addWidget(insert_btn)
        
        delete_btn = QPushButton("Delete at Index")
        delete_btn.clicked.connect(self.delete_element)
        delete_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(delete_btn)

        search_btn = QPushButton("Search for value")
        search_btn.clicked.connect(self.binary_search)
        search_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(search_btn)

        sort_btn = QPushButton("Shell Sort array")
        sort_btn.clicked.connect(self.shell_sort)
        sort_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(sort_btn)
        
        layout.addLayout(input_layout)
        
        # Visualization area
        self.array_display = QTextEdit()
        self.array_display.setReadOnly(True)
        self.array_display.setMaximumHeight(200)
        layout.addWidget(QLabel("Array Visualization:"))
        layout.addWidget(self.array_display)
        
        # Info area
        self.array_info = QLabel("Array is empty")
        layout.addWidget(self.array_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def add_element(self):
        value = self.array_input.text().strip()
        if value:
            self.array.append(value)
            self.array_input.clear()
            self.update_display()
    
    def insert_element(self):
        value = self.array_input.text().strip()
        index_str = self.index_input.text().strip()
        
        if value and index_str:
            try:
                index = int(index_str)
                if 0 <= index <= len(self.array):
                    self.array.insert(index, value)
                    self.array_input.clear()
                    self.index_input.clear()
                    self.update_display()
                else:
                    QMessageBox.warning(self, "Invalid Index", f"Index must be between 0 and {len(self.array)}")
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Index must be a number")
    
    def delete_element(self):
        index_str = self.index_input.text().strip()
        if index_str:
            try:
                index = int(index_str)
                if 0 <= index < len(self.array):
                    removed = self.array.pop(index)
                    self.index_input.clear()
                    QMessageBox.information(self, "Deleted", f"Deleted value: {removed}")
                    self.update_display()
                else:
                    QMessageBox.warning(self, "Invalid Index", f"Index must be between 0 and {len(self.array)-1}")
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Index must be a number")
    
    def update_display(self):
        if self.array:
            indices = "Indices: " + " ".join([f"[{i}]" for i in range(len(self.array))]) + "\n"
            values = "Values:  " + " ".join([f"[{v}]" for v in self.array])
            display = indices + values
        else:
            display = "Array is empty"
        
        self.array_display.setText(display)
        self.array_info.setText(f"Size: {len(self.array)}")
        self.sorted = False

    def shell_sort(self):
        array_len = self.array
        gaps = array_len // 2
        while gaps > 0:
            for i in range(gaps, array_len):
                t = self.array[i]
                j = i
                while j >= gaps and self.array[j-gaps] > t:
                    self.array[j] = self.array[j-gaps]
                    j -= gaps
                self.array[j] = t
            gaps //= 2
        self.update_display()
        self.sorted = True
        QMessageBox.information(self, "Sorted", f"The Array has been sorted")

    def binary_search(self):
        value = self.array_input.text().strip()
        if value and self.sorted:
            try:

                left = 0
                right = len(self.array) - 1
                while left <= right:
                    mid = (left + right) // 2
                    if self.array[mid] == value:

                        index_value = mid
                        self.array_input.clear()
                        QMessageBox.information(self, "Search", f"Value found on index: {index_value}")

                    if self.array[mid] < value:
                        left = mid + 1
                    else:
                        right = mid - 1
            except:
                QMessageBox.warning(self, "Invalid Value", f"value must be part of the array")
        else:
            QMessageBox.warning(self, "Invalid Operation", f"array must be ordered (use the button)")