import httpx
import os
import asyncio
import uuid
import random
from dotenv import load_dotenv
from nacl.secret import SecretBox
from nacl.encoding import HexEncoder

load_dotenv()


def encrypt_message(message: str, secret_box: SecretBox) -> bytes:
    """
    Encrypts a message using a secret box.

    Args:
        message (str): The message to be encrypted.
        secret_box (SecretBox): The secret box used for encryption.

    Returns:
        bytes: The encrypted message.
    """
    return secret_box.encrypt(message.encode(), encoder=HexEncoder)


async def send_messages(
    messages: list, secret_box: SecretBox, client: httpx.AsyncClient, client_name: str
) -> str:
    """
    Sends a list of messages to a receiver.

    Args:
        messages (list): The list of messages to send.
        secret_box (SecretBox): The secret box used for encryption.
        client (httpx.AsyncClient): The HTTP client used for sending requests.
        client_name (str): The name of the client.

    Returns:
        str: The response from the receiver.

    Raises:
        httpx.HTTPError: If there is an error sending the message.
    """
    for message in messages:
        encrypted_message = encrypt_message(message, secret_box).hex()
        delay = random.randint(1, 10) / 10
        await asyncio.sleep(delay)
        body = {
            "client_name": client_name,
            "encrypted_message_hex": encrypted_message,
        }
        print(f"Sent message: [{client_name}] {encrypted_message} {delay} delay")
        try:
            response = await client.post(
                "http://localhost:8000/receiver",
                json=body,
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"Failed to send message: {e}")


async def main():
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise ValueError("No SECRET_KEY found in environment variables")
    secret_box = SecretBox(bytes.fromhex(secret_key))

    desired_clients = 3
    message_batch_size = 10
    clients = [str(uuid.uuid4())[:8] for _ in range(desired_clients)]

    while True:
        tasks = []
        async with httpx.AsyncClient() as client:
            for client_name in clients:
                messages = [
                    f"[{client_name}] {i+1}-{str(uuid.uuid4())}"
                    for i in range(message_batch_size)
                ]
                tasks.append(
                    send_messages(
                        messages=messages,
                        secret_box=secret_box,
                        client=client,
                        client_name=client_name,
                    )
                )
            await asyncio.gather(*tasks)
            delay = random.randint(1, 5)
            print(f"Resting for {delay} seconds")
            await asyncio.sleep(delay)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting")
    except asyncio.CancelledError:
        print("Asyncio task was cancelled")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
