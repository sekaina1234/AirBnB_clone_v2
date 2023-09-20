#!/usr/bin/python3
""" This module initializes the storage engine """
from os import environ

storage_t = environ.get('HBNB_TYPE_STORAGE')

if storage_t == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
