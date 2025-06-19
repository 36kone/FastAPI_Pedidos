from sqlalchemy import create_engine, Integer, Boolean, Column, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

db = create_engine('sqlite:///banco.db')

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String)
    email = Column('email', String)
    senha = Column('senha', String)
    ativo = Column('ativo', Boolean)
    admin = Column('admin', Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = 'pedidos'
    
   # STATUS_PEDIDO = (
   #     ('PENDENTE', 'PENDENTE'),
   #     ('CANCELADO', 'CANCELADO'),
   #     ('FINALIZADO', 'FINALIZADO'),
   # )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    status = Column('status', String)
    usuario = Column('usuario', ForeignKey('usuarios.id'))
    preco = Column('preco', Float)

    def __init__(self, usuario, status='PENDENTE', preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco

class ItemPedido(Base):
    __tablename__ = 'Itens_Pedido'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    preco_unitario = Column('preco_unitario', Float)
    quantidade = Column('quantidade', Integer)
    sabor = Column('sabor', String)
    tamanho = Column('tamanho', String)
    pedido = Column('pedido', ForeignKey('pedidos.id'))

    def __init__(self, pedido, preco_unitario, quantidade, sabor, tamanho):
        self.preco_unitario = preco_unitario
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.pedido = pedido
