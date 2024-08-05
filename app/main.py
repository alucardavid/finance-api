from fastapi import Depends, FastAPI

from .routers import balances

app = FastAPI()

app.include_router(balances.router, prefix="/balances", tags=["balances"])

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}