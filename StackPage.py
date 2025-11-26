from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton,
                            QLabel, QTextEdit, QLineEdit, QMessageBox)
from PyQt6.QtGui import QFont

from Estructuras import Stack

class StackPage(QWidget):
    def __init__(self):
        super().__init__()
        self.stack = Stack()
        
        layout = QVBoxLayout()
        
        title = QLabel("📚 Pila (LIFO - Último en entrar es el primero en salir)")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("Una pila es común en la vida cotidiana, ejemplo:" \
                    "Al apilar libros para ordenarlos.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        input_layout = QHBoxLayout()
        self.stack_input = QLineEdit()
        self.stack_input.setPlaceholderText("Ingresar título del libro")
        input_layout.addWidget(self.stack_input)
        
        push_btn = QPushButton("Ingresar")
        push_btn.clicked.connect(self.push_stack)
        push_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        input_layout.addWidget(push_btn)
        
        pop_btn = QPushButton("Quitar cima")
        pop_btn.clicked.connect(self.pop_stack)
        pop_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(pop_btn)
        
        peek_btn = QPushButton("Ver cima")
        peek_btn.clicked.connect(self.peek_stack)
        peek_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
        input_layout.addWidget(peek_btn)
        
        layout.addLayout(input_layout)
        
        self.stack_display = QTextEdit()
        self.stack_display.setReadOnly(True)
        self.stack_display.setMaximumHeight(300)
        layout.addWidget(QLabel("Visualización de Pila:"))
        layout.addWidget(self.stack_display)
        
        self.stack_info = QLabel("Pila Vacía")
        layout.addWidget(self.stack_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def push_stack(self):
        value = self.stack_input.text().strip()
        if value:
            self.stack.push(value)
            self.stack_input.clear()
            self.update_display()
    
    def pop_stack(self):
        value = self.stack.pop()
        if value == "Stack is empty":
            QMessageBox.warning(self, "Pila Vacía", "No hay libros en la pila.")
        else:
            QMessageBox.information(self, "Despilado", f"Libro removido: {value}")
            self.update_display()
    
    def peek_stack(self):
        value = self.stack.peek()
        if value == "Stack is empty":
            QMessageBox.warning(self, "Pila Vacía", "No hay libros en la pila.")
        else:
            QMessageBox.information(self, "Cima de libros", f"Libro en la cima de libros: {value}")
    
    def update_display(self):
        stack_list = self.stack.toList()
        
        display = "Visualización de la pila:\n"
        display += stack_list
        
        self.stack_display.setText(display)
        self.stack_info.setText(f"Tamaño: {self.stack.size()} | Cima: {self.stack.peek() if not self.stack.isEmpty() else 'None'}")