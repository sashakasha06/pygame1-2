import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt
import random
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("UI.ui", self)
        self.pushButton.clicked.connect(self.button_clicked)
        self.fl = False

    def button_clicked(self):
        self.fl = True
        # Перерисовка окна
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        if self.fl:
            qp.begin(self)
            r = random.randint(10, 50)
            center = (random.randint(50, 450), random.randint(50, 450))
            color = QColor('yellow')
            qp.setBrush(QBrush(color))
            qp.drawEllipse(center[0] - r, center[1] - r, 2 * r, 2 * r)
            qp.end()
        self.fl = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())