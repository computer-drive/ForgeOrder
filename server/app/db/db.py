from flask import g

import extensions

from .main_db import MainDatabase
from .meta_db import MetaDatabase


def get_main_database():
    if "main_database" not in g:
        g.main_database = MainDatabase(extensions.config.get("main_db"))
        
    return g.main_database

def get_meta_database():
    if "meta_database" not in g:
        g.meta_database = MetaDatabase(extensions.config.get("meta_db"))
        
    return g.meta_database

def close_databases():
    if "main_database" in g:
        g.main_database.close()
    if "meta_database" in g:
        g.meta_database.close()