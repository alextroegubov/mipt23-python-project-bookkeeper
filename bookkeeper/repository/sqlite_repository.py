"""
Module for repository working with sqlite3 database
"""

from itertools import count
from typing import Any
from inspect import get_annotations

from pony import orm

from bookkeeper.repository.abstract_repository import AbstractRepository, T
import bookkeeper.repository.databases as my_dbs


class SQLiteRepository(AbstractRepository[T]):
    """
    SQLite3 repository
    """
    def __init__(self, db_filename: str, data_cls: type) -> None:

        if db_filename == 'abc':
            my_dbs.expenses_db.bind(provider='sqlite', 
                                    filename=db_filename,
                                    create_db=False)

            my_dbs.expenses_db.generate_mapping(create_tables=False)
            self.table_cls = my_dbs.Expense
        elif db_filename == 'def':
            my_dbs.category_db.bind(provider='sqlite', 
                                    filename=db_filename,
                                    create_db=False)

            my_dbs.category_db.generate_mapping(create_tables=False)
            self.table_cls = my_dbs.Category

        self.data_cls = data_cls
        self.data_cls_fields = get_annotations(self.data_cls, eval_str=True)
        self.data_cls_fiels.pop('pk')

    @orm.db_session
    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')

        kwargs = {f: getattr(obj, f) for f in self.data_cls_fields.keys()}
        db_obj = self.table_cls(**kwargs)

        return db_obj.pk

    @orm.db_session
    def get(self, pk: int) -> T | None:
        db_obj = orm.select(p for p in self.table_cls if p.pk == pk)

        if len(db_obj) == 0:
            return None

        db_obj_field = get_annotations(self.table_cls, eval_str=True)
        kwargs = {f: getattr(db_obj, f) for f in db_obj_field.keys()}

        return self.data_cls(**kwargs)

    @orm.db_session
    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')

        db_obj = self.table_cls[obj.pk]

        for f in self.data_cls_fields.keys():
            setattr(db_obj, f, getattr(obj, f))

    # def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
    #     if where is None:
    #         return list(self._container.values())
    #     return [obj for obj in self._container.values()
    #             if all(getattr(obj, attr) == value for attr, value in where.items())]