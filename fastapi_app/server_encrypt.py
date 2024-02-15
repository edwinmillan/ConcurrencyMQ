import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from nacl.secret import SecretBox
from nacl.encoding import HexEncoder
from nacl.exceptions import CryptoError

load_dotenv()

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY found in environment variables")
SECRET_BOX = SecretBox(bytes.fromhex(SECRET_KEY))


@app.post("/receiver")
async def receive_messages(request: Request):
    request_data = await request.json()
    try:
        client_name = request_data.get("client_name")
        encrypted_message_hex = request_data.get("encrypted_message_hex")
        encrypted_message = bytes.fromhex(encrypted_message_hex)
        decrypted_message = SECRET_BOX.decrypt(
            encrypted_message, encoder=HexEncoder
        ).decode()
        response = {
            "client_name": client_name,
            "decrypted_message": decrypted_message,
        }
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
