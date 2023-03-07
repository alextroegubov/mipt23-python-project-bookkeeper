from PySide6 import QtWidgets, QtGui, QtCore
from typing import Any, Callable

class EditCategoriesWindow(QtWidgets.QDialog):
    """ Window for editting categories"""
    def __init__(self, parent, data: list[list[str]],
                 add_callback: Callable[[str], None],
                 del_callback: Callable[[str], None]):
        super().__init__(parent)
        self.setWindowTitle("Редактирование списка категорий")
        self.add_callback = add_callback
        self.del_callback = del_callback

        self.user_data: list[list[str]]
        self.ctg_lst: list[str]

        main_layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Категории")
        main_layout.addWidget(message)

        self.ctg_lst_widget = QtWidgets.QListWidget()
        main_layout.addWidget(self.ctg_lst_widget)

        grid_layout = QtWidgets.QGridLayout()

        self.add_btn = QtWidgets.QPushButton('Добавить категорию')
        self.add_btn.clicked.connect(self.on_clicked_add_button)
        grid_layout.addWidget(self.add_btn, 0, 1)

        self.add_input = QtWidgets.QLineEdit()
        self.add_input.setPlaceholderText('Новая категория')
        grid_layout.addWidget(self.add_input, 0, 0)

        self.del_btn = QtWidgets.QPushButton('Удалить категорию')
        self.del_btn.clicked.connect(self.on_clicked_del_button)
        grid_layout.addWidget(self.del_btn, 1, 1)

        self.del_input = QtWidgets.QComboBox()
        grid_layout.addWidget(self.del_input, 1, 0)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

        self.set_data(data)

    def set_data(self, data: list[list[str]]):
        """ Data format: [['pk1', 'cat1'], ['pk2', 'cat2']].
            The first element is considered as a primary key and 
            used in callbacks
        """
        self.user_data = data
        self.ctgs_lst = [row[1] for row in data]

        self.ctg_lst_widget.clear()
        self.ctg_lst_widget.addItems(self.ctgs_lst)

        self.del_input.clear()
        self.del_input.addItems(self.ctgs_lst)

    def on_clicked_add_button(self):
        """ Triggers when add button is pressed"""
        if self.add_input.text():
            self.add_callback(self.add_input.text())

    def on_clicked_del_button(self):
        """ Triggers when delete button is pressed"""
        combo_box_input = self.del_input.currentText()
        pk = self.user_data[self.ctgs_lst.index(combo_box_input)][0]
        self.del_callback(pk)


class MainCategoryWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()

        btn = QtWidgets.QPushButton('Редактировать список категорий')
        btn.clicked.connect(self.on_clicked_edit_button)
        layout.addWidget(btn)
        self.setLayout(layout)

        self.w: EditCategoriesWindow = None

    def set_data(self, data: list[list[str]]):
        """ Data format: [['pk1', 'cat1'], ['pk2', 'cat2']].
            The first element is considered as a primary key and 
            used in callbacks
        """
        self.user_data = data
        if not (self.w is None):

            self.w.set_data(data)

    def register_add_callback(self, callback: Callable[[str], None]):
        """ Register callback on adding a new category"""
        self.add_callback = callback

    def register_del_callback(self, callback: Callable[[str], None]):
        """ Register callback on deleting a category"""
        self.del_callback = callback

    def on_clicked_edit_button(self):
        self.w = EditCategoriesWindow(self,
            data=self.user_data,
            add_callback=self.add_callback,
            del_callback=self.del_callback)
        self.w.show()

