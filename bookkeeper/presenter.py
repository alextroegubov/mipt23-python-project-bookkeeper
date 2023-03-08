import sys
import datetime
import itertools
from typing import Callable


from bookkeeper.pyqt6_view import PyQtView
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category

from PySide6.QtWidgets import QApplication

class Bookkeeper():
    def __init__(self, view: PyQtView, repo_cls: AbstractRepository):
        self.view = PyQtView()

        SQLiteRepository.bind_database('database.db')
        self.cat_repo = repo_cls[Category](Category, Category.__name__)

        self.view.register_category_add_callback(self.category_add_callback)
        self.view.register_category_del_callback(self.category_del_callback)
        self.set_category_data()

        self.expenses = [
            ['1', '1500', 'abc'],
            ['2', '1900', 'mnk'],
            ['3', '150', 'cde'],
            ['4', '1200', 'gh']
        ]
        self.headers = ['sum', 'comment']


        self.exp_counter = 4
        self.view.register_expense_add_callback(self.expense_add_callback)
        self.view.register_expense_del_callback(self.expense_remove_callback)
        self.view.register_expense_update_callback(self.expense_update_callback)
        self.view.set_expense_data(self.expenses, self.headers)

        self.view.window.show()

    def expense_add_callback(self, data: list[str]):
        new_row = []
        new_row.append(f'{self.exp_counter}')
        new_row.extend(data)

        self.expenses.append(new_row[:3])
        self.view.set_expense_data(self.expenses, self.headers)

    def expense_update_callback(self, pk: str, data: list[str]):

        for row in self.expenses:
            if row[0] == pk:
                new_row = []
                new_row.append(pk)
                new_row.extend(data)
                self.expenses.append(new_row[:3])
                self.view.set_expense_data(self.expenses, self.headers)
                break
    
    def expense_remove_callback(self, remove_pk: list[str]):
        new_data = []
        for row in self.expenses:
            if row[0] in remove_pk:
                continue
            else:
                new_data.append(row)
        self.expenses = new_data
        self.view.set_expense_data(self.expenses, self.headers)

    def set_category_data(self):
        ctgs_lst: list[Category] = self.cat_repo.get_all()
        ctg_data = [[f'{ctg.pk}', f'{ctg.name}'] for ctg in ctgs_lst]
        self.view.set_category_data(ctg_data)

    def category_add_callback(self, ctg_name: str):
        """ Triggers on adding a category """
        ctg = Category(name=ctg_name, parent = None)
        self.cat_repo.add(ctg)

        self.set_category_data()

    def category_del_callback(self, pk_str: str):
        """ Triggers on deleting a category """
        self.cat_repo.delete(int(pk_str))
        self.set_category_data()

app = QApplication(sys.argv)

bookkeeper = Bookkeeper(None, SQLiteRepository)

app.exec()