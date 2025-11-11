import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QStackedWidget, QLabel)

from GraphPage import GraphPage
from BinaryTreePage import *
from LinkedListPage import *
from ArrayPage import *
from QueuePage import *
from StackPage import *
from SideBar import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Structures Visualizer")
        self.setGeometry(100, 100, 1100, 700)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #2c3e50;")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # App title
        app_title = QLabel("  Data Structures")
        app_title.setStyleSheet("color: white; padding: 20px; font-size: 18px; font-weight: bold;")
        sidebar_layout.addWidget(app_title)
        
        # Menu buttons
        self.menu_buttons = []
        menu_items = [
            "Stack",
            "Queue",
            "Array",
            "Circular Linked List",
            "Binary Tree",
            "Graph"
        ]
        
        for item in menu_items:
            btn = SidebarButton(f"  {item}")
            btn.clicked.connect(lambda checked, index=len(self.menu_buttons): self.switch_page(index))
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)
        
        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)
        
        # Content area (stacked widget)
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #ecf0f1; padding: 20px;")
        
        # Add pages
        self.content_stack.addWidget(StackPage())
        self.content_stack.addWidget(QueuePage())
        self.content_stack.addWidget(ArrayPage())
        self.content_stack.addWidget(CircularLinkedListPage())
        self.content_stack.addWidget(BinaryTreePage())
        self.content_stack.addWidget(GraphPage())
        
        # Add sidebar and content to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Set Stack as default
        self.switch_page(0)
        
    def switch_page(self, index):
        # Uncheck all buttons
        for btn in self.menu_buttons:
            btn.setChecked(False)
        
        # Check the selected button
        self.menu_buttons[index].setChecked(True)
        
        # Switch to the corresponding page
        self.content_stack.setCurrentIndex(index)