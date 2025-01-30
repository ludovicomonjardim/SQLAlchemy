def listar_atributos(model):
    """Retorna um dicionário com os atributos (colunas) do modelo e seus respectivos tipos."""
    return {col.name: str(col.type) for col in model.__table__.columns}
