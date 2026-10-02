import asyncio
import sys
import time
import traceback

import websockets.exceptions as websocketsExceptions
from websockets import serve
from websockets.asyncio.server import ServerConnection


from ..processing.base import WorkerPipe
from ..config import ConfigManager, CONFIG
from .message import makeMessage
from .schema import MESSAGEES
lazy from .handlers.base import handlerManager as hm_
lazy from .context import WebsocketServerContext, Client
from core.log import Logger

def addClient(ws: ServerConnection, ctx: 'WebsocketServerContext'):

    def whenClosed(c: Client):
        ctx.logger.info("客户端 {client} 断开连接", {
            "client": c.address,
        }, "Client", "Disconnected")


    return Client(
        ws,
        ws.remote_address,
        time.time(),
        whenClosed, 
    )


async def websocketHandler(websocket: ServerConnection, ctx: 'WebsocketServerContext'):
    ctx.logger.info("客户端 {client} 连接成功", {
        "client": websocket.remote_address,
    }, "Client", "Connected")

    client = addClient(websocket, ctx)
    ctx.clients.append(client)

    try:
        async for message in websocket:
            ctx.logger.debug("客户端 {client} 收到消息：{message}", {
                "message": message,
            }, "Client", "Received")

            
            # 调用处理函数
            await ctx.handlerManager.handle(client, message)

    
    except websocketsExceptions.ConnectionClosedOK:
        pass

    except websocketsExceptions.ConnectionClosedError:
        ctx.logger.warning("客户端 {client} 连接异常关闭", {
            "client": websocket.remote_address,
        }, "Client", "ConnectionClosed")

    except websocketsExceptions.InvalidState:
        ctx.logger.warning("客户端 {client} 连接不可用", {
            "client": websocket.remote_address,
        }, "Client", "ConnectionUnavailable")

    except Exception as e:
        # 捕获除websocket连接异常以外的所有异常
        type, value, tb = sys.exc_info()

        ctx.logger.error("客户端 {client} 发生错误：{error}", {
            "client": websocket.remote_address,
            "error": {
                "type": type.__name__, #type: ignore
                "value": str(value),
                "traceback": traceback.format_exception(type, value, tb),
    
            },
        }, "Client", "Error")

        # 发送关闭消息
        await websocket.send(makeMessage(MESSAGEES.SERVER_ERROR))


    finally:
        await client.close()



async def listenPipe(childPipe: WorkerPipe, context, logger):
    loop = asyncio.get_running_loop()

    try:
        if sys.platform == "win32":
            # Windows: ProactorEventLoop 不支持 add_reader，
            # SelectorEventLoop 又不认管道句柄，只能用线程池轮询。
            while True:
                has_data = await loop.run_in_executor(None, childPipe.poll, 0.5)
                if not has_data:
                    continue

                message = childPipe.recv()
                logger.debug("收到消息：{type} {data}", {
                    "type": message.type,
                    "data": message.data,
                }, "WebsocketPipe", "Received")

                if message.type == "stop":
                    break
        else:
            # Unix: 用 add_reader，零轮询开销
            fd = childPipe.pipe.fileno()
            dataReady = asyncio.Event()
            loop.add_reader(fd, dataReady.set)
            try:
                while True:
                    if not childPipe.poll():
                        await dataReady.wait()
                        dataReady.clear()
                        continue

                    message = childPipe.recv()
                    logger.debug("收到消息：{type} {data}", {
                        "type": message.type,
                        "data": message.data,
                    }, "WebsocketPipe", "Received")

                    if message.type == "stop":
                        break
            finally:
                loop.remove_reader(fd)

    except (EOFError, OSError) as e:
        logger.warning("管道已关闭：{error}", {
            "error": str(e),
        }, "WebsocketPipe", "Closed")



async def websocketServer(childPipe: WorkerPipe, logger: Logger, config: ConfigManager):
    host = config.get(CONFIG.WS_HOST)
    port = config.get(CONFIG.WS_PORT)

    context = WebsocketServerContext(childPipe, logger, config, hm_)

    async def _websocketHandler(websocket):
        await websocketHandler(websocket, context)

    async with serve(_websocketHandler, host, port) as server:

        # 启动管道监听
        pipeTask = asyncio.create_task(
            listenPipe(childPipe, context, logger)
        )

        
        logger.info("Worker 启动成功（监听：ws://{host}:{port}）", {
            "host": host,
            "port": port,
        }, "WebSocket", "Started")


        childPipe.send("start")


        try:
            await pipeTask
        finally:
            pipeTask.cancel()
            logger.info("WebSocket服务已停止", {}, "WebSocket", "Stopped")
