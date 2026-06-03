from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, verify_token
from schemas import OrderSchema
from sqlalchemy.orm import Session
from models import Order, User



order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(get_session)])



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


@order_router.post("/order/cancel/{id_pedido}")
async def cancel_order(id_pedido: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id == id_pedido).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=403, detail="Você não tem permissão para cancelar este pedido.")
    order.status = "CANCELADO"
    session.commit()
    return {"message": f"Pedido {order.id} cancelado com sucesso!"}