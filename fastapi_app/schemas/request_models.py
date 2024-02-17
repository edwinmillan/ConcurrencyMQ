from pydantic import BaseModel


class SimpleRequest(BaseModel):
    client_name: str
    message: str


class SimpleResponse(BaseModel):
    client_name: str
    message: str


class DecryptRequest(BaseModel):
    client_name: str
    encrypted_message_hex: str


class DecryptedResponse(BaseModel):
    client_name: str
    decrypted_message: str
