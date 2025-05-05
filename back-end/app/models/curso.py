from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Curso(Base):
    __tablename__ = "cursos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=True)
    fk_perfil = Column(Integer, ForeignKey("perfis.id"), nullable=False)

    perfil = relationship("Perfil", back_populates="cursos")