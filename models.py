from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

# cria a conexão do seu banco
db = create_engine("sqlite:///banco.db")

# cria a base do banco de dados
Base = declarative_base()



# Clean the table USERS
# session=get_session()
# session.query(User).delete()
# session.commit()

# criar as classes/tabelas do banco de dados
class User(Base):  # USUARIO
    __tablename__ = "USERS"

    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    name = Column("NAME", String, nullable=False)
    email = Column("EMAIL", String, nullable=False)
    password = Column("PASSWORD", String, nullable=False)
    active = Column("ACTIVE", Boolean, default=True)
    admin = Column("ADMIN", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin
# PEDIDO
class Order(Base):
    __tablename__ = "ORDERS"

    # STATUS_ORDERS = (
    #     ("PENDING", "PENDING"),
    #     ("CANCELED", "CANCELED"),
    #     ("COMPLETED", "COMPLETED")
    # )

    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    status = Column("STATUS", String) #pending, canceled, completed
    user = Column("USER",ForeignKey("USERS.ID")) #passa o nome da tabela e o nome do campo da chave estrangeira
    price = Column("PRICE", Float) 
    #itens = 

    def __init__(self, user, status="PENDING", price=0.0):
        self.user = user
        self.status = status
        self.price = price

# ITENS DO PEDIDO
class ItemOrder(Base):
    __tablename__ = "ITEMS_ORDER"

    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    quantity = Column("QUANTITY", Integer)
    topping = Column("TOPPING", String)
    size = Column("SIZE", String)
    price_item = Column("PRICE_ITEM", Float)
    order = Column("ORDER", ForeignKey("ORDERS.ID")) #passa o nome da tabela e o nome do campo da chave estrangeira

    def __init__(self, order, quantity, topping, size, price_item):
        self.order = order
        self.quantity = quantity
        self.topping = topping
        self.size = size
        self.price_item = price_item

# executa a criação dos metadados do seu banco de dados
