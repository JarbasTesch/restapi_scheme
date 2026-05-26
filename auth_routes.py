from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def authenticate():
    """Autentication route"""
    return {"message": "Você acessou a rota de autenticação!"}
