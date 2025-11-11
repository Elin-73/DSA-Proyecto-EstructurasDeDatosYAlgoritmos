import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QStackedWidget, QLabel,
                            QTextEdit, QLineEdit, QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor

from GraphPage import *
from BinaryTreePage import *
from LinkedListPage import *
from ArrayPage import *
from QueuePage import *
from StackPage import *
from SideBar import *

class ArrayPage(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize your Array class here
        # self.array = Array()
        
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
            # self.array.append(value)
            self.array_input.clear()
            self.update_display()
    
    def insert_element(self):
        value = self.array_input.text().strip()
        index_str = self.index_input.text().strip()
        
        if value and index_str:
            try:
                index = int(index_str)
                # self.array.insert(index, value)
                self.array_input.clear()
                self.index_input.clear()
                self.update_display()
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Index must be a number")
    
    def delete_element(self):
        index_str = self.index_input.text().strip()
        if index_str:
            try:
                index = int(index_str)
                # removed = self.array.delete(index)
                self.index_input.clear()
                # QMessageBox.information(self, "Deleted", f"Deleted value: {removed}")
                self.update_display()
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Index must be a number")
    
    def update_display(self):
        display = "Indices: [0] [1] [2] [3]\n"
        display += "Values:  [A] [B] [C] [D]"
        self.array_display.setText(display)