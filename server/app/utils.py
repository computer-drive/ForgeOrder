from typing import TypedDict, cast

from flask import g as g_
from flask import current_app

from .processing.log.record import RequestLogContext
from .routes.responseGenerator import ResponseGenerator
from core.database.database import Database
from app.db.repository import RepositoryManager
from .processing.log.record import WorkerLogger
lazy from .setup import MyFlaskApp

class UserInfo(TypedDict):
    id: int
    isAdmin: bool
    username: str

class GProxy:
    '''拥有类型提示的g对象'''

    requestId: str

    logger: RequestLogContext
    workerLogger: WorkerLogger

    startTime: float
    endTime: float | None

    res: ResponseGenerator

    args: dict

    userInfo: UserInfo

    database: Database

    repos: RepositoryManager



    def __contains__(self, name: str):
        return hasattr(self, name)

g = cast(GProxy, g_)

currentApp = cast(MyFlaskApp, current_app)
