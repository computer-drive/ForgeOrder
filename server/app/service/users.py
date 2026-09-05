
import secrets
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import cast 
from werkzeug.security import check_password_hash, generate_password_hash

from ..utils import currentApp
from app.config import CONFIG

from .base import Service, Result
from ..db.repository import RepositoryManager
from core.database.repository.exceptions import RecordNotFoundError

class LoginResult(Enum):
    SUCCESS = auto()
    USERNAME_OR_PASSWORD_ERROR = auto()
    USER_DISABLED = auto()
    NEW_DEVICE = auto()
    REPEAT_LOGIN = auto()

class LogoutResult(Enum):
    SUCCESS = auto()
    TOKEN_INVALID = auto()

class AuthResult(Enum):
    SUCCESS = auto()
    TOKEN_INVALID = auto()

    TOKEN_EXPIRED = auto()
    TOKEN_LOGOUT = auto()
    TOKEN_OLD_DEVICE = auto()

class UserResult(Enum):
    SUCCESS = auto()

    MISSING_QUERY = auto() # 缺失查询条件

    USER_NOT_FOUND = auto()

    OLD_PASSWORD_ERROR = auto() # 再更改密码操作中，旧密码错误



class UserService(Service):
    LOGIN = LoginResult
    LOGOUT = LogoutResult
    AUTH = AuthResult
    USER = UserResult

    def _generateToken(self):
        '''使用secrets库生成随机token'''
        return secrets.token_urlsafe(32)

    def _insertToken(self, userId: int, token: str, expireTime: datetime, ip: str):
        '''
        将一条token插入到表中。
        '''
        self.repositoryManager.tokens.insert(
            userId=userId,
            token=token,
            status=0,
            expireTime=expireTime,
            ip=ip,
        )

    
    def __init__(self, repositoryManager: RepositoryManager):
        super().__init__(repositoryManager)


        
        self.availableTime = currentApp.configManager.get(CONFIG.AUTH_AVAILABLE_TIME)

        


    def login(self, username: str, password: str, ip: str, cover: bool):
        '''
        用户登录操作。
        '''

        repeatLogin = False

        users = self.repositoryManager.users.get(username=username)

        if users is None:
            # 用户不存在
            return Result(self.LOGIN.USERNAME_OR_PASSWORD_ERROR)

        # 判断密码是否正确

        if not check_password_hash(users["password"], password):
            # 密码错误
            return Result(self.LOGIN.USERNAME_OR_PASSWORD_ERROR)
        
        # 检查用户是否启用
        if not users["isAvailable"]:
            # 用户未启用
            return Result(self.LOGIN.USER_DISABLED)
        
        # 检查token是否存在
        tokenInfo = self.repositoryManager.tokens.get(userId=users["id"])

        if tokenInfo is None:
            # token不存在，生成新的token
            token = self._generateToken()
            expireTime = datetime.now() + timedelta(minutes=self.availableTime)

            self._insertToken(users["id"], token, expireTime, ip)
            

        else:
            # token存在
            token = tokenInfo["token"]

            # 判断是否有效
            if tokenInfo["status"] != 0 or tokenInfo["expireTime"] < datetime.now():
                # token无效
                # 删除旧token
                self.repositoryManager.tokens.update(
                    where={"id": tokenInfo["id"]},
                    data={"status": 3}
                )

                # 生成新的token
                token = self._generateToken()
                expireTime = datetime.now() + timedelta(days=self.availableTime)

                self._insertToken(users["id"], token, expireTime, ip)

                # 重新获取token确保tokenInfo为最新的信息
                tokenInfo = self.repositoryManager.tokens.get(userId=users["id"])

                repeatLogin = False
        
                
            elif tokenInfo["ip"] != ip:
                # token有效
                if not cover:
                    return Result(self.LOGIN.NEW_DEVICE, {
                        "oldDevice": tokenInfo["ip"]
                    })
                
                else:
                    # 删除旧token
                    self.repositoryManager.tokens.update(
                        where={"id": tokenInfo["id"]},
                        data={"status": 3}
                    )

                    # 生成新的token
                    token = self._generateToken()
                    expireTime = datetime.now() + timedelta(days=self.availableTime)

                    self.repositoryManager.tokens.insert(
                        userId=users["id"],
                        token=token,
                        status=0,
                        expireTime=expireTime,
                        ip=ip,
                    )

                    # 重新获取token确保tokenInfo为最新的信息
                    tokenInfo = self.repositoryManager.tokens.get(userId=users["id"])

                    repeatLogin = False

            else:
                # ip相同，同一设备的重复登录
                repeatLogin = True

            
                           
            
        # 删除敏感信息
        userInfo = dict(users.copy())
        del userInfo["password"]

        # 更新users表中的last_login_at
        self.repositoryManager.users.update(
            where={"id": users["id"]},
            data={"lastLoginAt": datetime.now()}
        )

        self.repositoryManager.users.commit()
        # 返回结果


        return Result(self.LOGIN.SUCCESS if not repeatLogin else self.LOGIN.REPEAT_LOGIN, {
            "token": token,
            "user": userInfo,
        })

    def logout(self, token: str):
        '''
        用户退出登录操作。
        '''


        # 检查token是否存在
        tokenInfo = self.repositoryManager.tokens.get(token=token)
        if tokenInfo is None:
            # token不存在
            return Result(self.LOGOUT.TOKEN_INVALID)

        # 更新token表中的status为2
        self.repositoryManager.tokens.update(
            where={"token": token},
            data={"status": 2}
        )

        # 整体提交事务
        self.repositoryManager.tokens.commit()

        # 返回结果
        return Result(self.LOGOUT.SUCCESS, tokenInfo)

    def checkToken(self, token: str):
        '''
        检查token是否有效。
        '''

        tokenInfo = self.repositoryManager.tokens.get(token=token)

        if tokenInfo is None:
            # token不存在
            return Result(self.AUTH.TOKEN_INVALID)

        if tokenInfo["status"] != 0:
            # token无效，删除
            self.repositoryManager.tokens.delete(
                where={"id": tokenInfo["id"]}
            )
        
        if tokenInfo["status"] == 1:
            # token已过期
            return Result(self.AUTH.TOKEN_EXPIRED)
        elif tokenInfo["status"] == 2:
            # token已退出登录
            return Result(self.AUTH.TOKEN_LOGOUT)
        elif tokenInfo["status"] == 3:
            # token旧设备
            return Result(self.AUTH.TOKEN_OLD_DEVICE)

        # 检查过期时间
        now = datetime.now()
        if now > tokenInfo["expireTime"]:
            # token已过期，更新数据库信息
            self.repositoryManager.tokens.update(
                where={"token": token},
                data={"status": 1}
            )

            self.repositoryManager.tokens.commit()
            return Result(self.AUTH.TOKEN_EXPIRED)
            
        else:
            # token未过期，更新过期时间
            self.repositoryManager.tokens.update(
                where={"token": token},
                data={"expireTime": now + timedelta(minutes=self.availableTime)}
            )


        self.repositoryManager.tokens.commit()

        # 获取用户信息
        userInfo = self.repositoryManager.users.get(id=tokenInfo["userId"])

        tokenInfo = dict(tokenInfo)
        tokenInfo["user"] = userInfo
        return Result(self.AUTH.SUCCESS, tokenInfo)


    def get(self, userId: int | None = None, username: str | None = None):
        '''
        通过id或用户名获取用户信息。
        '''

        if userId:
            result = self.repositoryManager.users.get(id=userId)
        elif username:
            result = self.repositoryManager.users.get(username=username)
        else:
            return Result(self.USER.MISSING_QUERY)

        if result is None:
            return Result(self.USER.USER_NOT_FOUND)

        return Result(self.USER.SUCCESS, result)


    def forceChangePassword(self, userId: int, newPassword: str):
        '''
        强制更改用户的密码。

        注意：本方法直接更改用户的密码，在一般场景，请勿使用。
        '''

        
        passwordHash = generate_password_hash(newPassword)

        try:
            self.repositoryManager.users.update(
                where={"id": userId},
                data={"password": passwordHash}
            )
        except RecordNotFoundError:
            return Result(self.USER.USER_NOT_FOUND)

        return Result(self.USER.SUCCESS)
        
    def changePassword(self, userId: int, oldPasswrod: str, newPassword: str):
        '''
        更改用户的密码。

        传入用户id、旧密码（明文）、新密码（明文）。
        '''

        status, user = self.get(userId=userId)
        
        if status != self.USER.SUCCESS:
            return Result(status)

        user = cast(dict, user)

    
        if not check_password_hash(user["password"], oldPasswrod):
            # 旧密码错误
            return Result(self.USER.OLD_PASSWORD_ERROR)

        # 旧密码正确

        self.forceChangePassword(userId, newPassword)

        return Result(self.USER.SUCCESS)

        
    def create(self,
                username: str,
                password: str,
                isAdmin: bool,
                isAvailable: bool,
                ):

        createTime = datetime.now()

        passwordHash = generate_password_hash(password)

        userId = self.repositoryManager.users.insert(
            username=username,
            password=passwordHash,
            isAdmin=isAdmin,
            isAvailable=isAvailable,
            createdAt=createTime,
        )

        self.repositoryManager.users.commit()

        return Result(self.USER.SUCCESS, userId)

    


