from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel,
                            QLineEdit, QMessageBox, QScrollArea)
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QPoint
import math


class GraphCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 500)
        self.vertices = {}
        self.edges = []
        self.mst_edges = []  # Edges that are part of MST
        
    def set_graph_data(self, adjacency_list, mst_edges=None):
        vertices_list = list(adjacency_list.keys())
        n = len(vertices_list)
        
        if n == 0:
            self.vertices = {}
            self.edges = []
            self.mst_edges = []
            self.update()
            return
        
        # Store MST edges if provided
        self.mst_edges = mst_edges if mst_edges else []
        
        # Position vertices in a circle
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(center_x, center_y) - 80
        
        for i, vertex in enumerate(vertices_list):
            angle = 2 * math.pi * i / n - math.pi / 2
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.vertices[vertex] = (int(x), int(y))
        
        # Build edge list
        self.edges = []
        for from_vertex, neighbors in adjacency_list.items():
            for to_vertex, weight in neighbors:
                self.edges.append((from_vertex, to_vertex, weight))
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if not self.vertices:
            painter.setPen(QPen(QColor("#7f8c8d"), 2))
            painter.setFont(QFont("Arial", 12))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Graph is empty")
            return
        
        node_radius = 25
        
        # Draw edges first
        for from_vertex, to_vertex, weight in self.edges:
            if from_vertex in self.vertices and to_vertex in self.vertices:
                x1, y1 = self.vertices[from_vertex]
                x2, y2 = self.vertices[to_vertex]
                
                # Check if this edge is in MST
                is_mst_edge = (from_vertex, to_vertex, weight) in self.mst_edges or \
                             (to_vertex, from_vertex, weight) in self.mst_edges
                
                # Use different color for MST edges
                if is_mst_edge:
                    painter.setPen(QPen(QColor("#27ae60"), 4))  # Green and thicker for MST
                else:
                    painter.setPen(QPen(QColor("#34495e"), 2))  # Normal gray
                
                # Draw line
                painter.drawLine(x1, y1, x2, y2)
                
                # Draw arrow head
                angle = math.atan2(y2 - y1, x2 - x1)
                arrow_size = 12
                
                # Calculate arrow endpoint
                end_x = x2 - node_radius * math.cos(angle)
                end_y = y2 - node_radius * math.sin(angle)
                
                # Arrow points
                arrow_p1_x = end_x - arrow_size * math.cos(angle - math.pi / 6)
                arrow_p1_y = end_y - arrow_size * math.sin(angle - math.pi / 6)
                arrow_p2_x = end_x - arrow_size * math.cos(angle + math.pi / 6)
                arrow_p2_y = end_y - arrow_size * math.sin(angle + math.pi / 6)
                
                if is_mst_edge:
                    painter.setBrush(QBrush(QColor("#27ae60")))
                else:
                    painter.setBrush(QBrush(QColor("#34495e")))
                    
                points = [
                    QPoint(int(end_x), int(end_y)),
                    QPoint(int(arrow_p1_x), int(arrow_p1_y)),
                    QPoint(int(arrow_p2_x), int(arrow_p2_y))
                ]
                painter.drawPolygon(points)
                
                # Draw weight label in the middle of the edge
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                
                # Draw background for weight text
                painter.setBrush(QBrush(QColor("#ecf0f1")))
                painter.setPen(QPen(QColor("#7f8c8d"), 1))
                painter.drawEllipse(mid_x - 15, mid_y - 15, 30, 30)
                
                # Draw weight text
                if is_mst_edge:
                    painter.setPen(QPen(QColor("#27ae60")))
                    painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                else:
                    painter.setPen(QPen(QColor("#34495e")))
                    painter.setFont(QFont("Arial", 9))
                    
                painter.drawText(mid_x - 15, mid_y - 15, 30, 30,
                               Qt.AlignmentFlag.AlignCenter, str(weight))
        
        # Draw vertices
        for vertex, (x, y) in self.vertices.items():
            # Draw circle
            painter.setBrush(QBrush(QColor("#e74c3c")))
            painter.setPen(QPen(QColor("#c0392b"), 2))
            painter.drawEllipse(x - node_radius, y - node_radius, node_radius * 2, node_radius * 2)
            
            # Draw vertex label
            painter.setPen(QPen(QColor("white")))
            painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            
            # Truncate long labels
            display_label = str(vertex)
            if len(display_label) > 3:
                display_label = display_label[:3] + "..."
            
            painter.drawText(x - node_radius, y - node_radius, node_radius * 2, node_radius * 2,
                           Qt.AlignmentFlag.AlignCenter, display_label)


class UnionFind:
    """Union-Find (Disjoint Set Union) data structure for Kruskal's algorithm"""
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
    
    def find(self, vertex):
        """Find the root of the set containing vertex (with path compression)"""
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]
    
    def union(self, v1, v2):
        """Union two sets containing v1 and v2 (union by rank)"""
        root1 = self.find(v1)
        root2 = self.find(v2)
        
        if root1 == root2:
            return False  # Already in same set
        
        # Union by rank
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
        # Graph stored as adjacency list with weights: {vertex: [(neighbor, weight), ...]}
        self.graph = {}
        self.mst_edges = []  # Store MST edges
        self.total_mst_weight = 0
        
        layout = QVBoxLayout()
        
        title = QLabel("🕸️ Graph (Weighted Directed Graph)")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("A weighted graph for Kruskal's Minimum Spanning Tree algorithm!")
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
        
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Weight")
        self.weight_input.setMaximumWidth(80)
        edge_layout.addWidget(self.weight_input)
        
        add_edge_btn = QPushButton("Add Edge")
        add_edge_btn.clicked.connect(self.add_edge)
        add_edge_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
        edge_layout.addWidget(add_edge_btn)
        
        layout.addLayout(edge_layout)
        
        # Algorithm buttons
        algo_layout = QHBoxLayout()
        
        kruskal_btn = QPushButton("Run Kruskal's MST")
        kruskal_btn.clicked.connect(self.run_kruskal)
        kruskal_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 10px;")
        algo_layout.addWidget(kruskal_btn)
        
        clear_mst_btn = QPushButton("Clear MST")
        clear_mst_btn.clicked.connect(self.clear_mst)
        clear_mst_btn.setStyleSheet("background-color: #f39c12; color: white; padding: 10px;")
        algo_layout.addWidget(clear_mst_btn)
        
        clear_btn = QPushButton("Clear Graph")
        clear_btn.clicked.connect(self.clear_graph)
        clear_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        algo_layout.addWidget(clear_btn)
        
        layout.addLayout(algo_layout)
        
        # Visualization area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.graph_canvas = GraphCanvas()
        scroll.setWidget(self.graph_canvas)
        layout.addWidget(QLabel("Graph Visualization (MST edges in green):"))
        layout.addWidget(scroll)
        
        # Info area
        self.graph_info = QLabel("Graph is empty")
        layout.addWidget(self.graph_info)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_display()
    
    def add_vertex(self):
        vertex = self.vertex_input.text().strip()
        if vertex:
            if vertex not in self.graph:
                self.graph[vertex] = []
                self.vertex_input.clear()
                self.update_display()
            else:
                QMessageBox.warning(self, "Duplicate", "Vertex already exists!")
    
    def add_edge(self):
        from_v = self.from_vertex.text().strip()
        to_v = self.to_vertex.text().strip()
        weight_str = self.weight_input.text().strip()
        
        if from_v and to_v and weight_str:
            try:
                weight = int(weight_str)
                
                if from_v in self.graph and to_v in self.graph:
                    # Check if edge already exists
                    if not any(neighbor == to_v for neighbor, _ in self.graph[from_v]):
                        self.graph[from_v].append((to_v, weight))
                        self.from_vertex.clear()
                        self.to_vertex.clear()
                        self.weight_input.clear()
                        self.clear_mst()  # Clear MST when graph changes
                        self.update_display()
                    else:
                        QMessageBox.warning(self, "Duplicate", "Edge already exists!")
                else:
                    QMessageBox.warning(self, "Invalid", "Both vertices must exist first!")
            except ValueError:
                QMessageBox.warning(self, "Invalid Weight", "Weight must be a number!")
    
    def run_kruskal(self):
        """Run Kruskal's algorithm to find Minimum Spanning Tree"""
        if len(self.graph) < 2:
            QMessageBox.warning(self, "Not Enough Vertices", 
                              "Need at least 2 vertices to find MST!")
            return
        
        # Collect all edges (treat as undirected for MST)
        all_edges = []
        seen_edges = set()
        
        for from_v, neighbors in self.graph.items():
            for to_v, weight in neighbors:
                # Create canonical form (smaller vertex first) to avoid duplicates
                edge = tuple(sorted([from_v, to_v]) + [weight])
                if edge not in seen_edges:
                    seen_edges.add(edge)
                    all_edges.append((from_v, to_v, weight))
        
        if not all_edges:
            QMessageBox.warning(self, "No Edges", "Graph has no edges!")
            return
        
        # Sort edges by weight (Kruskal's algorithm)
        all_edges.sort(key=lambda x: x[2])
        
        # Initialize Union-Find
        uf = UnionFind(self.graph.keys())
        
        # Kruskal's algorithm
        self.mst_edges = []
        self.total_mst_weight = 0
        
        for from_v, to_v, weight in all_edges:
            # If vertices are in different sets, add edge to MST
            if uf.union(from_v, to_v):
                self.mst_edges.append((from_v, to_v, weight))
                self.total_mst_weight += weight
                
                # Stop when we have V-1 edges (complete MST)
                if len(self.mst_edges) == len(self.graph) - 1:
                    break
        
        self.update_display()
        
        # Show result
        if len(self.mst_edges) == len(self.graph) - 1:
            edges_str = "\n".join([f"{u} -- {v} (weight: {w})" 
                                  for u, v, w in self.mst_edges])
            QMessageBox.information(self, "Kruskal's MST Result", 
                                  f"Minimum Spanning Tree found!\n\n"
                                  f"Edges in MST:\n{edges_str}\n\n"
                                  f"Total MST Weight: {self.total_mst_weight}")
        else:
            QMessageBox.warning(self, "Disconnected Graph", 
                              f"Graph is disconnected! Found {len(self.mst_edges)} edges.\n"
                              f"Need {len(self.graph) - 1} edges for complete MST.")
    
    def clear_mst(self):
        """Clear the MST highlighting"""
        self.mst_edges = []
        self.total_mst_weight = 0
        self.update_display()
    
    def clear_graph(self):
        self.graph = {}
        self.mst_edges = []
        self.total_mst_weight = 0
        self.update_display()
    
    def update_display(self):
        # Convert to simple adjacency list for canvas
        simple_adj = {v: [(n, w) for n, w in neighbors] 
                     for v, neighbors in self.graph.items()}
        
        self.graph_canvas.set_graph_data(simple_adj, self.mst_edges)
        
        vertices_count = len(self.graph)
        edges_count = sum(len(neighbors) for neighbors in self.graph.values())
        
        info_text = f"Vertices: {vertices_count} | Edges: {edges_count}"
        if self.mst_edges:
            info_text += f" | MST Weight: {self.total_mst_weight}"
        
        self.graph_info.setText(info_text)