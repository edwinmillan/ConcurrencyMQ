import asyncio
import zmq
import zmq.asyncio
import uuid
import random
import os
from dotenv import load_dotenv
from nacl.secret import SecretBox
from nacl.encoding import HexEncoder

load_dotenv()

CLIENT_NAME = str(uuid.uuid4())[:8]


def encrypt_message(message: str, secret_box: SecretBox) -> bytes:
    return secret_box.encrypt(message.encode(), encoder=HexEncoder)


async def send_messages(context, messages: list, secret_box: SecretBox):
    try:
        with context.socket(zmq.PUSH) as socket:
            socket.connect("tcp://localhost:5555")
            for message in messages:
                enc_message = encrypt_message(message, secret_box).hex()

                delay = random.randint(1, 10) / 10
                sent_message = enc_message
                await asyncio.sleep(delay)
                await socket.send_string(sent_message)
                print(f"Sent message: {sent_message} {delay} delay")
    except zmq.error.ZMQError as e:
        print(f"ZeroMQ error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


async def main():
    context = zmq.asyncio.Context()
    secret_key = bytes.fromhex(os.getenv("SECRET_KEY"))
    secret_box = SecretBox(secret_key)
    while True:
        messages = [f"[{CLIENT_NAME}] {i+1}-{str(uuid.uuid4())}" for i in range(10)]
        await send_messages(context=context, messages=messages, secret_box=secret_box)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting")
    except asyncio.CancelledError:
        print("Asyncio task was cancelled")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
