import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QStackedWidget, QLabel)

from SideBar import SidebarButton
from StackPage import StackPage
from QueuePage import QueuePage
from ArrayPage import ArrayPage
from LinkedListPage import CircularLinkedListPage
from BinaryTreePage import BinaryTreePage
from GraphPage import GraphPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projecto Final: Estructuras de Datos")
        self.setGeometry(50, 50, 1400, 850)
        self.setMinimumSize(1200, 700)
        
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #2c3e50;")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        app_title = QLabel("  Estructuras de Datos")
        app_title.setStyleSheet("""
            color: white; 
            padding: 20px; 
            font-size: 18px; 
            font-weight: bold;
            background-color: #1a252f;
        """)
        sidebar_layout.addWidget(app_title)
        
        self.menu_buttons = []
        menu_items = [
            ("📚", "Pila"),
            ("🎫", "Cola"),
            ("📊", "Arreglo"),
            ("🔄", "Lista Circular Simple"),
            ("🌳", "Arbol Binario"),
            ("🕸️", "Grafo")
        ]
        
        for icon, name in menu_items:
            btn = SidebarButton(f"  {icon}  {name}")
            btn.clicked.connect(lambda checked, index=len(self.menu_buttons): self.switch_page(index))
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)
        
        sidebar_layout.addStretch()
        
        footer = QLabel("  v1.0 - PyQt6")
        footer.setStyleSheet("color: #7f8c8d; padding: 10px; font-size: 11px;")
        sidebar_layout.addWidget(footer)
        
        sidebar.setLayout(sidebar_layout)
        
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #ecf0f1;")
        
        self.content_stack.addWidget(StackPage())
        self.content_stack.addWidget(QueuePage())
        self.content_stack.addWidget(ArrayPage())
        self.content_stack.addWidget(CircularLinkedListPage())
        self.content_stack.addWidget(BinaryTreePage())
        self.content_stack.addWidget(GraphPage())
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        self.switch_page(0)
        
    def switch_page(self, index):
        for btn in self.menu_buttons:
            btn.setChecked(False)
        
        self.menu_buttons[index].setChecked(True)
        
        self.content_stack.setCurrentIndex(index)