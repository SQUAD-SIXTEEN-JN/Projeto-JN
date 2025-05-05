from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class Perfil(Base):
    __tablename__ = "perfis"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)

    cursos = relationship("Curso", back_populates="perfil")