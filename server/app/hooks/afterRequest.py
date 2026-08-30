import time

from flask import Response

from app.utils import g


def afterRequest(response: Response):
    g.endTime = time.time()

    cost: float = (g.endTime - g.startTime) * 1000 # 转换为毫秒

    g.logger.setCategory("Request")

    logInfo = {
        "httpStatus": response.status_code,
        "size": response.content_length, #bytes
        "duration": round(cost, 2), #ms
    }


    g.logger.info(logInfo, "ResponseInfo")

    data = response.json

    if data:

        if  data.get("status") == None and data.get("message") == None:
            pass
        else:
            if data["status"] != 0:
                g.logger.info({
                                "status": data["status"],
                                "message": data["message"],
                }, "StatusWarning")

    if cost > 500:
        g.logger.warning('', "TooSlowRequest")

    return response
