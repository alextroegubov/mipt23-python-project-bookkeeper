""" Widgets for displaying budget"""
import itertools
from typing import Callable

from PySide6 import QtWidgets, QtCore



class BudgetWidget(QtWidgets.QWidget):
    """ Widget for displaying budget"""
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)

        self.user_data: list[list[str]]
        self.update_callback: Callable[[str, str], None]
        self.table = QtWidgets.QTableWidget()

        main_layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel('Бюджет')
        main_layout.addWidget(message)
        main_layout.addWidget(self.table)

        self.table.cellChanged.connect(self.on_cell_changed)

        self.last_clicked_cell: tuple[int, int] = (-1, -1)
        self.table.cellClicked.connect(self.on_cell_clicked)

        self.setLayout(main_layout)

    def on_cell_clicked(self, row: int, column: int) -> None:
        """ Triggers on cell clicked"""
        self.last_clicked_cell = (row, column)

    def on_cell_changed(self, row: int, column: int) -> None:
        """ Triggers on cell changed"""
        if self.last_clicked_cell == (row, column):
            item = self.table.item(row, column)
            pk = self.user_data[row][0]

            if item.text().isdecimal() and float(item.text()) >= 0:
                self.update_callback(pk, item.text())
            else:
                self.update_callback(pk, '0')

            self.last_clicked_cell = (-1, -1)

    def register_update_callback(self, callback: Callable[[str, str], None]) -> None:
        """ Register update callback"""
        self.update_callback = callback

    def set_data(self, user_data: list[list[str]], headers: list[str]) -> None:
        """
        Set user data to be displayed.
        The first element in each row is considered as a primary
        and is not displayed.
        Primary key is used in callbacks.
        """
        self.user_data = user_data
        self.table.setRowCount(len(self.user_data))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self._update_visual_content()

    def _update_visual_content(self) -> None:
        """ Update table widget"""
        n_rows = self.table.rowCount()
        n_cols = self.table.columnCount()

        # Qt.NoItemFlags          0   It does not have any properties set.
        # Qt.ItemIsSelectable     1   It can be selected.
        # Qt.ItemIsEditable       2   It can be edited.
        # Qt.ItemIsDragEnabled    4   It can be dragged.
        # Qt.ItemIsDropEnabled    8   It can be used as a drop target.
        # Qt.ItemIsUserCheckable  16  It can be checked or unchecked by the user.
        # Qt.ItemIsEnabled        32  The user can interact with the item.
        # Qt.ItemIsTristate

        for row, col in itertools.product(range(n_rows), range(n_cols)):
            item = QtWidgets.QTableWidgetItem(self.user_data[row][col+1])
            if col == 2:  # limit column
                item.setFlags(
                    QtCore.Qt.ItemFlag.ItemIsEditable |
                    QtCore.Qt.ItemFlag.ItemIsSelectable |
                    QtCore.Qt.ItemFlag.ItemIsEnabled)
            else:
                item.setFlags(
                    QtCore.Qt.ItemFlag.ItemIsSelectable |
                    QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(row, col, item)
