import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtGui import QScreen

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("The best Application")

        self.SizeIt()

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False)

        # Also change the window title.
        self.setWindowTitle("My Oneshot App")

    def SizeIt(self):
        w = self.screen().geometry().width()
        h = self.screen().geometry().height()

        self.resize(QSize(0.7*w, 0.7*h))
        self.setGeometry(0.15*w, 0.15*h, 0.7*w, 0.7*h)
        self.setMinimumSize(QSize(0.2*w, 0.2*h))
        self.setMaximumSize(QSize(0.9*w, 0.9*h))

app = QApplication(sys.argv)

window = MainWindow()
window.SizeIt()
window.show()

app.exec()


screen = window.screen() # QtGui.QScreen
print(screen.size()) # разрешение текущего экрана
print(screen.geometry()) # расположение экрана
print(screen.name()) # название, напр. 'BenQ BL2480’
print(screen.physicalSize()) # физ. размер в мм
