import asyncio
import zmq
import zmq.asyncio


async def receive_messages(context):
    try:
        with context.socket(zmq.PULL) as socket:
            socket.bind("tcp://*:5555")
            while True:
                message = await socket.recv_string()
                print(f"Received message: {message}")
    except zmq.error.ZMQError as e:
        print(f"ZeroMQ error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


async def main():
    context = zmq.asyncio.Context()
    await receive_messages(context)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting")
    except asyncio.CancelledError:
        print("Asyncio task was cancelled")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
