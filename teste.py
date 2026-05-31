from dependencies import get_session
from models import User


session=next(get_session())
session.query(User).delete()
session.commit()