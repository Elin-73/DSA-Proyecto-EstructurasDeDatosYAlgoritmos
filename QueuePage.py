from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel,
                            QTextEdit, QLineEdit, QMessageBox)
from PyQt6.QtGui import QFont

from Estructuras import Queue

class QueuePage(QWidget):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
        
        layout = QVBoxLayout()
        
        title = QLabel("🎫 Cola (FIFO - Primero en entrar es el primero en salir)")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("Las colas se pueden ejemplificar sobre colas hacia cajas registradoras." \
        "               El primero en llegar es el primero en ser atendido")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Input area
        input_layout = QHBoxLayout()
        self.queue_input = QLineEdit()
        self.queue_input.setPlaceholderText("Ingrese el nombre del cliente")
        input_layout.addWidget(self.queue_input)
        
        enqueue_btn = QPushButton("Encolar (añadir)")
        enqueue_btn.clicked.connect(self.enqueue)
        enqueue_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        input_layout.addWidget(enqueue_btn)
        
        dequeue_btn = QPushButton("descolar (remover)")
        dequeue_btn.clicked.connect(self.dequeue)
        dequeue_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(dequeue_btn)
        
        front_btn = QPushButton("Frente")
        front_btn.clicked.connect(self.peek_front)
        front_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        input_layout.addWidget(front_btn)
        
        layout.addLayout(input_layout)
        
        self.queue_display = QTextEdit()
        self.queue_display.setReadOnly(True)
        self.queue_display.setMaximumHeight(150)
        layout.addWidget(QLabel("Visualización de la cola:"))
        layout.addWidget(self.queue_display)
        
        self.queue_info = QLabel("Cola vacía")
        layout.addWidget(self.queue_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def enqueue(self):
        value = self.queue_input.text().strip()
        if value:
            self.queue.enqueue(value)
            self.queue_input.clear()
            self.update_display()
    
    def dequeue(self):
        return_value = self.queue.dequeue()
        if return_value == "Queue is empty":
            QMessageBox.warning(self, "Cola Vacía", "La cola está Vacía")
        else:
            QMessageBox.information(self, "Descolado", f"Cliente Removido: {return_value}")
            self.update_display()
    
    def peek_front(self):
        return_value = self.queue.peek()
        if return_value == "Queue is empty":
            QMessageBox.warning(self, "Cola Vacía", "La cola está Vacía")
        else:
            QMessageBox.information(self, "Frente", f"Cliente en el frente: {return_value}")
    
    def update_display(self):
        display = self.queue.toList()
        self.queue_display.setText(display)
        self.queue_info.setText(f"Tamaño: {self.queue.size()}")