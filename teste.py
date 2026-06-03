# from dependencies import get_session
from models import User, db
from sqlalchemy.orm import sessionmaker


def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


session=next(get_session())
# session.query(User).delete()
# session.commit()

session.query(User).filter(User.name == "admin").delete()
session.commit()