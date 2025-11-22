from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton,
                            QLabel, QTextEdit,
                            QLineEdit, QMessageBox)
from PyQt6.QtGui import QFont, QIntValidator


class ArrayPage(QWidget):
    def __init__(self):
        super().__init__()
        self.array = []
        self.sorted = False
        
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
        self.array_input.setPlaceholderText("Enter an integer")
        self.array_input.setValidator(QIntValidator())
        input_layout.addWidget(self.array_input)
        
        self.index_input = QLineEdit()
        self.index_input.setPlaceholderText("Index")
        self.index_input.setMaximumWidth(80)
        self.index_input.setValidator(QIntValidator(0, 999999))
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
        
        layout.addLayout(input_layout)
        
        # SEGUNDA LINEA DE BOTONES
        button_layout = QHBoxLayout()
        
        search_btn = QPushButton("Binary Search")
        search_btn.clicked.connect(self.binary_search)
        search_btn.setStyleSheet("background-color: #f1c40f; color: black; padding: 10px;")
        button_layout.addWidget(search_btn)

        sort_btn = QPushButton("Shell Sort")
        sort_btn.clicked.connect(self.shell_sort)
        sort_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
        button_layout.addWidget(sort_btn)
        
        clear_btn = QPushButton("Clear Array")
        clear_btn.clicked.connect(self.clear_array)
        clear_btn.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
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
            try:
                int_value = int(value)
                self.array.append(int_value)
                self.array_input.clear()
                self.sorted = False
                self.update_display()
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer")
        else:
            QMessageBox.warning(self, "Empty Input", "Please enter a value")
    
    def insert_element(self):
        value = self.array_input.text().strip()
        index_str = self.index_input.text().strip()
        
        if not value:
            QMessageBox.warning(self, "Empty Input", "Please enter a value")
            return
        
        if not index_str:
            QMessageBox.warning(self, "Empty Index", "Please enter an index")
            return
        
        try:
            int_value = int(value)
            index = int(index_str)
            
            if 0 <= index <= len(self.array):
                self.array.insert(index, int_value)
                self.array_input.clear()
                self.index_input.clear()
                self.sorted = False
                self.update_display()
            else:
                QMessageBox.warning(self, "Invalid Index", f"Index must be between 0 and {len(self.array)}")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Value and index must be integers")
    
    def delete_element(self):
        index_str = self.index_input.text().strip()
        
        if not index_str:
            QMessageBox.warning(self, "Empty Index", "Please enter an index")
            return
        
        try:
            index = int(index_str)
            if 0 <= index < len(self.array):
                removed = self.array.pop(index)
                self.index_input.clear()
                self.sorted = False
                QMessageBox.information(self, "Deleted", f"Deleted value: {removed}")
                self.update_display()
            else:
                if len(self.array) == 0:
                    QMessageBox.warning(self, "Empty Array", "Array is empty!")
                else:
                    QMessageBox.warning(self, "Invalid Index", f"Index must be between 0 and {len(self.array)-1}")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Index must be an integer")
    
    def clear_array(self):
        self.array = []
        self.sorted = False
        self.update_display()
    
    def update_display(self):
        if self.array:
            indices = "Indices: " + " ".join([f"[{i}]" for i in range(len(self.array))]) + "\n"
            values = "Values:  " + " ".join([f"[{v}]" for v in self.array])
            display = indices + values
        else:
            display = "Array is empty"
        
        self.array_display.setText(display)
        
        sorted_status = "Sorted ✓" if self.sorted else "Unsorted"
        self.array_info.setText(f"Size: {len(self.array)} | Status: {sorted_status}")

    def shell_sort(self):
        if len(self.array) == 0:
            QMessageBox.warning(self, "Empty Array", "Array is empty!")
            return
        
        if len(self.array) == 1:
            self.sorted = True
            self.update_display()
            QMessageBox.information(self, "Sorted", "Array has only one element, already sorted!")
            return
        
        array_len = len(self.array)
        gap = array_len // 2
        
        while gap > 0:
            for i in range(gap, array_len):
                temp = self.array[i]
                j = i
                while j >= gap and self.array[j - gap] > temp:
                    self.array[j] = self.array[j - gap]
                    j -= gap
                self.array[j] = temp
            gap //= 2
        
        self.sorted = True
        self.update_display()
        QMessageBox.information(self, "Sorted", "Array has been sorted using Shell Sort!")

    def binary_search(self):
        if len(self.array) == 0:
            QMessageBox.warning(self, "Empty Array", "Array is empty!")
            return
        
        if not self.sorted:
            QMessageBox.warning(self, "Unsorted Array", 
                                    "Array must be sorted first!\nClick 'Shell Sort' to sort the array.")
            return
        
        value = self.array_input.text().strip()
        
        if not value:
            QMessageBox.warning(self, "Empty Input", "Please enter a value to search")
            return
        
        try:
            search_value = int(value)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer")
            return
        
        left = 0
        right = len(self.array) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if self.array[mid] == search_value:
                self.array_input.clear()
                QMessageBox.information(self, "Found!", 
                                    f"Value {search_value} found at index: {mid}")
                return
            elif self.array[mid] < search_value:
                left = mid + 1
            else:
                right = mid - 1
        
        QMessageBox.information(self, "Not Found", 
                            f"Value {search_value} was not found in the array")