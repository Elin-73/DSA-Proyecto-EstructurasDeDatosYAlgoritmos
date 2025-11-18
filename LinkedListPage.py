from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel,
                            QTextEdit, QLineEdit)
from PyQt6.QtGui import QFont

from GraphPage import *
from BinaryTreePage import *
from LinkedListPage import *
from ArrayPage import *
from QueuePage import *
from StackPage import *
from SideBar import *

from Estructuras import CircularList

class CircularLinkedListPage(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize your CircularLinkedList class here
        self.cll = CircularList()
        
        layout = QVBoxLayout()
        
        title = QLabel("🔄 Circular Linked List")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("A Circular Linked List where the last node points back to the first node, forming a circle!")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Input area
        input_layout = QHBoxLayout()
        self.cll_input = QLineEdit()
        self.cll_input.setPlaceholderText("Enter a value")
        input_layout.addWidget(self.cll_input)
        
        add_btn = QPushButton("Add Node")
        add_btn.clicked.connect(self.add_node)
        add_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        input_layout.addWidget(add_btn)
        
        delete_btn = QPushButton("Delete First")
        delete_btn.clicked.connect(self.delete_node)
        delete_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(delete_btn)
        
        traverse_btn = QPushButton("Traverse")
        traverse_btn.clicked.connect(self.traverse)
        traverse_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
        input_layout.addWidget(traverse_btn)
        
        layout.addLayout(input_layout)
        
        # Visualization area
        self.cll_display = QTextEdit()
        self.cll_display.setReadOnly(True)
        self.cll_display.setMaximumHeight(200)
        layout.addWidget(QLabel("Circular Linked List Visualization:"))
        layout.addWidget(self.cll_display)
        
        # Info area
        self.cll_info = QLabel("List is empty")
        layout.addWidget(self.cll_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def add_node(self):
        value = self.cll_input.text().strip()
        if value:
            # self.cll.add(value)
            self.cll_input.clear()
            self.update_display()
    
    def delete_node(self):
        removed = self.cll.pop()
        # if not self.cll.is_empty():
        #     removed = self.cll.delete_first()
        #     QMessageBox.information(self, "Deleted", f"Deleted node: {removed}")
        #     self.update_display()
        # else:
        #     QMessageBox.warning(self, "Empty List", "List is empty!")
        pass
    
    def traverse(self):
        # if not self.cll.is_empty():
        #     traversal = self.cll.traverse()
        #     QMessageBox.information(self, "Traversal", traversal)
        # else:
        #     QMessageBox.warning(self, "Empty List", "List is empty!")
        pass
    
    def update_display(self):
        display = "[Node1] → [Node2] → [Node3] → [back to Node1] ↻"
        self.cll_display.setText(display)