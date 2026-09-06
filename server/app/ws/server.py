from multiprocessing.connection import Connection
import asyncio
import sys
import time

import websockets.exceptions as websocketsExceptions
from websockets import serve
from websockets.asyncio.server import ServerConnection

from ..processing.log import WorkerLogger
from ..config import ConfigManager, CONFIG
lazy from .context import WebsocketServerContext, Client
from .message import makeMessage
from .schema import MESSAGEES
lazy from .handlers.base import handlerManager as hm_
from ..processing.excepthook import _generateErrorMessage

def addClient(ws: ServerConnection, ctx: 'WebsocketServerContext'):

    def whenClosed(c: Client):
        ctx.logger.info({
            "client": c.address,
        }, "Client", "Disconnected")


    return Client(
        ws,
        ws.remote_address,
        time.time(),
        whenClosed, 
    )


async def websocketHandler(websocket: ServerConnection, ctx: 'WebsocketServerContext'):
    ctx.logger.info({
        "client": websocket.remote_address,
    }, "Client", "Connected")

    client = addClient(websocket, ctx)
    ctx.clients.append(client)

    try:
        async for message in websocket:
            ctx.logger.debug({
                "message": message,
            }, "Client", "Received")

            
            # 调用处理函数
            await ctx.handlerManager.handle(client, message)

    
    except websocketsExceptions.ConnectionClosedOK:
        pass

    except websocketsExceptions.ConnectionClosedError:
        ctx.logger.warning({
            "client": websocket.remote_address,
        }, "Client", "ConnectionClosed")

    except websocketsExceptions.InvalidState:
        ctx.logger.warning({
            "client": websocket.remote_address,
        }, "Client", "ConnectionUnavailable")

    except Exception as e:
        # 捕获除websocket连接异常以外的所有异常
        ctx.logger.error({
            "client": websocket.remote_address,
            "error": _generateErrorMessage(*sys.exc_info()),
        }, "Client", "Error")

        # 发送关闭消息
        await websocket.send(makeMessage(MESSAGEES.SERVER_ERROR))


    finally:
        await client.close()



async def websocketServer(childPipe: Connection, logger: WorkerLogger, config: ConfigManager):
    host = config.get(CONFIG.WS_HOST)
    port = config.get(CONFIG.WS_PORT)

    context = WebsocketServerContext(childPipe, logger, config, hm_)

    async def _websocketHandler(websocket):
        await websocketHandler(websocket, context)

    async with serve(_websocketHandler, host, port) as server:

        logger.info({
            "host": host,
            "port": port,
        }, "WebSocket", "Started")

        await asyncio.Future()

        logger.info("", "WebSocket", "Stopped")
