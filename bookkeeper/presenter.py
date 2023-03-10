""" Presenter module. Interacts with models, repositories and views."""
import sys
from datetime import date, datetime, timedelta
import calendar
from typing import Any

from PySide6.QtWidgets import QApplication

from bookkeeper.pyqt6_view import PyQtView
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


class Bookkeeper():
    def __init__(self, view_cls: Any, repo_cls: Any):
        self.view: PyQtView = view_cls()

        SQLiteRepository.bind_database('database.db')
        self.cat_repo = repo_cls(Category, Category.__name__)
        self.exp_repo = repo_cls(Expense, Expense.__name__)
        self.budget_repo = repo_cls(Budget, Budget.__name__)

        self.view.register_category_add_callback(self.category_add_callback)
        self.view.register_category_del_callback(self.category_del_callback)
        self.add_default_categories()
        self.set_category_data()

        self.view.register_expense_add_callback(self.expense_add_callback)
        self.view.register_expense_del_callback(self.expense_del_callback)
        self.view.register_expense_update_callback(self.expense_update_callback)
        self.set_expense_data()

        self.view.register_budget_update_callback(self.budget_update_callback)
        self.add_default_budget()
        self.set_budget_data()

        self.view.window.show()

    def set_budget_data(self) -> None:
        """ Take data from repository and pass it to view"""
        self.update_budget_spent_column()
        budget_lst: list[Budget] = self.budget_repo.get_all()
        budget_data = [
            [f'{b.pk}', f'{b.period}', f'{b.spent}', f'{b.limit}']
            for b in budget_lst
        ]
        headers = 'Период Потрачено Лимит'.split(' ')
        self.view.set_budget_data(budget_data, headers=headers)

    def update_budget_spent_column(self) -> None:
        """ Updates budget spent column based on expenses"""
        all_expenses: list[Expense] = self.exp_repo.get_all()

        day = date.today().day
        month = date.today().month
        year = date.today().year
        today = datetime(year=year, month=month, day=day)

        spent_day, spent_week, spent_month = 0, 0, 0

        for expense in all_expenses:
            # day
            if expense.expense_date == today:
                spent_day += expense.amount
            # month
            if (datetime(year=year, month=month, day=1) <= expense.expense_date
                    <= datetime(year=year, month=month, day=calendar.monthrange(year, month)[1])):
                spent_month += expense.amount
            # week
            monday = today - timedelta(days=today.weekday())
            if (monday <= expense.expense_date <= monday + timedelta(days=6)):
                spent_week += expense.amount

        for spent_prd, prd in zip([spent_day, spent_week, spent_month], ['День', 'Неделя', 'Месяц']):
            period_record: Budget = self.budget_repo.get_all(where={'period': prd})[0]
            if period_record.spent != spent_prd:
                period_record.spent = spent_prd
                self.budget_repo.update(period_record)

    def budget_update_callback(self, pk_str: str, new_limit_str: str) -> None:
        """ Callback for budget update"""
        record: Budget = self.budget_repo.get(int(pk_str))
        record.limit = float(new_limit_str)
        self.budget_repo.update(record)

        self.set_budget_data()

    def add_default_budget(self) -> None:
        """ Add default records in repository if it is empty"""
        if len(self.budget_repo.get_all()) == 0:
            for period in 'День Неделя Месяц'.split(' '):
                budget = Budget(period=period, limit=0, spent=0)
                self.budget_repo.add(budget)

    def add_default_categories(self) -> None:
        """ Add default records in repository if it is empty"""
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

    def set_expense_data(self) -> None:
        """ Take data from repository and pass it to view"""
        exp_lst: list[Expense] = self.exp_repo.get_all()
        exp_data = [
            [f'{exp.pk}', exp.expense_date, f'{exp.amount}',
             f'{self.cat_repo.get(exp.category).name}',
             f'{exp.comment}']
            for exp in exp_lst]

        exp_data = sorted(exp_data, key=lambda row: row[1], reverse=True)

        for exp in exp_data:
            exp[1] = f'{exp[1].strftime("%d-%m-%Y")}'

        headers = 'Дата Сумма Категория Комментарий'.split(' ')
        self.view.set_expense_data(exp_data, headers)
        self.set_budget_data()

    def expense_add_callback(self, data: dict[str, str]) -> None:
        """ Callback for expense add procedure"""
        data['category'] = self.cat_repo.get_all(where={'name': data['category']})[0].pk
        new_exp = Expense(**data)
        self.exp_repo.add(new_exp)
        self.set_expense_data()

    def expense_update_callback(self, pk: str, data: list[str]) -> None:
        """ Callback for expense update procedure"""
        data['category'] = self.cat_repo.get_all(where={'name': data['category']})[0].pk
        upd_exp = Expense(pk=int(pk), **data)
        self.exp_repo.update(upd_exp)
        self.set_expense_data()

    def expense_del_callback(self, del_pk: list[str]) -> None:
        """ Callback for expense delete procedure"""
        for pk in del_pk:
            self.exp_repo.delete(int(pk))
        self.set_expense_data()

    def set_category_data(self) -> None:
        """ Take data from repository and pass it to view"""
        ctgs_lst: list[Category] = self.cat_repo.get_all()
        ctg_data = [[f'{ctg.pk}', f'{ctg.name}'] for ctg in ctgs_lst]
        self.view.set_category_data(ctg_data)

    def category_add_callback(self, ctg_name: str) -> None:
        """ Callback for category add procedure"""
        ctg = Category(name=ctg_name, parent=None)
        self.cat_repo.add(ctg)

        self.set_category_data()

    def category_del_callback(self, pk_str: str) -> None:
        """ Callback for category add procedure"""
        self.cat_repo.delete(int(pk_str))
        self.set_category_data()


app = QApplication(sys.argv)

bookkeeper = Bookkeeper(PyQtView, SQLiteRepository)

app.exec()
