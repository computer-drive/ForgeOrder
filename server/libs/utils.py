import traceback

def create_server_info_by_exception(e: Exception):
    info = ""
    for line in traceback.format_exception(type(e), e, e.__traceback__):
        info += line
        info += "\n"
    
    return info