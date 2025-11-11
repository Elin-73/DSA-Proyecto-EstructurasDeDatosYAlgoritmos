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

class QueuePage(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize your Queue class here
        # self.queue = Queue()
        
        layout = QVBoxLayout()
        
        title = QLabel("🎫 Queue (FIFO - First In First Out)")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("A Queue is like a line at a store - first person in is the first person served!")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Input area
        input_layout = QHBoxLayout()
        self.queue_input = QLineEdit()
        self.queue_input.setPlaceholderText("Enter a value")
        input_layout.addWidget(self.queue_input)
        
        enqueue_btn = QPushButton("Enqueue (Add)")
        enqueue_btn.clicked.connect(self.enqueue)
        enqueue_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        input_layout.addWidget(enqueue_btn)
        
        dequeue_btn = QPushButton("Dequeue (Remove)")
        dequeue_btn.clicked.connect(self.dequeue)
        dequeue_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(dequeue_btn)
        
        front_btn = QPushButton("Front")
        front_btn.clicked.connect(self.peek_front)
        front_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
        input_layout.addWidget(front_btn)
        
        layout.addLayout(input_layout)
        
        # Visualization area
        self.queue_display = QTextEdit()
        self.queue_display.setReadOnly(True)
        self.queue_display.setMaximumHeight(150)
        layout.addWidget(QLabel("Queue Visualization:"))
        layout.addWidget(self.queue_display)
        
        # Info area
        self.queue_info = QLabel("Queue is empty")
        layout.addWidget(self.queue_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def enqueue(self):
        value = self.queue_input.text().strip()
        if value:
            # self.queue.enqueue(value)
            self.queue_input.clear()
            self.update_display()
    
    def dequeue(self):
        # if not self.queue.is_empty():
        #     removed = self.queue.dequeue()
        #     QMessageBox.information(self, "Dequeued", f"Removed value: {removed}")
        #     self.update_display()
        # else:
        #     QMessageBox.warning(self, "Empty Queue", "Queue is empty!")
        pass
    
    def peek_front(self):
        # if not self.queue.is_empty():
        #     front = self.queue.front()
        #     QMessageBox.information(self, "Front", f"Front value: {front}")
        # else:
        #     QMessageBox.warning(self, "Empty Queue", "Queue is empty!")
        pass
    
    def update_display(self):
        display = "FRONT → [Item1] ← [Item2] ← [Item3] ← REAR"
        self.queue_display.setText(display)