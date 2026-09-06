from multiprocessing.connection import Connection
from threading import Event
from typing import TypedDict
import argparse

class Message(TypedDict):
    command: str
    data: dict

parser = argparse.ArgumentParser(description="ForgeOrder控制台")

parser.add_argument("command", type=str, choices=["shutdown"])

def shutdown():
    pass

def consoleWorker(pipe: Connection,
                   stopEvent: Event, # 这是来自主线程的停止事件
                   
                ):

    while True:
        if stopEvent.is_set():
            break

        message: Message = pipe.recv()

        
        args = parser.parse_args(message["command"].split())

        match args.command:
            case "shutdown":
                shutdown()
                break
        





        

        

