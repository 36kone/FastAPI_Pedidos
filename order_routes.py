from fastapi import APIRouter, Depends, HTTPException
from models import Pedido, Usuario, ItemPedido
from dependecies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from sqlalchemy.orm import Session

order_router = APIRouter(prefix='/pedidos', tags=['pedidos'], dependencies=[Depends(verificar_token)])

@order_router.get('/') 
async def pedidos():
    return {'message': 'orders list:'}

@order_router.post('/pedido')
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {'message:': f'pedido criado com sucesso, ID do pedido: {novo_pedido.id}'}

@order_router.post('/pedido/cancelar/{id_pedido}')
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido: 
        raise HTTPException(status_code=400, detail='pedido nao encontrado')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=400, detail='voce nao tem autorizacao para fazer essa modificacao')
    pedido.status = 'CANCELADO'
    session.commit()
    return{
        'message': f'pedido numero: {pedido.id} cancelado com sucesso',
        'pedido': pedido
    }

@order_router.get('/listar')
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(status_code=400, detail='voce nao tem autorizacao para realizar essa operacao')
    else: 
        pedidos = session.query(Pedido).all()
        return{
            'pedidos': pedidos
        }
    
@order_router.post('/pedido/adicionar-item/{id_pedido}')
async def adicionar_item(id_pedido: int, item_pedido_schema: ItemPedidoSchema, 
                         session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail='pedido nao encontrado')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='voce nao tem autorizacao para realizar essa operacao')
    item_pedido = ItemPedido(id_pedido, item_pedido_schema.preco_unitario, item_pedido_schema.quantidade, 
                             item_pedido_schema.sabor, item_pedido_schema.tamanho)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        'message': 'item adicionado com sucesso',
        'item_id': id_pedido,
        'preco_pedido': pedido.preco
    }