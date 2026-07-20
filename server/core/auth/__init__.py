import hashlib
import time
import threading

from core.auth.schema import UserInfo



class AuthManager:
    def __init__(self, secret_key, available_time: int):
        # available_time: 单位分钟，有效期限
        self.secret_key = secret_key
        self.available_time = available_time

        self.tokens = []

        self._lock = threading.Lock()

    def user_login(self,
                   user: UserInfo,
                   device_ip: str,
                   cover: bool = False,
                   ):
        
        # 检查该用户是否已经存在
        for i in range(len(self.tokens)):
            token_item = self.tokens[i]

            if token_item["user"]["username"] == user["username"]:
                if token_item["expire"] < int(time.time()):
                    token_item["is_available"] = False  # 添加这行
                    token_item["cause_expire"] = "expire"
                    break

                if token_item["cause_expire"] == "logout":
                    token_item["is_available"] = False  # 添加这行
                    break

                if token_item["cause_expire"] == "old_device":
                    token_item["is_available"] = False  # 添加这行
                    break
                
                # token有效，判断ip是否相同
                if token_item["device_ip"] == device_ip:
                    return False, (0, token_item)#  重复登录
                
                else:
                    # 新设备登录，判断要不要覆盖旧设备
                    if cover:
                        self.tokens[i]["is_available"] = False
                        self.tokens[i]["cause_expire"] = "old_device"
                        break

                    else:
                        return False, (1, token_item["device_ip"]) # 新设备登录
                    
                
                
        # 不存在这个用户或覆盖旧设备，创建新token
        token = hashlib.sha512(
            (user["username"] + self.secret_key + str(time.time())).encode("utf-8")
        ).hexdigest()

        now = int(time.time())
        expire = now + self.available_time * 60

        self.tokens.append({
            "user": user,
            "token": token,
            "expire": expire,
            "device_ip": device_ip,
            "is_available": True,
            "cause_expire": None,
            })
        
        
        return True, token
    
    def user_logout(self, token: str):
        for token_item in self.tokens:
            if token_item["token"] == token:
                token_item["is_available"] = False
                token_item["cause_expire"] = "logout"
                
                return token_item
            

    def verify(self, token: str):
        '''
        验证token是否有效

        Return:
        0 - 无效token
        1 - 退出登录
        2 - 过期
        3 - 旧设备登录
        '''
        for token_item in self.tokens:
            with self._lock:  # 获取锁
                for i in range(len(self.tokens) - 1, -1, -1):
                token_item = self.tokens[i]
                if token_item["token"] == token:
                    ...
                    del self.tokens[i]
                    return (False, token_item["cause_expire"])
                
            return (False, None)
    
    def update_time(self, token):
        '''
        更新过期时间。

        注意：使用本方法时应以确定token有效
        '''

        for i, token_item in enumerate(self.tokens):
            if token_item["token"] == token:
                token_item["expire"] = int(time.time()) + self.available_time * 60
                return token_item
            
        return None


        
    


        
