"""
Module with sqlite3 database structure
"""

from pony import orm

expenses_db = orm.Database()

class Expense(expenses_db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    amount = orm.Required(float)
    category = orm.Optional(int)
    comment = orm.Optional(str, 50)
    added_date = orm.Required(str, 15)
    expense_data = orm.Optional(str, 10)


category_db = orm.Database()

class Category(category_db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    parent = orm.Required(int)
    name = orm.Required(str, 20)