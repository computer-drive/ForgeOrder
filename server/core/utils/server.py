from flask import jsonify, request
# from schema import Args
import os
import socket


# def verify_args(args: dict, args_format: list[Args]):
#     '''
#     验证参数是否符合要求
#     '''
#     args_invalid = []
#     for arg in args_format:
#         if arg["required"] and arg["arg_name"] not in args:
#             args_invalid.append(arg["arg_name"])
    
#     return args_invalid
      
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