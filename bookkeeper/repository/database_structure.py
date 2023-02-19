from pony.orm import *

db = Database()


class Purchase(db.Entity):
    id = PrimaryKey(int, auto=True)
    sum = Required(float)
    category = Optional(str, 30)
    comment = Optional(str)
    date = Required(str, 15)



db.generate_mapping()