# Concurrency with ZeroMQ

Having some fun just sending data between n clients and 1 server.

## TODO

- ~~Incorporate some message encryption to see how that flows.~~
- ~~Do this with FastAPI~~


# Requirements
I've got the requirements.txt included but I'm also running [poetry](https://python-poetry.org/), so you should be able to `poetry install` if you've got it running. 


## Starting The FastAPI Server
Don't run both at the same time, I've got it using port 8000. 

### Encrypted Server (To be used with fastapi_app/client_encrypt.py)
`hypercorn fastapi_app.server_encrypt:app --reload`

### Unencrypted Server (To be used with fastapi_app/client.py)
`hypercorn fastapi_app.server:app --reload`