from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, verify_token
from schemas import OrderSchema, OrderItemSchema
from sqlalchemy.orm import Session
from models import Order, User, ItemOrder



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

@order_router.get("/list")
async def list_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para acessar esta rota.")
    
    #TODO: implementar paginação, não retornar todos os pedidos de uma vez
    orders = session.query(Order).all()
    return {"orders": orders}

@order_router.post("/order/add_item/{id_pedido}")
async def add_item_to_order(id_pedido: int,
                            order_item_schema: OrderItemSchema,
                            session: Session = Depends(get_session),
                            user: User = Depends(verify_token)):
    
    order = session.query(Order).filter(Order.id == id_pedido).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=403, detail="Você não tem permissão para adicionar itens a este pedido.")
    
    order_item = ItemOrder(
        quantity=order_item_schema.quantity,
        topping=order_item_schema.topping,
        size=order_item_schema.size,
        price_item=order_item_schema.price_item,
        order=order
    )

    order.itens.append(order_item)
    
    order.price_calculation()
    
    session.add(order)
    session.commit()
    return {"message": f"Item adicionado ao pedido {order.id} com sucesso!",
            "item_id": order_item.id,
            "order_price": order.price}