from fastapi import APIRouter
from ..internal import db

router = APIRouter()

@router.get("/")
def read_balances():
    """Retrieve balances"""
    return {"balances": db.get_balances()}