import sys

from PySide6 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Bookkeeper Application")
        self.adjust_window_to_screen()


        self.grid = QtWidgets.QGridLayout()

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)

    def set_expense_widget(self, widget: QtWidgets.QTableWidget):
        self.grid.addWidget(widget, 0, 0)

    def set_category_widget(self, widget):
        self.grid.addWidget(widget, 1, 1)

    def set_budget_widget(self, widget):
        self.grid.addWidget(widget, 0, 1)

    def adjust_window_to_screen(self):
        w = self.screen().geometry().width()
        h = self.screen().geometry().height()

        self.resize(QtCore.QSize(0.7*w, 0.7*h))
        self.setGeometry(0.15*w, 0.15*h, 0.7*w, 0.7*h)
        self.setMinimumSize(QtCore.QSize(0.2*w, 0.2*h))
        self.setMaximumSize(QtCore.QSize(0.9*w, 0.9*h))
