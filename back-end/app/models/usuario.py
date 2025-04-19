from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.models import Base, perfil  # Certifique-se de que o Base está sendo importado corretamente

class Usuario(Base):
    __tablename__ = "usuarios"
    matricula = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    primeiro_acesso = Column(Boolean, default=True)
    fk_perfil = Column(Integer, ForeignKey("perfis.id"), nullable=False)
