import sys
import datetime
import itertools

from PySide6 import QtWidgets, QtGui, QtCore

from typing import Any, Callable

class BudgetWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_data: list[list[str]]
        self.update_callback: Callable
        self.table = QtWidgets.QTableWidget()

        main_layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel('Бюджет')
        main_layout.addWidget(message)
        main_layout.addWidget(self.table)

        self.table.cellChanged.connect(self.on_cell_changed)

        self.last_clicked_cell: tuple(int, int) = (-1, -1)
        self.table.cellClicked.connect(self.on_cell_clicked)

        self.setLayout(main_layout)

    def on_cell_clicked(self, row, column):
        self.last_clicked_cell = (row, column)

    def on_cell_changed(self, row: int, column: int):
        if self.last_clicked_cell == (row, column):
            item = self.table.item(row, column)
            pk = self.user_data[row][0]
            if item.text().isdecimal() and float(item.text()) >= 0:
                self.last_clicked_cell = (-1, -1)
                self.update_callback(pk, item.text())
            else:
                self.last_clicked_cell = (-1, -1)
                self.update_callback(pk, '0')

    def register_update_callback(self, callback: Callable[[str, str], None]):
        self.update_callback = callback

    def set_data(self, user_data: list[list[str]], headers: list[str]):
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

    def _update_visual_content(self):
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

        for i, j in itertools.product(range(n_rows), range(n_cols)):
            item = QtWidgets.QTableWidgetItem(self.user_data[i][j+1])
            if j == 2: # limit column
                item.setFlags(
                    QtCore.Qt.ItemFlag.ItemIsEditable | 
                    QtCore.Qt.ItemFlag.ItemIsSelectable | 
                    QtCore.Qt.ItemFlag.ItemIsEnabled)
                
            else:
                item.setFlags(
                    QtCore.Qt.ItemFlag.ItemIsSelectable | 
                    QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(i, j, item)

