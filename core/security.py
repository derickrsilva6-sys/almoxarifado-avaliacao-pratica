from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.usuario import Usuario, TipoUsuario
from database import get_db

# Simulação simples de esquema OAuth2 para a prova
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Função simulada para validação de token e resgate de usuário
def get_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Em um cenário real, aqui entraria a decodificação JWT.
    # Para a prova, vamos simular que o token seja o próprio username para facilitar os testes
    usuario = db.query(Usuario).filter(Usuario.username == token).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario

def verificar_admin(usuario_atual: Usuario = Depends(get_usuario_atual)):
    if usuario_atual.tipo != TipoUsuario.ADMINISTRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operação não permitida. Privilégios de Administrador requeridos."
        )
    return usuario_atual

def verificar_acesso_basico(usuario_atual: Usuario = Depends(get_usuario_atual)):
    return usuario_atual
