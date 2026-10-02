class UserError(Exception):
    '''已弃用'''
    hint: str = ""
    msg: str = ""