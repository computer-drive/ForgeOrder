import json

def makeMessage(name: str, data: dict | None= None):
    if data is None:
        data = {}
        
    return json.dumps({
        "name": name,
        "data": data,
    })