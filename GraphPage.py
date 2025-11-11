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

class GraphPage(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize your Graph class here
        # self.graph = Graph()
        
        layout = QVBoxLayout()
        
        title = QLabel("🕸️ Graph (Adjacency List)")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("A Graph consists of vertices (nodes) connected by edges!")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Input area
        input_layout = QHBoxLayout()
        self.vertex_input = QLineEdit()
        self.vertex_input.setPlaceholderText("Vertex name")
        input_layout.addWidget(self.vertex_input)
        
        add_vertex_btn = QPushButton("Add Vertex")
        add_vertex_btn.clicked.connect(self.add_vertex)
        add_vertex_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        input_layout.addWidget(add_vertex_btn)
        
        layout.addLayout(input_layout)
        
        # Edge input
        edge_layout = QHBoxLayout()
        self.from_vertex = QLineEdit()
        self.from_vertex.setPlaceholderText("From vertex")
        edge_layout.addWidget(self.from_vertex)
        
        self.to_vertex = QLineEdit()
        self.to_vertex.setPlaceholderText("To vertex")
        edge_layout.addWidget(self.to_vertex)
        
        add_edge_btn = QPushButton("Add Edge")
        add_edge_btn.clicked.connect(self.add_edge)
        add_edge_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
        edge_layout.addWidget(add_edge_btn)
        
        clear_btn = QPushButton("Clear Graph")
        clear_btn.clicked.connect(self.clear_graph)
        clear_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        edge_layout.addWidget(clear_btn)
        
        layout.addLayout(edge_layout)
        
        # Visualization area
        self.graph_display = QTextEdit()
        self.graph_display.setReadOnly(True)
        self.graph_display.setMaximumHeight(300)
        layout.addWidget(QLabel("Graph Adjacency List:"))
        layout.addWidget(self.graph_display)
        
        # Info area
        self.graph_info = QLabel("Graph is empty")
        layout.addWidget(self.graph_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def add_vertex(self):
        vertex = self.vertex_input.text().strip()
        if vertex:
            # self.graph.add_vertex(vertex)
            self.vertex_input.clear()
            self.update_display()
    
    def add_edge(self):
        from_v = self.from_vertex.text().strip()
        to_v = self.to_vertex.text().strip()
        
        if from_v and to_v:
            # self.graph.add_edge(from_v, to_v)
            self.from_vertex.clear()
            self.to_vertex.clear()
            self.update_display()
    
    def clear_graph(self):
        # self.graph.clear()
        self.update_display()
    
    def update_display(self):
        display = "A → [B, C]\n"
        display += "B → [A, D]\n"
        display += "C → [A]\n"
        display += "D → [B]"
        self.graph_display.setText(display)