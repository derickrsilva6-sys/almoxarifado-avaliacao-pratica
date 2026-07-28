import enum
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base

class TipoMovimentacao(str, enum.Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    quantidade_estoque = Column(Integer, default=0)
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    tipo = Column(Enum(TipoMovimentacao))
    quantidade = Column(Integer)
    data_hora = Column(DateTime, default=datetime.datetime.utcnow)

    produto = relationship("Produto")
    usuario = relationship("Usuario")
