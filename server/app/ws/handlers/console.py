
from ..context import WebsocketServerContext, Client
from ..handlerManager import HandlerManager


handler = HandlerManager()

@handler.register("console")
async def consoleHandler(client: Client, ctx: WebsocketServerContext):
    await client.send("received", {
        "data": "thank you"
    })