from fastapi import FastAPI
from database import engine, Base
from api import rotas_usuarios, rotas_estoque
from models.estoque import Produto
from sqlalchemy.orm import Session
from database import SessionLocal

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Almoxarifado API")

# Inclui os roteadores
app.include_router(rotas_usuarios.router)
app.include_router(rotas_estoque.router)

# Rota auxiliar para injetar um produto inicial e facilitar o teste prático
@app.post("/seed", tags=["Seed"])
def popular_banco_para_teste():
    db: Session = SessionLocal()
    produto_existente = db.query(Produto).filter(Produto.id == 1).first()
    if not produto_existente:
        produto_teste = Produto(nome="Desinfetante", quantidade_estoque=100)
        db.add(produto_teste)
        db.commit()
        return {"mensagem": "Produto de teste inserido (ID 1 com 100 unidades)."}
    return {"mensagem": "Produto de teste já existe."}
