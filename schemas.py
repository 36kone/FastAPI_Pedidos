from pydantic import BaseModel
from typing import Optional, List

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

class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]
    
    class Config: 
        from_attributes = True
