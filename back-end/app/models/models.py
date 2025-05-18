from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    matricula = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    primeiro_acesso = Column(Boolean, default=True)
    fk_perfil = Column(Integer, ForeignKey("perfis.id"), nullable=False)

class Perfil(Base):
    __tablename__ = "perfis"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(Text)

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
