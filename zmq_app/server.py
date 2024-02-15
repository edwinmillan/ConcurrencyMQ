import asyncio
import zmq
import zmq.asyncio
import os
from dotenv import load_dotenv
from nacl.secret import SecretBox
from nacl.encoding import HexEncoder
from nacl.exceptions import CryptoError

load_dotenv()


async def receive_messages(context, secret_box: SecretBox):
    """
    Receive messages from the ZeroMQ socket and decrypt them using the provided secret box.

    Args:
        context (zmq.Context): The ZeroMQ context.
        secret_box (SecretBox): The secret box used for message decryption.

    Raises:
        zmq.error.ZMQError: If a ZeroMQ error occurs.
        Exception: If an unexpected error occurs.
    """
    try:
        with context.socket(zmq.PULL) as socket:
            socket.bind("tcp://*:5555")
            while True:
                enc_message = await socket.recv_string()
                try:
                    dec_message = secret_box.decrypt(
                        bytes.fromhex(enc_message), encoder=HexEncoder
                    ).decode()
                    print(f"Received message: {dec_message}")
                except ValueError:
                    print("Received non-hexadecimal message.")
                except CryptoError:
                    print("Received a message that could not be decrypted. Check Key.")
    except zmq.error.ZMQError as e:
        print(f"ZeroMQ error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


async def main():
    context = zmq.asyncio.Context()
    secret_key = bytes.fromhex(os.getenv("SECRET_KEY"))
    secret_box = SecretBox(secret_key)
    await receive_messages(context=context, secret_box=secret_box)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting")
    except asyncio.CancelledError:
        print("Asyncio task was cancelled")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
