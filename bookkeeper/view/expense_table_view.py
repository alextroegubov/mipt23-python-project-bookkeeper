import sys
import datetime
import itertools

from PySide6 import QtWidgets, QtGui, QtCore

from typing import Any, Callable, List, Dict

class InputExpenseWindow(QtWidgets.QDialog):
    """ Window for entering information about new expense """
    def __init__(self, parent, on_clicked_save_callback: Callable, ctg_options: list[str]):
        super().__init__(parent)

        self.on_clicked_save_callback = on_clicked_save_callback
        self.ctg_options = ctg_options

        self.setWindowTitle("Добавление записи о раходах")

        self.layout = QtWidgets.QVBoxLayout()
        self.create_widgets()

        self.save_btn = QtWidgets.QPushButton('Сохранить новую запись')
        self.save_btn.clicked.connect(self.on_clicked_save_btn)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def create_widgets(self):
        """ Create widgets and add them to layout"""
        self.expense_date = QtWidgets.QLineEdit()
        self.expense_date.setPlaceholderText('Дата покупки')
        #todo validator
        self.layout.addWidget(self.expense_date)

        self.amount = QtWidgets.QLineEdit()
        self.amount.setPlaceholderText('Сумма')
        self.amount.setValidator(QtGui.QDoubleValidator(0, 1000000, 2))
        self.layout.addWidget(self.amount)

        self.category = QtWidgets.QComboBox()
        self.category.setPlaceholderText('Категория')
        self.category.addItems(self.ctg_options)
        self.layout.addWidget(self.category)

        self.comment = QtWidgets.QLineEdit()
        self.comment.setPlaceholderText('Комментарий')
        # todo validator
        self.layout.addWidget(self.comment)

    def is_mandatory_filled(self):
        """ Check if mandatory fields are filled"""
        return self.amount.text() and self.category.text()

    def get_data(self):
        """ Get formatted data""" 

        user_input = {
            'expense_date': self.expense_date.text(),
            'amount': self.amount.text(),
            'category': self.category.text(),
            'comment': self.comment.text()
        }

        user_input = [self.expense_date.text(), self.amount.text(),
                      self.category.text(), self.comment.text()]

        return user_input

    def on_clicked_save_btn(self):
        """ Reaction on clicked save button """
        if self.is_mandatory_filled():
            self.on_clicked_save_callback(self.get_data())
            self.close()
        else:
            # TODO show msg
            pass


class MainTableWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_data = [[]]
        self.update_callback: Callable
        self.remove_callback: Callable
        self.add_callback: Callable

        self.table = QtWidgets.QTableWidget()

        add_btn = QtWidgets.QPushButton('Add')
        add_btn.clicked.connect(self.on_clicked_add_button)
        del_btn = QtWidgets.QPushButton('Delete')
        del_btn.clicked.connect(self.on_clicked_del_button)

        # horizontal layout with buttons
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(add_btn)
        h_layout.addWidget(del_btn)

        # buttons under the table
        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addWidget(self.table)
        v_layout.addLayout(h_layout)

        self.table.cellChanged.connect(self.on_cell_changed)

        self.last_clicked_cell: tuple(int, int) = (-1, -1)
        self.table.cellClicked.connect(self.on_cell_clicked)

        self.setLayout(v_layout)

    def on_cell_clicked(self, row, column):
        self.last_clicked_cell = (row, column)
        #print(self.last_clicked_cell)

    def on_cell_changed(self, row, column):
        if self.last_clicked_cell == (row, column):

            items = [self.table.item(row, i) for i in range(self.table.columnCount())]

            new_row_data = [item.data() for item in items]
            pk = self.user_data[row][0]

            self.update_callback(pk, new_row_data)

            self.last_clicked_cell = (-1, -1)


    def on_clicked_add_button(self):
        exp_win = InputExpenseWindow(self, 
            on_clicked_save_callback=self.add_callback,
            ctg_options=self.cat_data)
        exp_win.show()
        #print('Add button clicked!')

#    def _expense_window_callback(self, input_data):
#        self.add_callback(input_data)

    def on_clicked_del_button(self):
        idx = self.table.selectedItems()

        if len(idx) == 0:
            return

        rows = set([i.row() for i in idx])
        pks = [self.user_data[row][0] for row in rows]

        self.remove_callback(pks)

        print(f'Delete button clicked!')

    def register_add_callback(self, callback: Callable[[list[str, str]], None]):
        self.add_callback = callback

    def register_remove_callback(self, callback: Callable[[list[str]], None]):
        self.remove_callback = callback

    def register_update_callback(self, callback: Callable[[str, list[str]], None]):
        self.update_callback = callback

    def set_categories(self, cat_data: list[str]):
        self.cat_data = cat_data

    def set_data(self, user_data: list[list[str]], headers: list[str]):
        """
        Set user data to be displayed.
        The first element in each row is considered as a primary 
        and is not displayed. 
        Primary key is used in callbacks. 
        """
        self.user_data = user_data
        self.table.setRowCount(len(self.user_data))
        self.table.setColumnCount(len(self.user_data[0]) - 1)
        self.table.setHorizontalHeaderLabels(headers)

        self._update_visual_content()

    def _update_visual_content(self):
        n_rows = self.table.rowCount()
        n_cols = self.table.columnCount()

        for i, j in itertools.product(range(n_rows), range(n_cols)):
            self.table.setItem(i, j, QtWidgets.QTableWidgetItem(self.user_data[i][j+1]))

