import asyncio
import zmq
import zmq.asyncio
import uuid
import random

client_name = str(uuid.uuid4())[:8]


async def send_messages(context, messages: list):
    try:
        with context.socket(zmq.PUSH) as socket:
            socket.connect("tcp://localhost:5555")
            for message in messages:
                delay = random.randint(1, 10) / 10
                await asyncio.sleep(delay)
                await socket.send_string(f"{message} {delay} delay")
                print(f"Sent message: {message} {delay} delay")
    except zmq.error.ZMQError as e:
        print(f"ZeroMQ error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


async def main():
    context = zmq.asyncio.Context()
    while True:
        messages = [f"[{client_name}] {i+1}-{str(uuid.uuid4())}" for i in range(10)]
        await send_messages(context, messages)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting")
    except asyncio.CancelledError:
        print("Asyncio task was cancelled")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
