import os
import socket
import traceback
from typing import Literal

from flask import jsonify, request

from typehints.utils import Args


def create_server_info_by_exception(e: Exception):
    info = ""
    for line in traceback.format_exception(type(e), e, e.__traceback__):
        info += line
        info += "\n"
    
    return info

def pad_string(string: str,
               length: int,
               pad_char: str = "0",
               position: Literal["left", "right"] = "left") -> str:
    '''
    根据长度补齐字符串
    '''

    if len(string) >= length:
        return string
    
    pad_length = length - len(string)

    if position == "left":
        return pad_char * pad_length + string
    else:
        return string + pad_char * pad_length
    
def verify_args(args: dict, args_format: list[Args]):
    '''
    验证参数是否符合要求
    '''
    args_invalid = []
    for arg in args_format:
        if arg["required"] and arg["arg_name"] not in args:
            args_invalid.append(arg["arg_name"])
    
    return args_invalid
      
def make_response(status: int, data: dict | list | int | str | bool | None):
    return jsonify({
        "status": status,
        "data": data
    })

def get_client_ip():
    if os.environ["ENV"] == "dev":
        # print(1)
        return request.headers["X-Real-IP"]
    else:
        return request.remote_addr
    

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"