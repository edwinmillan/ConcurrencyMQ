from fastapi import FastAPI, HTTPException, Request

app = FastAPI()


@app.post("/receiver")
async def receive_messages(request: Request):
    """
    Receive messages from the client.

    Args:
        request (Request): The incoming request object.

    Returns:
        dict: The response containing the client name and message.

    Raises:
        HTTPException: If the input is invalid.
    """
    request_data = await request.json()
    try:
        client_name = request_data.get("client_name")
        message = request_data.get("message")

        response = {
            "client_name": client_name,
            "message": message,
        }
        print(response)
        return response

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Check your message format.",
        )
