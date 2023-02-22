"""
Module with sqlite3 database structure
"""

import pony.orm as pny
from datetime import datetime

db = pny.Database()

class DatabaseHelper():
    @staticmethod
    def get_table_by_name(name: str) -> type:
        if name == 'Expense':
            return Expense
        elif name == 'Category':
            return Category

class Expense(db.Entity):
    pk = pny.PrimaryKey(int, auto=True)
    amount = pny.Required(float)
    category = pny.Required(int)
    comment = pny.Optional(str, 50)
    added_date = pny.Required(str, 30)
    expense_date = pny.Optional(str, 30)

    def get_data(self):
        return {
            'pk': self.pk,
            'amount': self.amount,
            'category': self.category,
            'comment': self.comment,
            'added_date': datetime.strptime(self.added_date, "%Y-%m-%d %H:%M:%S.%f"),
            'expense_date': datetime.strptime(self.expense_date, "%Y-%m-%d %H:%M:%S.%f")
        }
class Category(db.Entity):
    pk = pny.PrimaryKey(int, auto=True)
    parent = pny.Required(int)
    name = pny.Required(str, 20)