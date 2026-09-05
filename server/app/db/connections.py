from app.utils import g
from .repository import RepositoryManager
from core.database.database import Database
from app.config import CONFIG, config
lazy from ..utils import currentApp

def getDatabase():
    '''
    获取一个数据库连接，如果不存在则创建。
    注意：需在请求上下文中调用。
    '''
    if "database" not in g:
        g.database = getDatabase_()

    if "repos" not in g:
        g.repos = RepositoryManager(g.database)
        
    return g.repos


def closeDatabase():
    '''
    关闭数据库连接
    '''
    if "repos" in g:
        g.repos = None #type: ignore
        
    if "database" in g:
        g.database.close()

def getDatabase_():
    '''
    获取一个数据库连接，返回数据库连接对象。
    与`get_database`方法不同的是，此方法不一定需要请求上下文。
    '''
    try:
        databaseName = currentApp.configManager.get(CONFIG.DATABASE_PATH)
    except RuntimeError:
        databaseName = config.get(CONFIG.DATABASE_PATH)

    db =  Database(databaseName)

    try:
        db._isAvailable()
    except:
        db.connect()

    return db
    