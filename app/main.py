from fastapi import Depends, FastAPI

from .routers import balances, monthly_expenses

app = FastAPI()

app.include_router(balances.router, prefix="/balances", tags=["balances"])
app.include_router(monthly_expenses.router, prefix="/monthly-expenses", tags=["monthly-expenses"])

@app.get("/")
async def root():
    return {"message": "Hello"}