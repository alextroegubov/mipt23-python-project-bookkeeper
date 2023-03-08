import sys
import datetime
import itertools

from PySide6 import QtWidgets, QtGui, QtCore

from typing import Any, Callable


from bookkeeper.view.expense_table_view import MainTableWidget
from bookkeeper.view.categories_view import MainCategoryWidget
from bookkeeper.view.main_window import MainWindow

class PyQtView():
    def __init__(self):
        self.window = MainWindow()

        self.expense_view = MainTableWidget()
        self.category_view = MainCategoryWidget()
        self.budget_view = None

        self.window.set_expense_widget(self.expense_view)
        self.window.set_category_widget(self.category_view)
        

    def set_expense_data(self, user_data: list[list[str]], headers: list[str]):
        self.expense_view.set_data(user_data, headers)

    def set_category_data(self, data: list[list[str]]):
        self.category_view.set_data(data)

    def register_category_add_callback(self, callback: Callable[[str], None]):
        self.category_view.register_add_callback(callback)

    def register_category_del_callback(self, callback: Callable[[str], None]):
        self.category_view.register_del_callback(callback)

    def register_expense_add_callback(self, callback):
        self.expense_view.register_add_callback(callback)

    def register_expense_del_callback(self, callback):
        self.expense_view.register_remove_callback(callback)

    def register_expense_update_callback(self, callback):
        self.expense_view.register_update_callback(callback)

    def show_main_window(self):
        self.window.show()
