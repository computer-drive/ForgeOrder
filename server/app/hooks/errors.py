import json
import traceback

from flask import current_app
from werkzeug.exceptions import UnsupportedMediaType

from core.log import getConsoleLogger, getLogger
from ..db.connections import closeDatabase
from core.database.database.exceptions import DatabaseLockedError
from app.routes.schema import GLOBAL
from app.utils import g

# 415
def unsupportedMediaType(e: UnsupportedMediaType):

	return GLOBAL.PAYLOAD_ERROR(e.description), 415
# 405
def methodNotAllowed(e):
	return GLOBAL.METHOD_ERROR(), 405
    
# 404
def notFound(e):
	return GLOBAL.NOT_FOUND(), 404

# 500
def internalServerError(e):
	return GLOBAL.SERVER_ERROR(), 500
    

# 数据库错误处理
def handleDatabaseLockedError(e: DatabaseLockedError):
	g.logger.warning({
			"traceback": traceback.format_exception(type(e), e, e.__traceback__)
	}, "DatabaseBusy")
	return GLOBAL.DATABASE_BUSY(), 503

def databaseError(e):
	return GLOBAL.DATABASE_ERROR(), 500

def teardownAppContext(error): 
	if error is not None:
		# 有错误，回滚事务
		if g.database is not None:
			g.database.rollback()
		logs = {
					"error": {
						"msg": str(error),
						"type": type(error).__name__,
					},
					"traceback": None
					
				}
                
		if isinstance(error, Exception):
			logs["traceback"] = traceback.format_exception(type(error), error, error.__traceback__) # type: ignore
	
		consoleLogger = getConsoleLogger("flask")
	
		consoleLogger.warning('\n'.join(traceback.format_exception(type(error), error, error.__traceback__))) # type: ignore

		current_app.workerLogger.error(
			logs
		, "FLASK_APP", "RequestError")
        
	else:
		
		# 无错误，提交事务，防止未提交事务
		if g.database is not None:
			g.database.commit()

	# 关闭数据库连接
	closeDatabase()
                        

	

	return current_app



def setupErrorHandlers(app):
    app.errorhandler(405)(methodNotAllowed)

    app.errorhandler(404)(notFound)
    app.errorhandler(500)(internalServerError)
    app.errorhandler(415)(unsupportedMediaType)

    app.errorhandler(DatabaseLockedError)(handleDatabaseLockedError)

    app.teardown_appcontext(teardownAppContext)