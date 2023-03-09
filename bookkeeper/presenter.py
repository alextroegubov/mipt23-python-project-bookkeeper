import sys
import datetime
import itertools
from typing import Callable


from bookkeeper.pyqt6_view import PyQtView
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

from PySide6.QtWidgets import QApplication

class Bookkeeper():
    def __init__(self, view: PyQtView, repo_cls: AbstractRepository):
        self.view = PyQtView()

        SQLiteRepository.bind_database('database.db')
        self.cat_repo = repo_cls(Category, Category.__name__)

        self.view.register_category_add_callback(self.category_add_callback)
        self.view.register_category_del_callback(self.category_del_callback)
        self.add_default_categories()
        self.set_category_data()

        self.exp_repo = repo_cls(Expense, Expense.__name__)
        self.view.register_expense_add_callback(self.expense_add_callback)
        self.view.register_expense_del_callback(self.expense_del_callback)
        self.view.register_expense_update_callback(self.expense_update_callback)
        self.set_expense_data()

        self.budget_repo = repo_cls(Budget, Budget.__name__)
        self.budget = [
            ['1', 'Day', '1500', '2000'],
            ['2', 'Week', '1500', '2000'],
            ['3', 'Month', '1500', '10000']
        ]

        self.view.register_budget_update_callback(self.budget_update_callback)
        self.view.set_budget_data(self.budget, 'Период Потрачено Лимит'.split(' '))
        self.view.window.show()



    def budget_update_callback(self, pk_str, new_limit_str):
        self.budget[int(pk_str) - 1][3] = new_limit_str
        self.view.set_budget_data(self.budget, 'Период Потрачено Лимит'.split(' '))

    def add_default_categories(self):
        lst = [
            'Готовая еда',
            'Овощи, фрукты, ягоды',
            'Молочные продукты',
            'Сладости и десерты',
            'Мясо, птица',
            'Хлеб и выпечка',
            'Рыба, морепродукты',
            'Сыры',
            'Замороженные продукты',
            'Напитки',
            'Кафе и рестораны',
            'Бытовая химия',
            'Аптека, врачи',
            'Путешествия'
        ]

        if len(self.cat_repo.get_all()) == 0:
            for ctg in lst:
                self.category_add_callback(ctg)

    def set_expense_data(self):
        exp_lst: list[Expense] = self.exp_repo.get_all()
        exp_data = [
            [f'{exp.pk}', f'{exp.expense_date}', f'{exp.amount}', 
             f'{self.cat_repo.get(exp.category).name}',
             f'{exp.comment}'] 
        for exp in exp_lst]

        headers = 'Дата Сумма Категория Комментарий'.split(' ')
        self.view.set_expense_data(exp_data, headers)

    def expense_add_callback(self, data: dict[str, str]):
        data['category'] = self.cat_repo.get_all(where={'name': data['category']})[0].pk
        new_exp = Expense(**data)
        self.exp_repo.add(new_exp)
        self.set_expense_data()

    def expense_update_callback(self, pk: str, data: list[str]):
        pass
    
    def expense_del_callback(self, del_pk: list[str]):
        for pk in del_pk:
            self.exp_repo.delete(int(pk))
        self.set_expense_data()

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