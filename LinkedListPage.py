from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel,
                            QTextEdit, QLineEdit, QMessageBox, QSpinBox)
from PyQt6.QtGui import QFont, QIntValidator

from Estructuras import CircularList

class CircularLinkedListPage(QWidget):
    def __init__(self):
        super().__init__()
        self.cll = CircularList()
        
        layout = QVBoxLayout()
        
        title = QLabel("🔄📚 Lista de libros prestados")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("La biblioteca presta varios libros a lo largo del año\n" \
        "y los clientes necesitan saber si el libro que buscan se encuentra\n" \
        "en disponibilidad o no.\nAgregue los libros prestados a la lista.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # First input row - Add to end
        input_layout1 = QHBoxLayout()
        self.cll_input = QLineEdit()
        self.cll_input.setPlaceholderText("Ingresar nombre de libro")
        input_layout1.addWidget(self.cll_input)
        
        add_btn = QPushButton("Añadir al final")
        add_btn.clicked.connect(self.add_node)
        add_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        input_layout1.addWidget(add_btn)
        
        delete_first_btn = QPushButton("Devolver primero")
        delete_first_btn.clicked.connect(self.delete_node)
        delete_first_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout1.addWidget(delete_first_btn)
        
        layout.addLayout(input_layout1)
        
        # Second input row - Insert/Delete at position
        input_layout2 = QHBoxLayout()
        
        self.position_input = QSpinBox()
        self.position_input.setMinimum(0)
        self.position_input.setMaximum(0)
        self.position_input.setPrefix("Posición: ")
        self.position_input.setMaximumWidth(120)
        input_layout2.addWidget(self.position_input)
        
        self.insert_input = QLineEdit()
        self.insert_input.setPlaceholderText("Nombre del libro")
        input_layout2.addWidget(self.insert_input)
        
        insert_btn = QPushButton("Insertar en posición")
        insert_btn.clicked.connect(self.insert_at_position)
        insert_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 10px;")
        input_layout2.addWidget(insert_btn)
        
        delete_at_btn = QPushButton("Eliminar en posición")
        delete_at_btn.clicked.connect(self.delete_at_position)
        delete_at_btn.setStyleSheet("background-color: #e67e22; color: white; padding: 10px;")
        input_layout2.addWidget(delete_at_btn)
        
        layout.addLayout(input_layout2)
        
        # Third button row - Utilities
        button_layout = QHBoxLayout()
        
        traverse_btn = QPushButton("Lista completa")
        traverse_btn.clicked.connect(self.traverse)
        traverse_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        button_layout.addWidget(traverse_btn)
        
        clear_btn = QPushButton("Limpiar lista")
        clear_btn.clicked.connect(self.clear_list)
        clear_btn.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Visualization
        self.cll_display = QTextEdit()
        self.cll_display.setReadOnly(True)
        self.cll_display.setMaximumHeight(200)
        layout.addWidget(QLabel("Visualización completa de la lista de libros prestados:"))
        layout.addWidget(self.cll_display)
        
        # Info area
        self.cll_info = QLabel("Lista Vacía")
        layout.addWidget(self.cll_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def add_node(self):
        value = self.cll_input.text().strip()
        if not value:
            QMessageBox.warning(self, "Valor vacío", "Por favor ingrese un nombre de libro")
            return
        
        self.cll.push(value)
        self.cll_input.clear()
        self.update_display()
        QMessageBox.information(self, "Añadido", f"Libro '{value}' añadido al final de la lista")
    
    def insert_at_position(self):
        value = self.insert_input.text().strip()
        position = self.position_input.value()
        
        if not value:
            QMessageBox.warning(self, "Valor vacío", "Por favor ingrese un nombre de libro")
            return
        
        result = self.cll.insert_at(position, value)
        
        if result == "Invalid position":
            QMessageBox.warning(self, "Posición inválida", 
                              f"La posición debe estar entre 0 y {self.cll.get_size()}")
            return
        
        self.insert_input.clear()
        self.update_display()
        QMessageBox.information(self, "Insertado", 
                              f"Libro '{value}' insertado en posición {position}")
    
    def delete_node(self):
        removed = self.cll.pop()
        if removed == "List is Empty!":
            QMessageBox.warning(self, "Lista Vacía", "La lista está vacía")
        else:
            QMessageBox.information(self, "Devuelto", f"Libro devuelto: {removed}")
            self.update_display()
    
    def delete_at_position(self):
        position = self.position_input.value()
        
        if self.cll.is_empty():
            QMessageBox.warning(self, "Lista Vacía", "La lista está vacía")
            return
        
        if position >= self.cll.get_size():
            QMessageBox.warning(self, "Posición inválida", 
                              f"La posición debe estar entre 0 y {self.cll.get_size() - 1}")
            return
        
        # Get the book name before deleting
        book_name = self.cll.get_at(position)
        
        removed = self.cll.delete_at(position)
        
        if removed == "List is Empty!" or removed == "Invalid position":
            QMessageBox.warning(self, "Error", "No se pudo eliminar el libro")
        else:
            self.update_display()
            QMessageBox.information(self, "Eliminado", 
                                  f"Libro eliminado de posición {position}: {removed}")
    
    def traverse(self):
        if self.cll.is_empty():
            QMessageBox.information(self, "Lista Vacía", "No hay libros en la lista")
            return
        
        elements = self.cll.traverse()
        if elements:
            book_list = "\n".join([f"Posición {i}: {book}" for i, book in enumerate(elements)])
            QMessageBox.information(self, "Lista completa de libros prestados", 
                                  f"Total de libros: {len(elements)}\n\n{book_list}")
        else:
            QMessageBox.information(self, "Lista Vacía", "No hay libros en la lista")
    
    def clear_list(self):
        if self.cll.is_empty():
            QMessageBox.information(self, "Lista Vacía", "La lista ya está vacía")
            return
        
        reply = QMessageBox.question(self, "Confirmar limpieza", 
                                     "¿Está seguro que desea limpiar toda la lista?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.cll = CircularList()
            self.update_display()
            QMessageBox.information(self, "Limpiado", "Lista ha sido limpiada")
    
    def update_display(self):
        display = self.cll.display()
        self.cll_display.setText(display)
        
        # Update position spinner maximum
        max_pos = max(0, self.cll.get_size())
        self.position_input.setMaximum(max_pos)
        
        if self.cll.is_empty():
            self.cll_info.setText("Lista vacía | No hay libros prestados")
        else:
            self.cll_info.setText(f"Libros totales prestados: {self.cll.get_size()} | " \
                                f"Posiciones válidas: 0 a {self.cll.get_size() - 1}")