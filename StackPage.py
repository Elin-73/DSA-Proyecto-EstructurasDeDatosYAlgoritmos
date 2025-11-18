from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton,
                            QLabel, QTextEdit, QLineEdit, QMessageBox)
from PyQt6.QtGui import QFont

from GraphPage import *
from BinaryTreePage import *
from LinkedListPage import *
from ArrayPage import *
from QueuePage import *
from StackPage import *
from SideBar import *

from Estructuras import Stack

class StackPage(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize your Stack class here
        # self.stack = Stack()
        self.stack = Stack()
        
        layout = QVBoxLayout()
        
        title = QLabel("📚 Stack (LIFO - Last In First Out)")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("A Stack is like a stack of plates - you can only add or remove from the top!")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Input area
        input_layout = QHBoxLayout()
        self.stack_input = QLineEdit()
        self.stack_input.setPlaceholderText("Enter a value")
        input_layout.addWidget(self.stack_input)
        
        push_btn = QPushButton("Push")
        push_btn.clicked.connect(self.push_stack)
        push_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        input_layout.addWidget(push_btn)
        
        pop_btn = QPushButton("Pop")
        pop_btn.clicked.connect(self.pop_stack)
        pop_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(pop_btn)
        
        peek_btn = QPushButton("Peek")
        peek_btn.clicked.connect(self.peek_stack)
        peek_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
        input_layout.addWidget(peek_btn)
        
        layout.addLayout(input_layout)
        
        # Visualization area
        self.stack_display = QTextEdit()
        self.stack_display.setReadOnly(True)
        self.stack_display.setMaximumHeight(300)
        layout.addWidget(QLabel("Stack Visualization:"))
        layout.addWidget(self.stack_display)
        
        # Info area
        self.stack_info = QLabel("Stack is empty")
        layout.addWidget(self.stack_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def push_stack(self):
        value = self.stack_input.text().strip()
        if value:
            # Call your stack's push method
            # self.stack.push(value)
            self.stack.push(value)
            self.stack_input.clear()
            self.update_display()
            
    
    def pop_stack(self):
        value = self.stack.pop()
        if value == "Stack is empty":
            QMessageBox.warning(self, "Empty Stack", "Stack is empty!")
        else:
            QMessageBox.information(self, "Popped", f"Popped value: {value}")
            self.update_display()
        # Call your stack's pop method
        # if not self.stack.is_empty():
        #     popped = self.stack.pop()
        #     QMessageBox.information(self, "Popped", f"Popped value: {popped}")
        #     self.update_display()
        # else:
        #     QMessageBox.warning(self, "Empty Stack", "Stack is empty!")
        pass
    
    def peek_stack(self):
        value = self.stack.peek()
        if value == "Stack is empty":
            QMessageBox.warning(self, "Empty Stack", "Stack is empty!")
        else:
            QMessageBox.information(self, "Peek", f"Top value: {value}")
        # Call your stack's peek method
        # if not self.stack.is_empty():
        #     top = self.stack.peek()
        #     QMessageBox.information(self, "Peek", f"Top value: {top}")
        # else:
        #     QMessageBox.warning(self, "Empty Stack", "Stack is empty!")
        pass
    
    def update_display(self):
        # Get the stack data and visualize it
        stack_list = self.stack.toList()
        
        display = "Stack visualization:\n"
        display += stack_list
        
        self.stack_display.setText(display)
        # Update info: self.stack_info.setText(f"Size: {self.stack.size()} | Top: {self.stack.peek() if not self.stack.is_empty() else 'None'}")
        self.stack_info.setText(f"Size: {self.stack.size()} | Top: {self.stack.peek() if not self.stack.isEmpty() else 'None'}")