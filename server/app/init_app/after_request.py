import time

from flask import g, Response


def after_request(response: Response):
    g.end_time = time.time()

    cost: float = (g.end_time - g.start_time) * 1000 # 转换为毫秒

    g.logger.info({
        "status": response.status_code,
        "size": response.content_length, #bytes
        "duration": round(cost, 2), #ms
    }, "ResponseInfo")

    return response
