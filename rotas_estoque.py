from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.estoque import Produto, Movimentacao, TipoMovimentacao
from models.usuario import Usuario
from schemas.estoque_schema import ProdutoResponse, MovimentacaoCreate, MovimentacaoResponse
from core.security import verificar_acesso_basico

router = APIRouter(prefix="/estoque", tags=["Estoque"])

@router.get("/produtos", response_model=List[ProdutoResponse])
def listar_produtos(
    skip: int = 0,
    limit: int = 10,
    nome: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(verificar_acesso_basico)
):
    query = db.query(Produto)
    if nome:
        query = query.filter(Produto.nome.ilike(f"%{nome}%"))
    return query.offset(skip).limit(limit).all()

@router.post("/produtos/{produto_id}/saida", response_model=MovimentacaoResponse)
def registrar_saida(
    produto_id: int,
    movimentacao: MovimentacaoCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(verificar_acesso_basico)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    if movimentacao.quantidade > produto.quantidade_estoque:
        mensagem_erro = f"Saída não permitida: estoque insuficiente. Disponível: {produto.quantidade_estoque}. Solicitado: {movimentacao.quantidade}."
        raise HTTPException(status_code=400, detail=mensagem_erro)

    produto.quantidade_estoque -= movimentacao.quantidade

    nova_movimentacao = Movimentacao(
        produto_id=produto.id,
        usuario_id=usuario_logado.id,
        tipo=TipoMovimentacao.SAIDA,
        quantidade=movimentacao.quantidade
    )

    db.add(nova_movimentacao)
    db.commit()
    db.refresh(nova_movimentacao)

    return nova_movimentacao
