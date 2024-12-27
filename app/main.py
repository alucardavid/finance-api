from fastapi import Depends, FastAPI
from .routers import balances, monthly_expenses, variable_expenses, form_of_payments, incomings, expense_categorys
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

origins = [
    "http://localhost",
    "http://172.19.0.1",
    "http://172.19.0.2",
    "http://172.19.0.3",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://172.19.0.2:8000",
    "http://172.19.0.2:8001",
    "http://172.19.0.3:8000",
    "http://172.19.0.3:8001",
    "http://172.19.0.3:80",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(balances.router, prefix="/balances", tags=["balances"])
app.include_router(monthly_expenses.router, prefix="/monthly-expenses", tags=["monthly-expenses"])
app.include_router(variable_expenses.router, prefix="/variable-expenses", tags=["variable-expenses"])
app.include_router(form_of_payments.router, prefix="/form-of-payments", tags=["form-of-payments"])
app.include_router(incomings.router, prefix="/incomings", tags=["incomings"])
app.include_router(expense_categorys.router, prefix="/expense-categorys", tags=["expense-categorys"])

@app.get("/")
async def root():
    return {"message": "Hello World Mother Fucker Teste WatchTower"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)