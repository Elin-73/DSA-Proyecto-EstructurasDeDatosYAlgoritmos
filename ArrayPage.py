from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton,
                            QLabel, QTextEdit,
                            QLineEdit, QMessageBox)
from PyQt6.QtGui import QFont, QIntValidator


class ArrayPage(QWidget):
    def __init__(self):
        super().__init__()
        self.array = []
        self.sorted = False
        
        layout = QVBoxLayout()
        
        title = QLabel("📊 Arreglo de clientes")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("En este arreglo se van a almacenar el número de cuenta\n" \
        "de los clientes de la librería, todos aquellos que tengan su tarjeta\n" \
        "de bliblioteca a la mano pueden ser atendidos.\n" \
        "Esta medida es provisional hasta la implementación de una base de datos formal.\n" \
        "Agregue el número de cuenta de los clientes según se vayan registrando.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Input area
        input_layout = QHBoxLayout()
        self.array_input = QLineEdit()
        self.array_input.setPlaceholderText("Ingrese un número")
        self.array_input.setValidator(QIntValidator())
        input_layout.addWidget(self.array_input)
        
        self.index_input = QLineEdit()
        self.index_input.setPlaceholderText("Índice")
        self.index_input.setMaximumWidth(80)
        self.index_input.setValidator(QIntValidator(0, 999999))
        input_layout.addWidget(self.index_input)
        
        add_btn = QPushButton("Añadir")
        add_btn.clicked.connect(self.add_element)
        add_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        input_layout.addWidget(add_btn)
        
        insert_btn = QPushButton("Insertar en Índice")
        insert_btn.clicked.connect(self.insert_element)
        insert_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 10px;")
        input_layout.addWidget(insert_btn)
        
        delete_btn = QPushButton("Eliminar el Índice")
        delete_btn.clicked.connect(self.delete_element)
        delete_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        input_layout.addWidget(delete_btn)
        
        layout.addLayout(input_layout)
        
        button_layout = QHBoxLayout()
        
        search_btn = QPushButton("Búsqueda Binaria")
        search_btn.clicked.connect(self.binary_search)
        search_btn.setStyleSheet("background-color: #f1c40f; color: black; padding: 10px;")
        button_layout.addWidget(search_btn)

        sort_btn = QPushButton("Ordenamiento Shell")
        sort_btn.clicked.connect(self.shell_sort)
        sort_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
        button_layout.addWidget(sort_btn)
        
        clear_btn = QPushButton("Limpiar Arreglo")
        clear_btn.clicked.connect(self.clear_array)
        clear_btn.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
        self.array_display = QTextEdit()
        self.array_display.setReadOnly(True)
        self.array_display.setMaximumHeight(200)
        layout.addWidget(QLabel("Visualización de Arreglo:"))
        layout.addWidget(self.array_display)
        
        self.array_info = QLabel("Arreglo Vacío")
        layout.addWidget(self.array_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def add_element(self):
        value = self.array_input.text().strip()
        if value:
            try:
                int_value = int(value)
                self.array.append(int_value)
                self.array_input.clear()
                self.sorted = False
                self.update_display()
            except ValueError:
                QMessageBox.warning(self, "Valor Ingresado Inválido", "Porfavor ingrese un número entero")
        else:
            QMessageBox.warning(self, "Valor vacío", "Ingrese un valor válido")
    
    def insert_element(self):
        value = self.array_input.text().strip()
        index_str = self.index_input.text().strip()
        
        if not value:
            QMessageBox.warning(self, "Valor vacío", "Ingrese valor")
            return
        
        if not index_str:
            QMessageBox.warning(self, "Índice vacío", "Ingrese Índice")
            return
        
        try:
            int_value = int(value)
            index = int(index_str)
            
            if 0 <= index <= len(self.array):
                self.array.insert(index, int_value)
                self.array_input.clear()
                self.index_input.clear()
                self.sorted = False
                self.update_display()
            else:
                QMessageBox.warning(self, "Índice inválido", f"El valor del Índice debe encontrarse en medio de 0 y {len(self.array)}")
        except ValueError:
            QMessageBox.warning(self, "Valor ingresado inválido", "Ambos valores deben ser Enteros")
    
    def delete_element(self):
        index_str = self.index_input.text().strip()
        
        if not index_str:
            QMessageBox.warning(self, "Índice vacío", "Porfavor Ingrese índice")
            return
        
        try:
            index = int(index_str)
            if 0 <= index < len(self.array):
                removed = self.array.pop(index)
                self.index_input.clear()
                self.sorted = False
                QMessageBox.information(self, "Eliminado", f"Valor Eliminado: {removed}")
                self.update_display()
            else:
                if len(self.array) == 0:
                    QMessageBox.warning(self, "Arreglo vacío", "El arreglo está vacío.")
                else:
                    QMessageBox.warning(self, "Índice inválido", f"El valor del Índice debe encontrarse en medio de 0 y {len(self.array)-1}")
        except ValueError:
            QMessageBox.warning(self, "Valor inválido", "Índice debe ser entero")
    
    def clear_array(self):
        self.array = []
        self.sorted = False
        self.update_display()
    
    def update_display(self):
        if self.array:
            indices = "Índices: " + " ".join([f"[{i}]" for i in range(len(self.array))]) + "\n"
            values = "Valores:  " + " ".join([f"[{v}]" for v in self.array])
            display = indices + values
        else:
            display = "Arreglo vacío"
        
        self.array_display.setText(display)
        
        sorted_status = "Ordenado ✓" if self.sorted else "Desordenado"
        self.array_info.setText(f"Tamaño: {len(self.array)} | Se encuentra: {sorted_status}")

    def shell_sort(self):
        if len(self.array) == 0:
            QMessageBox.warning(self, "Arreglo Vacío", "el arreglo está vacío")
            return
        
        if len(self.array) == 1:
            self.sorted = True
            self.update_display()
            QMessageBox.information(self, "Ordenado", "El arreglo solo tiene un elemento, ya se encuentra ordenado.")
            return
        
        array_len = len(self.array)
        gap = array_len // 2
        
        while gap > 0:
            for i in range(gap, array_len):
                temp = self.array[i]
                j = i
                while j >= gap and self.array[j - gap] > temp:
                    self.array[j] = self.array[j - gap]
                    j -= gap
                self.array[j] = temp
            gap //= 2
        
        self.sorted = True
        self.update_display()
        QMessageBox.information(self, "Ordenado", "El arreglo ha sido ordenado pormedio de Shell Sort.")

    def binary_search(self):
        if len(self.array) == 0:
            QMessageBox.warning(self, "Arreglo vacío", "El arreglo está vacío")
            return
        
        if not self.sorted:
            QMessageBox.warning(self, "Arreglo desordenado", 
                                    "El arreglo debe estar ordenado primero\nHaga click en Shell para ordenarlo.")
            return
        
        value = self.array_input.text().strip()
        
        if not value:
            QMessageBox.warning(self, "Caja Vacía", "Ponga algún valor para buscar.")
            return
        
        try:
            search_value = int(value)
        except ValueError:
            QMessageBox.warning(self, "Valor inválido", "El valor tiene que ser entero.")
            return
        
        left = 0
        right = len(self.array) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if self.array[mid] == search_value:
                self.array_input.clear()
                QMessageBox.information(self, "Encontrado", 
                                    f"Valor {search_value} encontrado en índice: {mid}")
                return
            elif self.array[mid] < search_value:
                left = mid + 1
            else:
                right = mid - 1
        
        QMessageBox.information(self, "Not Encontrado", 
                            f"El valor {search_value} no fue encontrado en el arreglo.")