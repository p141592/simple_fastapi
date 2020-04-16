from gino import Gino

from .application import Application

app = Application()
db = Gino()


@app.get("/ping")
async def root():
    return {"message": "pong"}
