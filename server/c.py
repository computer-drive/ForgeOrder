import asyncio
import websockets

async def client():
    uri = "ws://localhost:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"已连接到服务器: {uri}")
            print("输入消息发送，输入 'exit' 或 'quit' 退出程序")
            print("-" * 40)
            
            # 创建两个并发任务
            # 1. 发送消息
            # 2. 接收消息
            
            # 创建发送和接收的异步任务
            send_task = asyncio.create_task(send_messages(websocket))
            receive_task = asyncio.create_task(receive_messages(websocket))
            
            # 等待任意一个任务完成（比如用户输入 exit 退出）
            done, pending = await asyncio.wait(
                [send_task, receive_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # 取消另一个未完成的任务
            for task in pending:
                task.cancel()
                
    except websockets.exceptions.ConnectionClosedError:
        print("与服务器的连接已断开")
    except Exception as e:
        print(f"连接出错: {e}")

async def send_messages(websocket):
    """发送消息的任务"""
    while True:
        try:
            # 读取用户输入
            message = await asyncio.get_event_loop().run_in_executor(
                None, input, "你: "
            )
            
            # 检查是否退出
            if message.lower() in ['exit', 'quit', 'q']:
                print("正在退出...")
                break
            
            # 发送消息到服务端
            await websocket.send(message)
            
        except websockets.exceptions.ConnectionClosed:
            print("连接已关闭，无法发送消息")
            break
        except Exception as e:
            print(f"发送消息时出错: {e}")
            break

async def receive_messages(websocket):
    """接收消息的任务"""
    try:
        async for message in websocket:
            print(f"\n服务端: {message}")
            print("你: ", end="", flush=True)  # 重新显示输入提示
    except websockets.exceptions.ConnectionClosed:
        print("\n服务器连接已关闭")
    except Exception as e:
        print(f"\n接收消息时出错: {e}")

if __name__ == "__main__":
    asyncio.run(client())