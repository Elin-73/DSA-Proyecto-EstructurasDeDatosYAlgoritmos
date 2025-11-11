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

class SidebarButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 15px 20px;
                border: none;
                background-color: #2c3e50;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #3498db;
                font-weight: bold;
            }
        """)