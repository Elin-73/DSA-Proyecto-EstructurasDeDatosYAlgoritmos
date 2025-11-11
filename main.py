import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from estructuras import Stack, Queue


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")

        # Set the central widget of the Window.
        self.setCentralWidget(button)


def main() -> None:
  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  app.exec()

if __name__ == "__main__":
  main()