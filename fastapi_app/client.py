import httpx
import asyncio
import uuid
import random


async def send_messages(
    messages: list, client: httpx.AsyncClient, client_name: str
):
    """
    Sends a list of messages to the receiver endpoint.

    Args:
        messages (list): The list of messages to be sent.
        client (httpx.AsyncClient): The HTTP client used to send the messages.
        client_name (str): The name of the client sending the messages.

    Raises:
        httpx.HTTPError: If there is an error while sending the message.

    Returns:
        None
    """
    for message in messages:
        try:
            delay = random.randint(1, 10) / 10
            await asyncio.sleep(delay)
            body = {
                "client_name": client_name,
                "message": message,
            }
            response = await client.post(
                "http://localhost:8000/receiver",
                json=body,
            )
            response.raise_for_status()
            print(f"Sent message: {message} {delay} delay")
        except httpx.HTTPError as e:
            print(f"Failed to send message: {e}")


async def main():
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
                        messages=messages, client=client, client_name=client_name
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
