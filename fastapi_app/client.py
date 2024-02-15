import httpx
import asyncio
import uuid


CLIENT_NAME = str(uuid.uuid4())[:8]


async def send_message(message: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/receiver",
            json={
                "client_name": CLIENT_NAME,
                "message": message,
            },
        )
        print(response.json())
        return response.json()


async def main():
    messages = [f"[{CLIENT_NAME}] {i+1}-{str(uuid.uuid4())}" for i in range(10)]
    await asyncio.gather(*[send_message(message) for message in messages])


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting")
    except asyncio.CancelledError:
        print("Asyncio task was cancelled")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
