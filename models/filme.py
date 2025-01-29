from models.base import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates

# Modelo da tabela "filmes"
class Filme(Base):
    __tablename__ = "filmes"

    titulo = Column(String, primary_key=True)
    genero = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Filme(titulo='{self.titulo}', genero='{self.genero}', ano={self.ano})"

    """
    Utilizando:
    Validação com @validates.
    - para validação automática na atribuição de valores
    
    Também há:
    Validação dentro do __init__ do Modelo.
    - para evitar valores inválidos logo na criação do objeto
    Validação no session.commit() usando before_flush.
    - para impedir valores inválidos apenas no momento do commit()
    """

    @validates("ano")
    def valida_ano(self, key, value):
        """Valida se o ano está dentro de um intervalo permitido"""
        if not (1800 <= value <= 2100):
            raise ValueError(f"O ano {value} não é válido. Deve estar entre 1800 e 2100.")
        return value

    @validates("genero")
    def valida_genero(self, key, value):
        """Valida se o gênero está na lista permitida"""
        generos_permitidos = {"Ação", "Drama", "Ficção", "Fantasia", "Comédia"}
        if value not in generos_permitidos:
            raise ValueError(f"Gênero '{value}' inválido. Escolha entre {generos_permitidos}")
        return value