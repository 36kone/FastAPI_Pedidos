from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependecies import pegar_sessao
from main import bcrypt_context, SECRET_KET, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix='/auth', tags=['auth'])

def criar_token(id_usuario, duracao_token = timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    data_expire = datetime.now(timezone.utc) + duracao_token
    dic_info = {'sub': str(id_usuario), 'exp': data_expire}
    jwt_codificado = jwt.encode(dic_info, SECRET_KET, ALGORITHM)
    return jwt_codificado

def verificar_token(usuario, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id==1).first()
    return usuario

def autenticar_usuario(email, senha, session):
     usuario = session.query(Usuario).filter(Usuario.email==email).first()
     if not usuario: 
         return False
     elif not bcrypt_context.verify(senha, usuario.senha):
         return False
     return usuario

@auth_router.get('/')
async def auth():
    return {'message': 'authenticated users:'} 

@auth_router.post('/criar_conta')
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario: 
        raise HTTPException(status_code=400, detail='e-mail ja cadastrado')
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {'message': f'usuario cadastrado com sucesso {usuario_schema.email}'}
    
@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail='usuario nao encontrado ou credencias incorretas')
    else:
        acess_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            'acess_token': acess_token,
            'refresh': refresh_token,
            'token_type': 'Bearer'
        }

@auth_router.get('/refresh')
async def use_refresh_token(token):
    usuario = verificar_token(token)
    acess_token = criar_token(usuario.id)
    return {
            'acess_token': acess_token,
            'token_type': 'Bearer'
        }
    