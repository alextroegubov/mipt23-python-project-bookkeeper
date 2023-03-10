from PySide6 import QtWidgets, QtCore

class MainWindow(QtWidgets.QMainWindow):
    """ Main window class """
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent=parent)

        self.setWindowTitle("Bookkeeper Application")
        self.adjust_window_to_screen()

        self.grid = QtWidgets.QGridLayout()

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)

    def set_expense_widget(self, widget: QtWidgets.QWidget) -> None:
        self.grid.addWidget(widget, 0, 0)

    def set_category_widget(self, widget: QtWidgets.QWidget) -> None:
        self.grid.addWidget(widget, 1, 1)

    def set_budget_widget(self, widget: QtWidgets.QWidget) -> None:
        self.grid.addWidget(widget, 0, 1)

    def adjust_window_to_screen(self) -> None:
        """ Adjust window size in correspondence with screen size"""
        w = self.screen().geometry().width()
        h = self.screen().geometry().height()

        self.resize(QtCore.QSize(int(0.7*w), int(0.7*h)))
        self.setGeometry(int(0.15*w), int(0.15*h), int(0.7*w), int(0.7*h))
        self.setMinimumSize(QtCore.QSize(int(0.2*w), int(0.2*h)))
        self.setMaximumSize(QtCore.QSize(int(0.9*w), int(0.9*h)))
