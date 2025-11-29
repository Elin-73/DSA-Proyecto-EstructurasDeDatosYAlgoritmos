from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel,
                            QLineEdit, QMessageBox, QScrollArea,
                            QSplitter, QFrame)
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor, QIntValidator
from PyQt6.QtCore import Qt, QPoint
import math


class GraphCanvas(QWidget):
    def __init__(self, title="Grafo", parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 450)
        self.vertices = {}
        self.edges = []
        self.mst_edges = []
        self.title = title
        self.is_mst_view = False
        
    def set_graph_data(self, adjacency_list, mst_edges=None, is_mst_view=False):
        vertices_list = list(adjacency_list.keys())
        n = len(vertices_list)
        
        self.is_mst_view = is_mst_view
        
        if n == 0:
            self.vertices = {}
            self.edges = []
            self.mst_edges = []
            self.update()
            return
        
        self.mst_edges = mst_edges if mst_edges else []
        
        center_x = self.width() // 2
        center_y = (self.height() - 30) // 2 + 30
        radius = min(center_x, center_y - 30) - 60
        
        for i, vertex in enumerate(vertices_list):
            angle = 2 * math.pi * i / n - math.pi / 2
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.vertices[vertex] = (int(x), int(y))
        
        self.edges = []
        for from_vertex, neighbors in adjacency_list.items():
            for to_vertex, weight in neighbors:
                self.edges.append((from_vertex, to_vertex, weight))
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(QBrush(QColor("#34495e")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, 0, self.width(), 30)
        
        painter.setPen(QPen(QColor("white")))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        painter.drawText(0, 0, self.width(), 30, Qt.AlignmentFlag.AlignCenter, self.title)
        
        if not self.vertices:
            painter.setPen(QPen(QColor("#7f8c8d"), 2))
            painter.setFont(QFont("Arial", 12))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Grafo vacío")
            return
        
        node_radius = 22
        
        edges_to_draw = self.edges
        if self.is_mst_view and self.mst_edges:
            mst_set = set()
            for u, v, w in self.mst_edges:
                mst_set.add((u, v, w))
                mst_set.add((v, u, w))
            edges_to_draw = [(u, v, w) for u, v, w in self.edges if (u, v, w) in mst_set or (v, u, w) in mst_set]
        
        # Draw edges
        for from_vertex, to_vertex, weight in edges_to_draw:
            if from_vertex in self.vertices and to_vertex in self.vertices:
                x1, y1 = self.vertices[from_vertex]
                x2, y2 = self.vertices[to_vertex]
                
                # Check if this edge is in MST
                is_mst_edge = (from_vertex, to_vertex, weight) in self.mst_edges or \
                             (to_vertex, from_vertex, weight) in self.mst_edges
                
                # Use different color for MST edges
                if is_mst_edge or self.is_mst_view:
                    painter.setPen(QPen(QColor("#27ae60"), 3))
                else:
                    painter.setPen(QPen(QColor("#7f8c8d"), 2))
                
                # Draw line
                painter.drawLine(x1, y1, x2, y2)
                
                # Draw arrow head
                angle = math.atan2(y2 - y1, x2 - x1)
                arrow_size = 10
                
                end_x = x2 - node_radius * math.cos(angle)
                end_y = y2 - node_radius * math.sin(angle)
                
                arrow_p1_x = end_x - arrow_size * math.cos(angle - math.pi / 6)
                arrow_p1_y = end_y - arrow_size * math.sin(angle - math.pi / 6)
                arrow_p2_x = end_x - arrow_size * math.cos(angle + math.pi / 6)
                arrow_p2_y = end_y - arrow_size * math.sin(angle + math.pi / 6)
                
                if is_mst_edge or self.is_mst_view:
                    painter.setBrush(QBrush(QColor("#27ae60")))
                else:
                    painter.setBrush(QBrush(QColor("#7f8c8d")))
                    
                points = [
                    QPoint(int(end_x), int(end_y)),
                    QPoint(int(arrow_p1_x), int(arrow_p1_y)),
                    QPoint(int(arrow_p2_x), int(arrow_p2_y))
                ]
                painter.drawPolygon(points)
                
                # Draw weight label
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                
                painter.setBrush(QBrush(QColor("white")))
                painter.setPen(QPen(QColor("#7f8c8d"), 1))
                painter.drawEllipse(mid_x - 12, mid_y - 12, 24, 24)
                
                if is_mst_edge or self.is_mst_view:
                    painter.setPen(QPen(QColor("#27ae60")))
                    painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))
                else:
                    painter.setPen(QPen(QColor("#34495e")))
                    painter.setFont(QFont("Arial", 9))
                    
                painter.drawText(mid_x - 12, mid_y - 12, 24, 24,
                               Qt.AlignmentFlag.AlignCenter, str(weight))
        
        # Draw vertices
        for vertex, (x, y) in self.vertices.items():
            painter.setBrush(QBrush(QColor("#e74c3c")))
            painter.setPen(QPen(QColor("#c0392b"), 2))
            painter.drawEllipse(x - node_radius, y - node_radius, node_radius * 2, node_radius * 2)
            
            painter.setPen(QPen(QColor("white")))
            painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            
            display_label = str(vertex)
            if len(display_label) > 3:
                display_label = display_label[:3]
            
            painter.drawText(x - node_radius, y - node_radius, node_radius * 2, node_radius * 2,
                           Qt.AlignmentFlag.AlignCenter, display_label)


class UnionFind:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
    
    def find(self, vertex):
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]
    
    def union(self, v1, v2):
        root1 = self.find(v1)
        root2 = self.find(v2)
        
        if root1 == root2:
            return False
        
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1
        
        return True


class GraphPage(QWidget):
    def __init__(self):
        super().__init__()
        self.graph = {}
        self.mst_edges = []
        self.total_mst_weight = 0
        
        layout = QVBoxLayout()
        
        title = QLabel("🏝 Grafo de distancias entre islas")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("En un archipielago se encuentran varias islas con distintas\n" \
        "distancias entre sí. Se necesita encontrar las rutas de barco más optimas\n" \
        "y minimizar las mismas.\n" \
        "Agregue el nombre de las Islas y la distancia entre cada una, en caso de no\n" \
        "poder haber una ruta entre dos islas deje la distancia entre si sin llenar.\n" \
        "Se recomienda tener una lista de las islas y poner una nomenclatura de 3 caracteres para el Mapa.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Input area
        input_layout = QHBoxLayout()
        self.vertex_input = QLineEdit()
        self.vertex_input.setPlaceholderText("Nombre de Isla")
        self.vertex_input.setMaximumWidth(120)
        input_layout.addWidget(self.vertex_input)
        
        add_vertex_btn = QPushButton("Añadir Isla")
        add_vertex_btn.clicked.connect(self.add_vertex)
        add_vertex_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px;")
        input_layout.addWidget(add_vertex_btn)
        
        input_layout.addSpacing(20)
        
        self.from_vertex = QLineEdit()
        self.from_vertex.setPlaceholderText("Desde")
        self.from_vertex.setMaximumWidth(80)
        input_layout.addWidget(self.from_vertex)
        
        self.to_vertex = QLineEdit()
        self.to_vertex.setPlaceholderText("Hacia")
        self.to_vertex.setMaximumWidth(80)
        input_layout.addWidget(self.to_vertex)
        
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Distancia")
        self.weight_input.setMaximumWidth(70)
        self.weight_input.setValidator(QIntValidator(1, 9999))
        input_layout.addWidget(self.weight_input)
        
        add_edge_btn = QPushButton("Añadir Distancia")
        add_edge_btn.clicked.connect(self.add_edge)
        add_edge_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        input_layout.addWidget(add_edge_btn)
        
        input_layout.addStretch()
        layout.addLayout(input_layout)
        
        # Algorithm buttons
        algo_layout = QHBoxLayout()
        
        kruskal_btn = QPushButton("▶ Correr algoritmo de minimización (kruskal)")
        kruskal_btn.clicked.connect(self.run_kruskal)
        kruskal_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 10px; font-weight: bold;")
        algo_layout.addWidget(kruskal_btn)
        
        clear_mst_btn = QPushButton("Limpiar primer mapa")
        clear_mst_btn.clicked.connect(self.clear_mst)
        clear_mst_btn.setStyleSheet("background-color: #f39c12; color: white; padding: 10px;")
        algo_layout.addWidget(clear_mst_btn)
        
        clear_btn = QPushButton("Limpiar ambos mapas")
        clear_btn.clicked.connect(self.clear_graph)
        clear_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        algo_layout.addWidget(clear_btn)
        
        algo_layout.addStretch()
        layout.addLayout(algo_layout)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        original_frame = QFrame()
        original_frame.setFrameShape(QFrame.Shape.StyledPanel)
        original_layout = QVBoxLayout(original_frame)
        original_layout.setContentsMargins(0, 0, 0, 0)
        
        original_scroll = QScrollArea()
        original_scroll.setWidgetResizable(True)
        self.original_canvas = GraphCanvas("Grafo original")
        original_scroll.setWidget(self.original_canvas)
        original_layout.addWidget(original_scroll)
        
        splitter.addWidget(original_frame)
        
        mst_frame = QFrame()
        mst_frame.setFrameShape(QFrame.Shape.StyledPanel)
        mst_layout = QVBoxLayout(mst_frame)
        mst_layout.setContentsMargins(0, 0, 0, 0)
        
        mst_scroll = QScrollArea()
        mst_scroll.setWidgetResizable(True)
        self.mst_canvas = GraphCanvas("Mapa de rutas optimas")
        mst_scroll.setWidget(self.mst_canvas)
        mst_layout.addWidget(mst_scroll)
        
        splitter.addWidget(mst_frame)
        
        # Set equal sizes
        splitter.setSizes([500, 500])
        
        layout.addWidget(splitter)
        
        # Info area
        self.graph_info = QLabel("Mapa vacío | Añada Islas y Distancias")
        self.graph_info.setStyleSheet("padding: 5px; background-color: #ecf0f1; border-radius: 3px;")
        layout.addWidget(self.graph_info)
        
        self.setLayout(layout)
        self.update_display()
    
    def add_vertex(self):
        vertex = self.vertex_input.text().strip()
        if not vertex:
            QMessageBox.warning(self, "Caja vacía", "Añada nombre para la Isla")
            return
        
        if vertex in self.graph:
            QMessageBox.warning(self, "Duplicado", "Nombre de isla duplicado")
            return
        
        self.graph[vertex] = []
        self.vertex_input.clear()
        self.clear_mst()
        self.update_display()
    
    def add_edge(self):
        from_v = self.from_vertex.text().strip()
        to_v = self.to_vertex.text().strip()
        weight_str = self.weight_input.text().strip()
        
        if not from_v or not to_v or not weight_str:
            QMessageBox.warning(self, "Sin valor", "Rellene las cajas con los valores correspondientes")
            return
        
        try:
            weight = int(weight_str)
            if weight <= 0:
                QMessageBox.warning(self, "Distancia invalida", "Distancia debe ser un entero positivo")
                return
        except ValueError:
            QMessageBox.warning(self, "Distancia invalida", "Distancia debe ser un número entero positivo")
            return
        
        if from_v not in self.graph or to_v not in self.graph:
            QMessageBox.warning(self, "Nombres de Isla invalidos", "Ambos Nombres de Isla deben existir")
            return
        
        if any(neighbor == to_v for neighbor, _ in self.graph[from_v]):
            QMessageBox.warning(self, "Distancia entre Islas duplicados", "Esta ruta ya existe")
            return
        
        self.graph[from_v].append((to_v, weight))
        self.graph[to_v].append((from_v, weight))
        
        self.from_vertex.clear()
        self.to_vertex.clear()
        self.weight_input.clear()
        self.clear_mst()
        self.update_display()
    
    def run_kruskal(self):
        if len(self.graph) < 2:
            QMessageBox.warning(self, "Sin rutas suficientes", 
                              "Se necesitan al menos dos rutas para el algoritmo.")
            return
        
        all_edges = []
        seen_edges = set()
        
        for from_v, neighbors in self.graph.items():
            for to_v, weight in neighbors:
                edge_key = tuple(sorted([from_v, to_v]))
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    all_edges.append((from_v, to_v, weight))
        
        if not all_edges:
            QMessageBox.warning(self, "Sin distancias/rutas", "Mapa sin distancias.")
            return
        
        all_edges.sort(key=lambda x: x[2])
        
        # Run Kruskal's
        uf = UnionFind(self.graph.keys())
        self.mst_edges = []
        self.total_mst_weight = 0
        
        for from_v, to_v, weight in all_edges:
            if uf.union(from_v, to_v):
                self.mst_edges.append((from_v, to_v, weight))
                self.total_mst_weight += weight
                
                if len(self.mst_edges) == len(self.graph) - 1:
                    break
        
        self.update_display()
        
        # Show result
        if len(self.mst_edges) == len(self.graph) - 1:
            edges_str = "\n".join([f"  {u} ─── {v}  (weight: {w})" 
                                  for u, v, w in self.mst_edges])
            QMessageBox.information(self, "Kruskal's MST Result", 
                                  f"✓ Minimum Spanning Tree found!\n\n"
                                  f"MST Edges:\n{edges_str}\n\n"
                                  f"Total Weight: {self.total_mst_weight}")
        else:
            QMessageBox.warning(self, "Disconnected Graph", 
                              f"Graph is disconnected!\n"
                              f"Found {len(self.mst_edges)} edges, need {len(self.graph) - 1} for MST.\n"
                              f"Make sure all vertices are connected.")
    
    def clear_mst(self):
        self.mst_edges = []
        self.total_mst_weight = 0
        self.update_display()
    
    def clear_graph(self):
        self.graph = {}
        self.mst_edges = []
        self.total_mst_weight = 0
        self.update_display()
    
    def update_display(self):
        # Update original graph canvas (shows all edges, MST highlighted)
        self.original_canvas.set_graph_data(self.graph, self.mst_edges, is_mst_view=False)
        
        # Update MST canvas (shows only MST edges)
        self.mst_canvas.set_graph_data(self.graph, self.mst_edges, is_mst_view=True)
        
        vertices_count = len(self.graph)
        edges_count = sum(len(neighbors) for neighbors in self.graph.values()) // 2  # Undirected
        
        info_text = f"Vertices: {vertices_count} | Edges: {edges_count}"
        if self.mst_edges:
            info_text += f" | MST Edges: {len(self.mst_edges)} | MST Total Weight: {self.total_mst_weight}"
        
        self.graph_info.setText(info_text)