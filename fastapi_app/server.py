from fastapi import FastAPI, HTTPException, Request
from fastapi_app.schemas.request_models import SimpleRequest, SimpleResponse

app = FastAPI()


@app.post("/receiver")
async def receive_messages(request: SimpleRequest):
    """
    Receives messages from the client and returns a response.

    Args:
        request (SimpleRequest): The request object containing the client name and message.

    Returns:
        SimpleResponse: The response object containing the client name and message.

    Raises:
        HTTPException: If the input is invalid.
    """
    try:
        client_name = request.client_name
        message = request.message

        response = SimpleResponse(
            client_name=client_name,
            message=message,
        )
        print(response)
        return response

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Check your message format.",
        )
