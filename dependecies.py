from fastapi import Depends, HTTPException
from main import SECRET_KET, ALGORITHM, oauth2_scheme
from models import db, Usuario
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError

def pegar_sessao():
    try: 
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KET, ALGORITHM)
        id_usuario = dic_info.get('sub')
    except JWTError:
        raise HTTPException(status_code=401, detail='Acesso negado, verifique o token')
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not id_usuario:
            raise HTTPException(status_code=401, detail='Acesso invalido, verifique a validade do token')
    return usuario