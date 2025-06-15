from typing import List, Dict
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.models import Usuario, Perfil, Progressos
from app.schemas.usuario import UsuarioUpdate


async def get_usuario_obj(db: Session, matricula: int) -> Usuario:
    """
    Busca um usuário pela matrícula e retorna o objeto Usuario.
    """
    usuario = db.query(Usuario).options(joinedload(Usuario.perfil)).filter(
        Usuario.matricula == matricula
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario


async def get_usuario(db: Session, matricula: int) -> Dict:
    """
    Busca um usuário formatado para detalhamento conforme exemplo fornecido.
    """
    usuario = await get_usuario_obj(db, matricula)
   
    usuario_dict = {
        "nome": usuario.nome,
        "matricula": usuario.matricula,
        "perfil": usuario.perfil.nome if usuario.perfil else "Sem perfil"
    }
   
    return usuario_dict


async def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> List[Dict]:
    """
    Busca usuários formatados para listagem
    """
    usuarios = db.query(Usuario).options(joinedload(Usuario.perfil)).offset(skip).limit(limit).all()
    
    usuarios_formatados = []
    for usuario in usuarios:
        usuario_dict = {
            "nome": usuario.nome,
            "matricula": usuario.matricula,
            "perfil": usuario.perfil.nome if usuario.perfil else "Sem perfil"
        }
        usuarios_formatados.append(usuario_dict)
    
    return usuarios_formatados


async def update_usuario(db: Session, matricula: int, usuario_data: UsuarioUpdate) -> Usuario:
    """
    Atualiza um usuário existente.
    """
    usuario = await get_usuario_obj(db, matricula)
    
    # Se está tentando atualizar o perfil, busca pelo nome e valida se existe
    if usuario_data.perfil is not None:
        perfil = db.query(Perfil).filter(Perfil.nome == usuario_data.perfil).first()
        if not perfil:
            raise HTTPException(status_code=400, detail="Perfil não existe")
        setattr(usuario, "fk_perfil", perfil.id)
    
    # Atualiza apenas os campos fornecidos (exceto perfil que já foi tratado)
    update_data = usuario_data.dict(exclude_unset=True, exclude={"perfil"})
    for key, value in update_data.items():
        setattr(usuario, key, value)
    
    db.commit()
    db.refresh(usuario)
    
    return usuario


async def delete_usuario(db: Session, matricula: int) -> Dict[str, bool]:
    """
    Remove um usuário do banco de dados.
    """
    usuario = await get_usuario_obj(db, matricula)
    
    # Remove todos os progressos associados a este usuário
    db.query(Progressos).filter(Progressos.fk_usuario == matricula).delete()
    
    db.delete(usuario)
    db.commit()
    
    return {"success": True}