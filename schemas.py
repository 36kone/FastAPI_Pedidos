from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    senha: str
    email: str
    admin: Optional[bool] = False
    ativo: Optional[bool] = True

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

class ItemPedidoSchema(BaseModel):
    preco_unitario: float
    quantidade: int
    sabor: str
    tamanho: str

    class Config: 
        from_attributes = True