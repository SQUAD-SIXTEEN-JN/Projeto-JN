from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, REAL
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    matricula = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    primeiro_acesso = Column(Boolean, default=True)
    fk_perfil = Column(Integer, ForeignKey("perfis.id"), nullable=False)

    perfil = relationship("Perfil", back_populates="usuarios")
    progresso = relationship("Progressos", back_populates="usuario")
    

class Perfil(Base):
    __tablename__ = "perfis"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(Text)

    usuarios = relationship("Usuario", back_populates="perfil")
    permissoes = relationship("Permissoes", back_populates="perfil")

class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(30), nullable=False)
    descricao = Column(Text, nullable=False)
    rota = Column(Text, nullable=False)

    permissoes = relationship("Permissoes", back_populates="menu")

class Permissoes(Base):
    __tablename__ = "permissoes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fk_perfil = Column(Integer, ForeignKey("perfis.id"), nullable=False)
    fk_menu = Column(Integer, ForeignKey("menus.id"), nullable=False)

    perfil = relationship("Perfil", back_populates="permissoes")
    menu = relationship("Menu", back_populates="permissoes")

class Cursos(Base):
    __tablename__ = "cursos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)

    modulos = relationship("Modulos", back_populates="curso")
    progresso = relationship("Progressos", back_populates="curso")

class Modulos(Base):
    __tablename__ = "modulos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(40), nullable=False)
    ordem = Column(Integer, nullable=False)
    descricao = Column(Text)
    fk_curso = Column(Integer, ForeignKey("cursos.id"), nullable=False)

    curso = relationship("Cursos", back_populates="modulos")
    conteudos = relationship("Conteudo", back_populates="modulo")

class Progressos(Base):
    __tablename__ = "progressos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    progresso = Column(REAL, nullable=False)
    fk_usuario = Column(Integer, ForeignKey("usuarios.matricula"), nullable=False)
    fk_curso = Column(Integer, ForeignKey("cursos.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="progresso")
    curso = relationship("Cursos", back_populates="progresso")
    
class Conteudo(Base):
    __tablename__ = "conteudos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    ordem = Column(Integer, nullable=False)
    tipo = Column(String,nullable=False)
    url = Column(String, nullable=False)
    fk_modulo = Column(Integer, ForeignKey("modulos.id"), nullable=False)
    
    modulo = relationship("Modulos", back_populates="conteudos")
    