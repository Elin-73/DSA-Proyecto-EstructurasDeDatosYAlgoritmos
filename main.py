from MainWindow import *
from PyQt6.QtWidgets import QApplication

# Import your data structure classes here
# Example:
# from your_file import Stack, Queue, Array, CircularLinkedList, BinaryTree, Graph

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())