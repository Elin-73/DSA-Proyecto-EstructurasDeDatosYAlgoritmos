from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel,
                            QLineEdit, QMessageBox, QScrollArea)
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor, QIntValidator
from PyQt6.QtCore import Qt
import math

from Estructuras import Tree


class BinaryTreeCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1200, 700)  # Larger canvas
        self.tree_nodes = []
        self.positions = {}
        
    def set_tree_data(self, nodes):
        self.tree_nodes = nodes
        self.calculate_positions()
        self.update()
    
    def calculate_positions(self):
        if not self.tree_nodes:
            self.positions = {}
            return
        
        self.positions = {}
        max_level = self._calculate_level(len(self.tree_nodes) - 1)
        
        # Dynamic sizing based on tree depth
        vertical_spacing = min(70, 500 // (max_level + 1))
        
        for i, node_value in enumerate(self.tree_nodes):
            if node_value is None:
                continue
            
            level = self._calculate_level(i)
            pos_in_level = i - (2**level - 1)
            nodes_at_level = 2 ** level
            
            # Calculate x position with dynamic spacing
            spacing = self.width() // (nodes_at_level + 1)
            x = spacing * (pos_in_level + 1)
            y = 50 + level * vertical_spacing
            
            self.positions[i] = (x, y)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), QColor("#f8f9fa"))
        
        if not self.tree_nodes or all(node is None for node in self.tree_nodes):
            painter.setPen(QPen(QColor("#7f8c8d"), 2))
            painter.setFont(QFont("Arial", 14))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Tree is empty\nAdd nodes to visualize")
            return
        
        node_radius = 20
        
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
                    painter.setPen(QPen(QColor("#3498db"), 2))
                    painter.drawLine(x, y + node_radius, left_x, left_y - node_radius)
            
            # Draw edge to right child
            right_child_idx = 2 * i + 2
            if right_child_idx < len(self.tree_nodes) and self.tree_nodes[right_child_idx] is not None:
                if right_child_idx in self.positions:
                    right_x, right_y = self.positions[right_child_idx]
                    painter.setPen(QPen(QColor("#e74c3c"), 2))
                    painter.drawLine(x, y + node_radius, right_x, right_y - node_radius)
        
        # Draw nodes
        for i, node_value in enumerate(self.tree_nodes):
            if node_value is None or i not in self.positions:
                continue
            
            x, y = self.positions[i]
            
            # Determine node color (root is different)
            if i == 0:
                painter.setBrush(QBrush(QColor("#27ae60")))  # Green for root
                painter.setPen(QPen(QColor("#1e8449"), 2))
            else:
                painter.setBrush(QBrush(QColor("#3498db")))  # Blue for others
                painter.setPen(QPen(QColor("#2c3e50"), 2))
            
            painter.drawEllipse(x - node_radius, y - node_radius, node_radius * 2, node_radius * 2)
            
            # Draw node value
            painter.setPen(QPen(QColor("white")))
            painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            
            display_value = str(node_value)
            if len(display_value) > 4:
                display_value = display_value[:3] + ".."
            
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
        
        title = QLabel("🌳 Árbol Binario")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("Árbol binario gráfico. Ingrese cualquier número para que sea agregado al árbol")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Input area
        input_layout = QHBoxLayout()
        self.tree_input = QLineEdit()
        self.tree_input.setPlaceholderText("Ingrese entero")
        self.tree_input.setValidator(QIntValidator())
        self.tree_input.setMaximumWidth(150)
        input_layout.addWidget(self.tree_input)
        
        add_btn = QPushButton("Añadir valor")
        add_btn.clicked.connect(self.add_node)
        add_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        input_layout.addWidget(add_btn)
        
        del_btn = QPushButton("Eliminar valor")
        del_btn.clicked.connect(self.del_node)
        del_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(del_btn)
        
        search_btn = QPushButton("Buscar valor")
        search_btn.clicked.connect(self.search_node)
        search_btn.setStyleSheet("background-color: #f39c12; color: white; padding: 10px;")
        input_layout.addWidget(search_btn)
        
        clear_btn = QPushButton("Limpiar Árbol")
        clear_btn.clicked.connect(self.clear_tree)
        clear_btn.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")
        input_layout.addWidget(clear_btn)
        
        input_layout.addStretch()
        layout.addLayout(input_layout)
        
        # Traversal buttons
        traversal_layout = QHBoxLayout()
        
        traversal_label = QLabel("Traversales:")
        traversal_label.setStyleSheet("font-weight: bold;")
        traversal_layout.addWidget(traversal_label)
        
        inorder_btn = QPushButton("In-Orden")
        inorder_btn.clicked.connect(lambda: self.show_traversal("in-orden"))
        inorder_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        traversal_layout.addWidget(inorder_btn)
        
        preorder_btn = QPushButton("Pre-Orden")
        preorder_btn.clicked.connect(lambda: self.show_traversal("pre-orden"))
        preorder_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 8px;")
        traversal_layout.addWidget(preorder_btn)
        
        postorder_btn = QPushButton("Post-Orden")
        postorder_btn.clicked.connect(lambda: self.show_traversal("post-orden"))
        postorder_btn.setStyleSheet("background-color: #e67e22; color: white; padding: 8px;")
        traversal_layout.addWidget(postorder_btn)
        
        traversal_layout.addStretch()
        layout.addLayout(traversal_layout)
        
        # Visualization area with scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(500)
        self.tree_canvas = BinaryTreeCanvas()
        scroll.setWidget(self.tree_canvas)
        
        layout.addWidget(QLabel("Visualización de Árbol:"))
        layout.addWidget(scroll)
        
        # Info area
        self.tree_info = QLabel("Árbol vacío")
        self.tree_info.setStyleSheet("padding: 5px; background-color: #ecf0f1; border-radius: 3px;")
        layout.addWidget(self.tree_info)
        
        self.setLayout(layout)
        self.update_display()
    
    def add_node(self):
        value = self.tree_input.text().strip()
        if not value:
            QMessageBox.warning(self, "Valor ingresado vacío", "Introduzca algún número entero")
            return
        
        try:
            int_value = int(value)
            self.tree.insert(int_value)
            self.tree_input.clear()
            self.update_display()
        except ValueError:
            QMessageBox.warning(self, "Valor inválido", "Ingrese un número entero")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo agregar: {str(e)}")

    def del_node(self):
        value = self.tree_input.text().strip()
        if not value:
            QMessageBox.warning(self, "Valor vacío", "Ingrese número entero a eliminar")
            return
        
        try:
            int_value = int(value)
            
            # Check if node exists
            if self.tree.search(self.tree.root, int_value) is None:
                QMessageBox.warning(self, "No encontrado", f"Valor {int_value} no encontrado en el Árbol")
                return
            
            self
            self.tree.root = self.tree.delNode(self.tree.root, int_value)
            self.tree_input.clear()
            QMessageBox.information(self, "Eliminado", f"valor {int_value} eliminado exitosamente")
            self.update_display()
        except ValueError:
            QMessageBox.warning(self, "Valor inválido", "Ingrese un número entero")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo eliminar el valor: {str(e)}")
    
    def search_node(self):
        value = self.tree_input.text().strip()
        if not value:
            QMessageBox.warning(self, "Valor vacío", "Ingrese número entero a buscar")
            return
        
        try:
            int_value = int(value)
            result = self.tree.search(self.tree.root, int_value)
            
            if result is not None:
                QMessageBox.information(self, "Encontrado", f"✓ Valor {int_value} existe en el Árbol")
            else:
                QMessageBox.information(self, "No encontrado", f"✗ Valor {int_value} no encontrado en el Árbol")
        except ValueError:
            QMessageBox.warning(self, "Valor inválido", "Ingrese número entero")
    
    def clear_tree(self):
        self.tree = Tree()
        self.update_display()
        QMessageBox.information(self, "Podado", "Árbol podado")
    
    def show_traversal(self, order):
        if self.tree.root is None:
            QMessageBox.information(self, "Árbol vacío", "El Árbol se encuentra vacío")
            return
        
        result = []
        
        if order == "in-orden":
            self._inorder_collect(self.tree.root, result)
            description = "Izquierda → Raíz → Derecho"
        elif order == "pre-orden":
            self._preorder_collect(self.tree.root, result)
            description = "Raíz → Izquierda → Derecho"
        elif order == "post-orden":
            self._postorder_collect(self.tree.root, result)
            description = "Izquierda → Derecho → Raíz"
        
        result_str = " → ".join(map(str, result))
        QMessageBox.information(self, f"{order.title()} Traversal", 
                              f"Orden: {description}\n\nResultado:\n{result_str}")
    
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
        
        if actual_node_count == 0:
            self.tree_info.setText("Árbol vacío | Añada valores para iniciar")
        else:
            height = self.tree.getHeight(self.tree.root, 0)
            self.tree_info.setText(f"Nodos: {actual_node_count} | Altura: {height}")