from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router  # noqa: E402
from order_routes import order_router  # noqa: E402

app.include_router(auth_router)
app.include_router(order_router)


# para rodar o nosso código, executar no terminal: uvicorn main:app --reload
