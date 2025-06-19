
from fastapi import APIRouter, Depends
from models import Pedido
from dependecies import pegar_sessao
from schemas import PedidoSchema
from sqlalchemy.orm import Session

order_router = APIRouter(prefix='/pedidos', tags=['pedidos'])

@order_router.get('/') 
async def pedidos():
    return {'message': 'orders list:'}

@order_router.post('/pedido')
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {'message:': f'pedido criado com sucesso, ID do pedido: {novo_pedido.id}'}
