from flask import g

import extensions

from .main_db import MainDatabase


def get_database():
    if "database" not in g:
        g.database = MainDatabase(extensions.config.get("database.path"))
        
    return g.database



def close_database():
    if "database" in g:
        g.database.close()
    