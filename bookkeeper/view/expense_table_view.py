import sys
import datetime
import itertools
from functools import partial

from PySide6 import QtWidgets, QtGui, QtCore
from typing import Any, Callable


class InputExpenseWindow(QtWidgets.QDialog):
    """ Window for entering information about new expense """

    def __init__(
        self,
        parent: QtWidgets.QWidget | None,
        on_clicked_save_callback: Callable[[dict[str, str]], None],
        ctg_options: list[str],
        msg_dict: dict[str, str],
        default_values: dict[str, str] | None = None
    ):
        super().__init__(parent)

        self.msg_dict = msg_dict
        self.setWindowTitle(msg_dict['window_title'])

        self.on_clicked_save_callback = on_clicked_save_callback
        self.ctg_options = ctg_options

        self.my_layout = QtWidgets.QVBoxLayout()
        self.expense_date: QtWidgets.QDateEdit
        self.amount: QtWidgets.QLineEdit
        self.category: QtWidgets.QComboBox
        self.comment: QtWidgets.QLineEdit

        self.create_widgets()

        if not default_values is None:
            self.fill_in_default_data(default_values)

        save_btn = QtWidgets.QPushButton(msg_dict['save_button_text'])
        save_btn.clicked.connect(self.on_clicked_save_btn)  # type: ignore[attr-defined]
        self.my_layout.addWidget(save_btn)

        self.setLayout(self.my_layout)

    def fill_in_default_data(self, data: dict[str, str]) -> None:
        self.expense_date.setDate(
            QtCore.QDate.fromString(f"{data['expense_date']}", 'dd-MM-yyyy')
        )
        self.expense_date.show()
        self.amount.setText(f"{float(data['amount']):.2f}")
        self.category.setCurrentText(f"{data['category']}")
        self.comment.setText(f"{data['comment']}")

    def create_widgets(self) -> None:
        """ Create widgets and add them to layout"""
        label = QtWidgets.QLabel('Дата покупки')
        self.my_layout.addWidget(label)

        self.expense_date = QtWidgets.QDateEdit()
        self.expense_date.setDisplayFormat('dd-MM-yyyy')
        self.expense_date.setMinimumDate(
            QtCore.QDate.fromString('01-01-2022', 'dd-MM-yyyy'))
        self.expense_date.setMaximumDate(
            QtCore.QDate.fromString('01-01-2100', 'dd-MM-yyyy'))
        self.my_layout.addWidget(self.expense_date)

        label = QtWidgets.QLabel('Сумма покупки')
        self.my_layout.addWidget(label)
        self.amount = QtWidgets.QLineEdit()
        self.amount.setPlaceholderText('500')
        self.amount.setValidator(QtGui.QDoubleValidator(0, 1000000, 2))
        self.my_layout.addWidget(self.amount)

        label = QtWidgets.QLabel('Категория покупки')
        self.my_layout.addWidget(label)
        self.category = QtWidgets.QComboBox()
        self.category.setPlaceholderText('Выбрать')
        self.category.addItems(self.ctg_options)
        self.my_layout.addWidget(self.category)

        label = QtWidgets.QLabel('Комментарий')
        self.my_layout.addWidget(label)
        self.comment = QtWidgets.QLineEdit()
        self.comment.setPlaceholderText('Кафе после работы')
        # todo validator
        self.my_layout.addWidget(self.comment)

    def is_mandatory_filled(self) -> bool:
        """ Check if mandatory fields are filled"""
        return bool(self.amount.text() and self.category.currentText())

    def get_data(self) -> dict[str, str]:
        """ Get formatted data"""
        return {
            'expense_date': self.expense_date.date().toString('dd-MM-yyyy'),
            'amount': self.amount.text(),
            'category': self.category.currentText(),
            'comment': self.comment.text()
        }

    def on_clicked_save_btn(self) -> None:
        """ Reaction on clicked save button """
        if self.is_mandatory_filled():
            self.on_clicked_save_callback(self.get_data())
            self.close()
        else:
            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Information,
                text="Заполните поля 'сумма' и 'категория'"
            )
            dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            dlg.exec()


class MainTableWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)

        self.user_data = list[list[str]]
        self.update_callback: Callable[[str, list[str]], None]
        self.remove_callback: Callable[[list[str]], None]
        self.add_callback: Callable[[dict[str, str]], None]

        self.table = QtWidgets.QTableWidget()

        add_btn = QtWidgets.QPushButton("Добавить")
        add_btn.clicked.connect(self.on_clicked_add_button)  # type: ignore[attr-defined]
        del_btn = QtWidgets.QPushButton("Удалить")
        del_btn.clicked.connect(self.on_clicked_del_button)  # type: ignore[attr-defined]
        upd_btn = QtWidgets.QPushButton("Редактировать")
        upd_btn.clicked.connect(self.on_clicked_upd_button)  # type: ignore[attr-defined]

        # horizontal layout with buttons
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(add_btn)
        h_layout.addWidget(del_btn)
        h_layout.addWidget(upd_btn)

        # buttons under the table
        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addWidget(QtWidgets.QLabel("Последние расходы"))
        v_layout.addWidget(self.table)
        v_layout.addLayout(h_layout)

        # self.table.cellChanged.connect(self.on_cell_changed)

        # self.last_clicked_cell: tuple(int, int) = (-1, -1)
        # self.table.cellClicked.connect(self.on_cell_clicked)

        self.setLayout(v_layout)

    def on_clicked_upd_button(self) -> None:
        idx = self.table.selectedItems()
        rows = list(set([i.row() for i in idx]))

        msg_dict = {
            'window_title': 'Редактировать запись',
            'save_button_text': 'Сохранить изменения'
        }

        if len(rows) == 0:
            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Information,
                text="Выберете запись для редактирования."
            )
            dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            dlg.exec()

        elif len(rows) == 1:
            row = rows[0]
            pk = self.user_data[row][0]
            row_data = {
                'expense_date': self.user_data[row][1], 'amount': self.user_data[row][2],
                'category': self.user_data[row][3], 'comment': self.user_data[row][4]
            }
            InputExpenseWindow(
                self,
                on_clicked_save_callback=partial(self.update_callback, pk),
                ctg_options=self.cat_data,
                msg_dict=msg_dict,
                default_values=row_data
            ).show()
        else:
            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Information,
                text="За раз можно отредактировать только одну запись."
            )
            dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            dlg.exec()

    def on_clicked_add_button(self) -> None:

        msg_dict = {
            'window_title': 'Добавление новой записи',
            'save_button_text': 'Добавить'
        }
        InputExpenseWindow(
            self,
            on_clicked_save_callback=self.add_callback,
            ctg_options=self.cat_data,
            msg_dict=msg_dict
        ).show()

    def on_clicked_del_button(self) -> None:
        idx = self.table.selectedItems()
        if len(idx) == 0:
            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Information,
                text="Выберите записи в таблице расходов"
            )
            dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            dlg.exec()
        else:
            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Question,
                text="Удалить выбранные записи?"
            )
            dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            answer = dlg.exec()

            if answer == QtWidgets.QMessageBox.Yes:
                rows = set([i.row() for i in idx])
                pks = [self.user_data[row][0] for row in rows]
                self.remove_callback(pks)

    def register_add_callback(self, callback: Callable[[dict[str, str]], None]) -> None:
        self.add_callback = callback

    def register_remove_callback(self, callback: Callable[[list[str]], None]) -> None:
        self.remove_callback = callback

    def register_update_callback(self, callback: Callable[[str, list[str]], None]) -> None:
        self.update_callback = callback

    def set_categories(self, cat_data: list[str]) -> None:
        self.cat_data = cat_data

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
        n_rows = self.table.rowCount()
        n_cols = self.table.columnCount()

        for i, j in itertools.product(range(n_rows), range(n_cols)):
            item = QtWidgets.QTableWidgetItem(self.user_data[i][j+1])
            item.setFlags(
                QtCore.Qt.ItemFlag.ItemIsSelectable |
                QtCore.Qt.ItemFlag.ItemIsEnabled)

            self.table.setItem(i, j, item)
