# from dependencies import get_session
from models import ItemOrder, Order, User, db
from sqlalchemy.orm import sessionmaker





# Clean the table USERS
# session=get_session()
# session.query(User).delete()
# session.commit()





def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

session=next(get_session())

item_order_id = 4

item_order = session.query(ItemOrder).filter(ItemOrder.id == item_order_id).first()
input(f'Item order encontrado: {item_order.topping} tamanho: {item_order.size}. Pressione Enter para continuar...')

order = item_order.order
input(f"Pedido: {order}")

session.delete(item_order)
session.flush()
order.price_calculation()
session.commit()

print({"message": f"Item removido do pedido {order.id} com sucesso!",
        "order_price": order.price,
        "order_quantity": len(order.itens)}
)