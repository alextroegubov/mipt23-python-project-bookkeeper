import sys
import datetime
import itertools

from bookkeeper.pyqt6_view import PyQtView
from bookkeeper.repository.abstract_repository import AbstractRepository
from typing import Callable

from PySide6.QtWidgets import QApplication

class Bookkeeper():
    def __init__(self, view: PyQtView, repository: AbstractRepository):
        self.view = PyQtView()
        self.repository = AbstractRepository

        self.ctgs = [
            ['1', 'cat1'],
            ['2', 'cat2'],
            ['3', 'cat3'],
            ['4', 'cat4']
        ]

        self.expenses = [
            ['1', '1500', 'abc'],
            ['2', '1900', 'mnk'],
            ['3', '150', 'cde'],
            ['4', '1200', 'gh']
        ]

        self.headers = ['sum', 'comment']

        self.ctg_counter = 4
        self.view.register_category_add_callback(self.category_add_callback)
        self.view.register_category_del_callback(self.category_del_callback)
        self.view.set_category_data(self.ctgs)


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

    def category_add_callback(self, cat):
        self.ctg_counter += 1
        self.ctgs.append([f'{self.ctg_counter}', f'{cat}'])
        self.view.category_view.set_data(self.ctgs)

    def category_del_callback(self, pk):
        pks = [row[0] for row in self.ctgs]
        self.ctgs.remove(self.ctgs[pks.index(pk)])
        self.view.category_view.set_data(self.ctgs)

app = QApplication(sys.argv)

bookkeeper = Bookkeeper(None, None)

app.exec()