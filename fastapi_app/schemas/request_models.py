from pydantic import BaseModel


class DecryptedRequest(BaseModel):
    client_name: str
    encrypted_message_hex: str


class DecryptedResponse(BaseModel):
    client_name: str
    decrypted_message: str
