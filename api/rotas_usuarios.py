from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from core.security import verificar_admin, verificar_acesso_basico

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    novo_usuario = Usuario(
        nome=usuario.nome,
        username=usuario.username,
        senha_hash=usuario.senha, # Em produção, use hash aqui (ex: passlib)
        tipo=usuario.tipo
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

#Ajustes feito
@router.get("/", response_model = list[UsuarioResponse])
def Listar_usuarios(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(verificar_acesso_basico)
):
    usuarios = db.query(Usuario).all()
    return usuarios

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(
    usuario_id: int,
    usuario_atualizado: UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(verificar_acesso_basico)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).fister()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    usuario.nome = usuario_atualizado.nome
    usuario.username = usuario_atualizado.username
    usuario.senha_hash = usuario_atualizado.senha
    usuario.tipo = usuario_atualizado.tipo
    
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(verificar_admin)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(usuario)
    db.commit()
    return None