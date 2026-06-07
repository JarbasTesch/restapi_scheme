from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, verify_token
from schemas import OrderSchema, OrderItemSchema, OrderResponseSchema
from sqlalchemy.orm import Session
from models import Order, User, ItemOrder
from typing import List

#TODO: implementar paginação, não retornar todos os pedidos de uma vez


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


@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id == order_id).first()
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


@order_router.post("/order/add_item/{order_id}")
async def add_item_to_order(order_id: int,
                            order_item_schema: OrderItemSchema,
                            session: Session = Depends(get_session),
                            user: User = Depends(verify_token)):
    
    order = session.query(Order).filter(Order.id == order_id).first()
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


@order_router.post("/order/remove_item/{item_order_id}")
async def remove_item_from_order(item_order_id: int,
                            session: Session = Depends(get_session),
                            user: User = Depends(verify_token)):
    
    item_order = session.query(ItemOrder).filter(ItemOrder.id == item_order_id).first()

    if not item_order:
        raise HTTPException(status_code=404, detail="Item do pedido não encontrado.")

    order = item_order.order
    print(f"Pedido: {order}")

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=403, detail="Você não tem permissão para remover itens deste pedido.")
    
    session.delete(item_order)
    session.flush()
    order.price_calculation()
    session.commit()
    
    return {"message": f"Item removido do pedido {order.id} com sucesso!",
            "order_price": order.price,
            "order_quantity": len(order.itens)}


@order_router.post("/order/finish/{order_id}")
async def finish_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=403, detail="Você não tem permissão para finalizar este pedido.")
    order.status = "FINALIZADO"
    session.commit()
    return {"message": f"Pedido {order.id} finalizado com sucesso!", "order_price": order.price}


@order_router.get("/order/{order_id}")
async def view_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=403, detail="Você não tem permissão para finalizar este pedido.")
    
    return {"Quantidade de itens": len(order.itens),
            "Pedido": order}


@order_router.get("/list/user-orders")
async def list_user_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    orders = session.query(Order).filter(Order.user == user.id).all()
    return {"orders": orders}


@order_router.get("/list/user-order-resume", response_model=List[OrderResponseSchema])
async def list_user_order_resume(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    orders = session.query(Order).filter(Order.user == user.id).all()
    return orders