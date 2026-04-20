# this will have get_my_orders
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import get_current_user

my_orders_router = APIRouter()

@my_orders_router.get("/my_orders")
async def get_my_orders(current_user_id: int = Depends(get_current_user)):

    return {"message": "my orders", "current_user_id": current_user_id}