from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    senha: str
    email: str
    admin: Optional[bool]
    ativo: Optional[bool]

    class Config: 
        from_attributes = True

class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True