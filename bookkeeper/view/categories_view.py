"""GUI for categories"""
from typing import Callable
from PySide6 import QtWidgets


class EditCategoriesWindow(QtWidgets.QDialog):
    """ Window for editing categories"""

    def __init__(self,
                 parent: QtWidgets.QWidget | None,
                 data: list[list[str]],
                 add_callback: Callable[[str], None],
                 del_callback: Callable[[str], None]):
        super().__init__(parent=parent)
        self.setWindowTitle("Редактирование списка категорий")
        self.add_callback = add_callback
        self.del_callback = del_callback

        self.user_data: list[list[str]]
        self.ctgs_lst: list[str]

        main_layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Категории")
        main_layout.addWidget(message)

        self.ctg_lst_widget = QtWidgets.QListWidget()
        main_layout.addWidget(self.ctg_lst_widget)

        grid_layout = QtWidgets.QGridLayout()

        add_btn = QtWidgets.QPushButton('Добавить категорию')
        add_btn.clicked.connect(self.on_clicked_add_button)  # type: ignore[attr-defined]
        grid_layout.addWidget(add_btn, 0, 1)

        self.add_input = QtWidgets.QLineEdit()
        self.add_input.setPlaceholderText('Новая категория')
        grid_layout.addWidget(self.add_input, 0, 0)

        del_btn = QtWidgets.QPushButton('Удалить категорию')
        del_btn.clicked.connect(self.on_clicked_del_button)  # type: ignore[attr-defined]
        grid_layout.addWidget(del_btn, 1, 1)

        self.del_input = QtWidgets.QComboBox()
        self.del_input.setPlaceholderText('Выберите категорию')
        grid_layout.addWidget(self.del_input, 1, 0)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

        self.set_data(data)

    def set_data(self, data: list[list[str]]) -> None:
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

    def on_clicked_add_button(self) -> None:
        """ Triggers when add button is pressed"""
        # TODO check duplicates: through callback return value ?!
        if self.add_input.text():

            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Question,
                text=f"Добавить категорию {self.add_input.text()}?"
            )
            dlg.setStandardButtons(QtWidgets.QMessageBox.Yes |
                                   QtWidgets.QMessageBox.Cancel)
            answer = dlg.exec()

            if answer == QtWidgets.QMessageBox.Yes:
                self.add_callback(self.add_input.text())
                self.add_input.clear()

    def on_clicked_del_button(self) -> None:
        """ Triggers when delete button is pressed"""
        combo_box_input = self.del_input.currentText()

        if combo_box_input:

            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Question,
                text=f"Удалить категорию {combo_box_input}?"
            )
            dlg.setStandardButtons(QtWidgets.QMessageBox.Yes |
                                   QtWidgets.QMessageBox.Cancel)
            answer = dlg.exec()

            if answer == QtWidgets.QMessageBox.Yes:
                pk = self.user_data[self.ctgs_lst.index(combo_box_input)][0]
                self.del_callback(pk)


class MainCategoryWidget(QtWidgets.QWidget):
    """ Main widget for displaying  categories"""

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)

        layout = QtWidgets.QVBoxLayout()

        btn = QtWidgets.QPushButton('Редактировать список категорий')
        btn.clicked.connect(self.on_clicked_edit_button)  # type: ignore[attr-defined]
        layout.addWidget(btn)
        self.setLayout(layout)

        self.edit_window: EditCategoriesWindow | None = None
        self.add_callback: Callable[[str], None]
        self.del_callback: Callable[[str], None]
        self.user_data: list[list[str]]

    def set_data(self, data: list[list[str]]) -> None:
        """ Data format: [['pk1', 'cat1'], ['pk2', 'cat2']].
            The first element is considered as a primary key and 
            used in callbacks
        """
        self.user_data = data
        if not self.edit_window is None:
            self.edit_window.set_data(data)

    def register_add_callback(self, callback: Callable[[str], None]) -> None:
        """ Register callback on adding a new category"""
        self.add_callback = callback

    def register_del_callback(self, callback: Callable[[str], None]) -> None:
        """ Register callback on deleting a category"""
        self.del_callback = callback

    def on_clicked_edit_button(self) -> None:
        """ Open edit window on clicked edit button"""
        self.edit_window = EditCategoriesWindow(self,
                                                data=self.user_data,
                                                add_callback=self.add_callback,
                                                del_callback=self.del_callback)
        self.edit_window.show()
