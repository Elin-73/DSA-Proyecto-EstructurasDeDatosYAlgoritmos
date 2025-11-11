from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel,
                            QTextEdit, QLineEdit)
from PyQt6.QtGui import QFont

class BinaryTreePage(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize your BinaryTree class here
        # self.tree = BinaryTree()
        
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
        
        clear_btn = QPushButton("Clear Tree")
        clear_btn.clicked.connect(self.clear_tree)
        clear_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(clear_btn)
        
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
        self.tree_display = QTextEdit()
        self.tree_display.setReadOnly(True)
        self.tree_display.setMaximumHeight(300)
        layout.addWidget(QLabel("Binary Tree Visualization:"))
        layout.addWidget(self.tree_display)
        
        # Info area
        self.tree_info = QLabel("Tree is empty")
        layout.addWidget(self.tree_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def add_node(self):
        value = self.tree_input.text().strip()
        if value:
            # self.tree.insert(value)
            self.tree_input.clear()
            self.update_display()
    
    def clear_tree(self):
        # self.tree.clear()
        self.update_display()
    
    def show_traversal(self, order):
        # result = ""
        # if order == "in-order":
        #     result = self.tree.inorder()
        # elif order == "pre-order":
        #     result = self.tree.preorder()
        # elif order == "post-order":
        #     result = self.tree.postorder()
        # QMessageBox.information(self, f"{order.title()} Traversal", f"{order.title()}: {result}")
        pass
    
    def update_display(self):
        display = "       Root\n"
        display += "      /  \\\n"
        display += "   Left  Right\n"
        display += "   / \\   / \\\n"
        display += "  L1 L2 R1 R2"
        self.tree_display.setText(display)