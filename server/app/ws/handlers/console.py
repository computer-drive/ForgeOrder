from websockets.asyncio.server import ServerConnection
from ..context import WebsocketServerContext

from .base import handlerManager


@handlerManager.register("console")
async def consoleHandler(ws: ServerConnection, ctx: WebsocketServerContext):
    pass