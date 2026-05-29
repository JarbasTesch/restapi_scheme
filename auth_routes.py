from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def crate_token(id: int):
    token = f"aowadawo{id}"
    return token


@auth_router.get("/")
async def home():
    """Padron route"""
    return {"message": "Você acessou a rota de autenticação!", "auth":False}

@auth_router.post("/create_account")
async def create_account(user_schema: UserSchema, session: Session = Depends(get_session)):  
    user = session.query(User).filter(User.email == user_schema.email).first()
    print(user_schema.email, user_schema.password,user_schema. name, user)

    if user:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    
    crypted_password = bcrypt_context.hash(user_schema.password)
    new_user = User(
        email=user_schema.email,
        password=crypted_password,
        name=user_schema.name
    )
    
    session.add(new_user)
    session.commit()
    return {"message": f"Conta criada com sucesso! {user_schema.email}" }



@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == login_schema.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email não encontrado.")
    access_token = crate_token(user.id)
    return{
        "access_token": access_token,
        "token_type": "bearer"
        }