from fastapi import Depends, FastAPI
from .routers import balances, monthly_expenses, variable_expenses, form_of_payments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",
    "http://localhost:8001",
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

@app.get("/")
async def root():
    return {"message": "Hello World Mother Fucker"}

