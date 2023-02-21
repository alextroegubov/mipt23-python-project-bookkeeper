"""
Module for repository working with sqlite3 database
"""

from itertools import count
from typing import Any
from inspect import get_annotations
import datetime

from pony import orm

from bookkeeper.repository.abstract_repository import AbstractRepository, T
import bookkeeper.repository.databases as my_dbs
from bookkeeper.utils import py2sqlite_type_converter


class SQLiteRepository(AbstractRepository[T]):
    """
    SQLite3 repository
    """
    def __init__(self, data_cls: type,
                 table_name: str, 
                 db_filename: str = 'database.db') -> None:

        my_dbs.db.bind(provider='sqlite', 
                        filename=db_filename,
                        create_db=True)

        my_dbs.db.generate_mapping(create_tables=True)

        self.table_cls = my_dbs.DatabaseHelper.get_table_by_name(table_name)
        self.data_cls = data_cls
        self.data_cls_fields = get_annotations(self.data_cls, eval_str=True)
        self.data_cls_fields.pop('pk')

    @orm.db_session
    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')

        kwargs = {
            f: py2sqlite_type_converter(getattr(obj, f)) 
            for f in self.data_cls_fields.keys()
        }
        db_obj = my_dbs.Expense(**kwargs)
        orm.commit()
        return db_obj.pk

    @orm.db_session
    def get(self, pk: int) -> T | None:
        db_obj = orm.select(p for p in self.table_cls if p.pk == pk)[:]

        if len(db_obj) == 0:  # no such a primary key
            return None

        return self.data_cls(**db_obj[0].get_data())

    @orm.db_session
    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')

        db_obj = self.table_cls[obj.pk]

        for f in self.data_cls_fields.keys():
            setattr(db_obj, f, getattr(obj, f))

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        pass

    def delete(self, pk: int) -> None:
        pass

    # @orm.db_session
    # def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
    #     if where is None:
    #         res_lst = orm.select(p for p in )

    #         return list(self._container.values())
    #     return [obj for obj in self._container.values()
    #             if all(getattr(obj, attr) == value for attr, value in where.items())]