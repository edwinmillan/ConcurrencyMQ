import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from nacl.secret import SecretBox
from nacl.encoding import HexEncoder
from nacl.exceptions import CryptoError
from fastapi_app.schemas.request_models import DecryptRequest, DecryptedResponse

load_dotenv()

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY found in environment variables")
SECRET_BOX = SecretBox(bytes.fromhex(SECRET_KEY))


@app.post("/receiver")
async def receive_messages(request: DecryptRequest):
    """
    Receive encrypted messages from clients and decrypt them.

    Args:
        request (DecryptRequest): The request object containing the client name and encrypted message.

    Returns:
        DecryptedResponse: The response object containing the client name and decrypted message.

    Raises:
        HTTPException: If decryption fails or the input is invalid.
    """
    try:
        client_name = request.client_name
        encrypted_message_hex = request.encrypted_message_hex
        encrypted_message = bytes.fromhex(encrypted_message_hex)
        decrypted_message = SECRET_BOX.decrypt(
            encrypted_message, encoder=HexEncoder
        ).decode()
        response = DecryptedResponse(
            client_name=client_name,
            decrypted_message=decrypted_message,
        )
        print(response)
        return response

    except CryptoError:
        raise HTTPException(
            status_code=400, detail="Decryption failed. Invalid message or key."
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Check your encrypted message format.",
        )
