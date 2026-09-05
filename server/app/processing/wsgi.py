from typing import cast

from waitress.server import TcpWSGIServer
from waitress.channel import HTTPChannel

# 这是一个自定义的HTTPChannel类，用于实现优雅关闭
class _CustomHTTPChannel(HTTPChannel):


    def del_channel(self, map=None):
        super().del_channel(map)

        self.server = cast(AppServer, self.server)

        # 是否排空请求，是否有活动连接
        if self.server.draining and not self.server.active_channels:
            # 没有活动连接了，完成关闭
            self.server.finishedShutdown()


# 这是一个自定义的WSGI服务器类，用于实现优雅关闭
class AppServer(TcpWSGIServer):
    channel_class = _CustomHTTPChannel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.draining = False  # 是否准备关闭，排空请求


    def gracefulShutdown(self):
        # 优雅关闭
        if self.draining:
            return  # 已经在排空请求了

        self.draining = True

        # 不再接受新的TCP连接
        self.accepting = False  

        # 判断是否有连接
        if not self.active_channels:
            self.finishedShutdown()


    def finishedShutdown(self):
        # 完成关闭
        self.close()


