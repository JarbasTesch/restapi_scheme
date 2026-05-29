from fastapi import APIRouter, Depends
from dependencies import get_session
from schemas import OrderSchema
from sqlalchemy.orm import Session
from models import Order
order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.get("/")
async def orders():
    """Orders route"""
    return {"message": "Você acessou a rota de pedidos!"}


@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    """Create a new order"""
    new_order = Order(user=order_schema.user_id)
    print(new_order)
    session.add(new_order)
    session.commit()
    return {"message": f"Pedido criado com sucesso! {new_order.id}"}