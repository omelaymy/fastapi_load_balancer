from fastapi import FastAPI

app = FastAPI()


@app.get("/health/", status_code=200)
async def i_am_alive():
    """
    Проверка работоспособности
    """
    return 'I am alive'


@app.get("/")
async def hello():
    return {"Hello": "World"}
