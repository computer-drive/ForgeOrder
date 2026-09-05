from multiprocessing.connection import Connection
import asyncio
import json

import websockets
import websockets.asyncio
import websockets.asyncio.server

from ..processing.log import WorkerLogger
from ..config import ConfigManager, CONFIG
from .context import WebsocketServerContext
from .message import makeMessage
from .schema import MESSAGEES
from .handlers.base import handlerManager


async def websocketHandler(websocket: websockets.asyncio.server.ServerConnection, ctx: WebsocketServerContext):
    ctx.logger.info({
        "client": websocket.remote_address,
    }, "Client", "Connected")

    try:
        async for message in websocket:
            ctx.logger.debug({
                "message": message,
            }, "Client", "Received")

            # 解析 JSON 消息
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                await websocket.send(makeMessage(MESSAGEES.MESSAGE_INVALID))
                continue

            # 验证消息格式
            if "name" not in data or "data" not in data:
                await websocket.send(makeMessage(MESSAGEES.MESSAGE_INVALID))
                continue

            # 处理消息逻辑
            handler = handlerManager.match(data["name"])

            if handler is None:
                await websocket.send(makeMessage(MESSAGEES.NAME_NOT_FOUND))
                continue
            
            await handler(websocket, ctx)


    
    except websockets.exceptions.ConnectionClosedOK:
        ctx.logger.info({
            "client": websocket.remote_address,
        }, "Client", "Disconnected")

    except Exception as e:
        ctx.logger.error({
            "client": websocket.remote_address,
            "error": str(e),
        }, "Client", "Error")


    finally:
        await websocket.close()



async def websocketServer(childPipe: Connection, logger: WorkerLogger, config: ConfigManager):
    host = config.get(CONFIG.WS_HOST)
    port = config.get(CONFIG.WS_PORT)

    context = WebsocketServerContext(childPipe, logger, config)

    async def _websocketHandler(websocket):
        await websocketHandler(websocket, context)

    async with websockets.serve(_websocketHandler, host, port) as server:

        logger.info({
            "host": host,
            "port": port,
        }, "WebSocket", "Started")

        await asyncio.Future()

        logger.info("", "WebSocket", "Stopped")
