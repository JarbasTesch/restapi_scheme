from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session, verify_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm



auth_router = APIRouter(prefix="/auth", tags=["auth"])


def create_token(user_id: int, token_duration: int=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire_date = datetime.now(timezone.utc) + token_duration
    dic_info = {"sub": str(user_id), "exp": expire_date}
    jwt_encoded = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encoded


def auth_user(email: str, password: str, session: Session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


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
        name=user_schema.name,
        admin=user_schema.admin
    )
    
    session.add(new_user)
    session.commit()
    return {"message": f"Conta criada com sucesso! {user_schema.email}" }



@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = auth_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Email não encontrado.")
    access_token = create_token(user.id)
    refresh_token = create_token(user.id, token_duration=timedelta(days=7))
    return{
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
        }



@auth_router.post("/login-form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = auth_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Email não encontrado.")
    access_token = create_token(user.id)
    return{
        "access_token": access_token,
        "token_type": "Bearer"
        }



@auth_router.post("/refresh")
async def use_refresh_token(user: User = Depends(verify_token)):
    acess_token = create_token(user.id)
    return{
        "access_token": acess_token,
        "token_type": "Bearer"
    }