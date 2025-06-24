from fastapi import APIRouter, Depends, HTTPException
from models import Pedido, Usuario, ItemPedido
from dependecies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from sqlalchemy.orm import Session
from typing import List

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
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
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

@order_router.post('/pedido/remover-item/{id_item_pedido}')
async def remover_item(id_item_pedido: int,
                         session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail='item no pedido nao existente')
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.id).first()
    if not pedido:
        raise HTTPException(status_code=400, detail='pedido nao existente')
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='voce nao tem autorizacao para realizar essa operacao')
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        'message': 'item removido com sucesso',
        'quantidade_itens_pedido': len[pedido.itens],
        'pedido': item_pedido.pedido
    }

@order_router.post('/pedidos/finalizar/{id_pedido}')
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido: 
        raise HTTPException(status_code=400, detail='pedido nao encontrado')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=400, detail='voce nao tem autorizacao para realizar essa operacao')
    pedido.status = 'FINALIZADO'
    session.commit()
    return{
        'message': f'pedido {pedido.id} finalizado com sucesso',
        'pedido': pedido
    }

@order_router.get('/pedido/{id_pedido}')
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido: 
        raise HTTPException(status_code=400, detail='pedido nao encontrado')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=400, detail='voce nao tem autorizacao para realizar essa operacao')
    return pedido

@order_router.get('/listar/pedidos-usuario', response_model=List[ResponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
        pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
        return pedidos