
import sys
import datetime

from PySide6 import QtWidgets, QtGui

from PySide6.QtCore import QSize, Qt, QAbstractTableModel, QModelIndex
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTableView

from typing import Any, Callable

class ExpenseTableModel(QAbstractTableModel):
    def __init__(self, data: list[list], headers: list[str]):
        super(ExpenseTableModel, self).__init__()

        self.m_data = data
        self.m_headers = headers

        assert len(headers) == len(data[0])

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            value = self.m_data[index.row()][index.column()]

            return self._data_type_converter(value)

    def rowCount(self, index):
        """The length of the outer list"""
        return len(self.m_data)

    def columnCount(self, index):
        """ The following takes the first sub-list, and returns the length 
        (only works if all rows are an equal length) 
        """
        return len(self.m_data[0])

    def headerData(self, section: int, orientation: Qt.Orientation, role = Qt.ItemDataRole.DisplayRole) -> Any:

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.m_headers[section]

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled| Qt.ItemFlag.ItemIsEditable

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.m_data[index.row()][index.column()] = value
            return True

    def _data_type_converter(self, value):

        if isinstance(value, datetime.datetime):
            return value.strftime("%Y-%m-%d")

        if isinstance(value, float):
            return f"{value:.2f}"

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            return value


    def removeRows(self, first_row, count, parent: QModelIndex) -> bool:
        self.beginRemoveRows(parent, first_row, first_row + count - 1)
        for row_number in range(count):
            #TODO delete from db
            del(self.m_data[first_row])
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True

    def insertRow(self, row_value: list) -> bool:
        row = len(self.m_data)

        self.beginInsertRows(QModelIndex(), row, row)
        self.m_data.append(row_value)
        self.endInsertRows()
        self.layoutChanged.emit()
        return True


class AddExpenseWindow(QtWidgets.QDialog):
    """ Pop-up window for entering information about new expense """
    def __init__(self, parent, on_clicked_save_callback: Callable):
        super().__init__(parent)

        self.setWindowTitle("Добавление записи о раходах")

        self.layout = QtWidgets.QVBoxLayout()
        self.create_widgets()

        self.save_btn = QtWidgets.QPushButton('Добавить новую запись')
        self.save_btn.clicked.connect(self.on_clicked_save_btn)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

        self.on_clicked_save_callback = on_clicked_save_callback

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

        self.category = QtWidgets.QLineEdit()
        self.category.setPlaceholderText('Категория')
        # todo validator
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
        return [self.expense_date.text(), self.amount.text(), self.category.text(), self.comment.text()]

    def on_clicked_save_btn(self):
        """ Reaction on clicked save button """
        if self.is_mandatory_filled():
            self.on_clicked_save_callback(self.get_data())
            self.close()
        else:
            # TODO show msg
            pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("The best Application")
        self.adjust_window_to_screen()

        data = [
          ['abc', 9, 2],
          [1, 0, 0],
          [3, 2.78, 0],
          [3, 3, 2],
          [7, 8, 9],
          [1, 0, 0],
          [3, 2.78, 0],
          [3, 3, 2],
          [7, 8, 9],        
        ]

        self.model = ExpenseTableModel(data, ['col1', 'col2', 'col3'])

        h_layout = QtWidgets.QHBoxLayout()
        v_layout = QtWidgets.QVBoxLayout()

        del_btn = QtWidgets.QPushButton('Delete')
        del_btn.clicked.connect(self.on_clicked_delete_btn)
        add_btn = QtWidgets.QPushButton('Add')
        add_btn.clicked.connect(self.on_clicked_add_btn)

        v_layout.addWidget(add_btn)
        v_layout.addWidget(del_btn)


        self.table = QTableView()
        self.table.setModel(self.model)
        
        h_layout.addWidget(self.table)
        h_layout.addLayout(v_layout)

        widget = QtWidgets.QWidget()
        widget.setLayout(h_layout)

        self.setCentralWidget(widget)


    def on_clicked_delete_btn(self):
        idx = self.table.selectedIndexes()

        if len(idx) == 0:
            return

        rows = set([i.row() for i in idx])

        self.model.removeRows(
            first_row=idx[0].row(),
            count=len(rows),
            parent=idx[0]
        )
        print('Delete button clicked!')

    def expense_window_callback(self, data):
        self.model.insertRow(data[1:])
        print('Add button clicked!')


    def on_clicked_add_btn(self):
        exp_win = AddExpenseWindow(self, self.expense_window_callback)
        exp_win.show()

    def adjust_window_to_screen(self):
        w = self.screen().geometry().width()
        h = self.screen().geometry().height()

        self.resize(QSize(0.7*w, 0.7*h))
        self.setGeometry(0.15*w, 0.15*h, 0.7*w, 0.7*h)
        self.setMinimumSize(QSize(0.2*w, 0.2*h))
        self.setMaximumSize(QSize(0.9*w, 0.9*h))

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()