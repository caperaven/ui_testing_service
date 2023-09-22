import fastapi
from uvicorn import run

app = fastapi.FastAPI()


@app.get("/")
def index():
    return {"message": "Hello, world!"}


run(app, host="127.0.0.1", port=8000)
