from pydantic import BaseModel
from datetime import datetime

class ProdutoBase(BaseModel):
    nome: str
    quantidade_estoque: int

class ProdutoResponse(ProdutoBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True

class MovimentacaoCreate(BaseModel):
    quantidade: int

class MovimentacaoResponse(BaseModel):
    id: int
    produto_id: int
    usuario_id: int
    tipo: str
    quantidade: int
    data_hora: datetime

    class Config:
        from_attributes = True
