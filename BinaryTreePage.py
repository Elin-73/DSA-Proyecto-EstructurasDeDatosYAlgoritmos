from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel,
                            QLineEdit, QMessageBox, QScrollArea)
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt
import math

from Estructuras import Tree


class BinaryTreeCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1000, 600)
        self.tree_nodes = []
        self.positions = {}
        
    def set_tree_data(self, nodes):
        self.tree_nodes = nodes
        self.calculate_positions()
        self.update()
    
    def calculate_positions(self):
        if not self.tree_nodes:
            return
        
        self.positions = {}
        max_level = self._calculate_level(len(self.tree_nodes) - 1)
        
        max_nodes_at_bottom = 2 ** max_level
        h_spacing = max(50, self.width() // (max_nodes_at_bottom + 1))
        
        for i, node_value in enumerate(self.tree_nodes):
            if node_value is None:
                continue
            
            level = self._calculate_level(i)
            x = self._calculate_x_position(i, h_spacing, max_level)
            y = 40 + level * 60
            
            self.positions[i] = (x, y)
    
    def _calculate_x_position(self, index, h_spacing, max_level):
        level = self._calculate_level(index)
        pos_in_level = index - (2**level - 1)
        
        nodes_at_level = 2 ** level
        total_width = self.width()
        spacing = total_width // (nodes_at_level + 1)
        
        return spacing * (pos_in_level + 1)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if not self.tree_nodes or all(node is None for node in self.tree_nodes):
            painter.setPen(QPen(QColor("#7f8c8d"), 2))
            painter.setFont(QFont("Arial", 12))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Tree is empty")
            return
        
        node_radius = 18
        
        # Draw edges first
        for i, node_value in enumerate(self.tree_nodes):
            if node_value is None or i not in self.positions:
                continue
            
            x, y = self.positions[i]
            
            # Draw edge to left child
            left_child_idx = 2 * i + 1
            if left_child_idx < len(self.tree_nodes) and self.tree_nodes[left_child_idx] is not None:
                if left_child_idx in self.positions:
                    left_x, left_y = self.positions[left_child_idx]
                    painter.setPen(QPen(QColor("#34495e"), 1.5))
                    painter.drawLine(x, y + node_radius, left_x, left_y - node_radius)
            
            # Draw edge to right child
            right_child_idx = 2 * i + 2
            if right_child_idx < len(self.tree_nodes) and self.tree_nodes[right_child_idx] is not None:
                if right_child_idx in self.positions:
                    right_x, right_y = self.positions[right_child_idx]
                    painter.setPen(QPen(QColor("#34495e"), 1.5))
                    painter.drawLine(x, y + node_radius, right_x, right_y - node_radius)
        
        # Draw nodes
        for i, node_value in enumerate(self.tree_nodes):
            if node_value is None or i not in self.positions:
                continue
            
            x, y = self.positions[i]
            
            # Draw node circle
            painter.setBrush(QBrush(QColor("#3498db")))
            painter.setPen(QPen(QColor("#2c3e50"), 1.5))
            painter.drawEllipse(x - node_radius, y - node_radius, node_radius * 2, node_radius * 2)
            
            # Draw node value
            painter.setPen(QPen(QColor("white")))
            painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            
            display_value = str(node_value)
            if len(display_value) > 4:
                display_value = display_value[:3] + "..."
            
            painter.drawText(x - node_radius, y - node_radius, node_radius * 2, node_radius * 2, 
                           Qt.AlignmentFlag.AlignCenter, display_value)
    
    def _calculate_level(self, index):
        if index < 0:
            return 0
        return int(math.log2(index + 1))


class BinaryTreePage(QWidget):
    def __init__(self):
        super().__init__()
        self.tree = Tree()
        
        layout = QVBoxLayout()
        
        title = QLabel("🌳 Binary Tree")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("A Binary Tree where each node has at most two children (left and right)!")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Input area
        input_layout = QHBoxLayout()
        self.tree_input = QLineEdit()
        self.tree_input.setPlaceholderText("Enter a value")
        input_layout.addWidget(self.tree_input)
        
        add_btn = QPushButton("Add Node")
        add_btn.clicked.connect(self.add_node)
        add_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        input_layout.addWidget(add_btn)
        
        del_btn = QPushButton("Delete Node")
        del_btn.clicked.connect(self.del_node)
        del_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(del_btn)
        
        layout.addLayout(input_layout)
        
        # Traversal buttons
        traversal_layout = QHBoxLayout()
        inorder_btn = QPushButton("In-Order")
        inorder_btn.clicked.connect(lambda: self.show_traversal("in-order"))
        inorder_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        traversal_layout.addWidget(inorder_btn)
        
        preorder_btn = QPushButton("Pre-Order")
        preorder_btn.clicked.connect(lambda: self.show_traversal("pre-order"))
        preorder_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 8px;")
        traversal_layout.addWidget(preorder_btn)
        
        postorder_btn = QPushButton("Post-Order")
        postorder_btn.clicked.connect(lambda: self.show_traversal("post-order"))
        postorder_btn.setStyleSheet("background-color: #e67e22; color: white; padding: 8px;")
        traversal_layout.addWidget(postorder_btn)
        
        layout.addLayout(traversal_layout)
        
        # Visualization area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.tree_canvas = BinaryTreeCanvas()
        scroll.setWidget(self.tree_canvas)
        layout.addWidget(QLabel("Binary Tree Visualization:"))
        layout.addWidget(scroll)
        
        # Info area
        self.tree_info = QLabel("Tree is empty")
        layout.addWidget(self.tree_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def add_node(self):
        value = self.tree_input.text().strip()
        if value:
            try:
                try:
                    value = int(value)
                except ValueError:
                    pass
                self.tree.insert(value)
                self.tree_input.clear()
                self.update_display()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not add node: {str(e)}")

    def del_node(self):
        value = self.tree_input.text().strip()
        if value:
            try:
                try:
                    value = int(value)
                except ValueError:
                    pass
                self.tree.root = self.tree.delNode(self.tree.root, value)
                self.tree_input.clear()
                self.update_display()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not delete node: {str(e)}")
    
    def show_traversal(self, order):
        if self.tree.root is None:
            QMessageBox.information(self, "Empty Tree", "Tree is empty!")
            return
        
        result = []
        
        if order == "in-order":
            self._inorder_collect(self.tree.root, result)
        elif order == "pre-order":
            self._preorder_collect(self.tree.root, result)
        elif order == "post-order":
            self._postorder_collect(self.tree.root, result)
        
        result_str = ", ".join(map(str, result))
        QMessageBox.information(self, f"{order.title()} Traversal", 
                              f"{order.title()}: {result_str}")
    
    def _inorder_collect(self, node, result):
        if node is None:
            return
        self._inorder_collect(node.left, result)
        result.append(node.data)
        self._inorder_collect(node.right, result)
    
    def _preorder_collect(self, node, result):
        if node is None:
            return
        result.append(node.data)
        self._preorder_collect(node.left, result)
        self._preorder_collect(node.right, result)
    
    def _postorder_collect(self, node, result):
        if node is None:
            return
        self._postorder_collect(node.left, result)
        self._postorder_collect(node.right, result)
        result.append(node.data)
    
    def update_display(self):
        nodes = self.tree.levelOrder(self.tree.root)
        self.tree_canvas.set_tree_data(nodes)
        
        actual_node_count = sum(1 for node in nodes if node is not None)
        self.tree_info.setText(f"Nodes: {actual_node_count}")