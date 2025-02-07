from utils.session import session_manager
from utils.migration import atualizar_tabela
from database import get_session

class CrudBaseRepository:
    model = None  # Deve ser sobrescrito nas subclasses

    @classmethod
    def update_structure(cls):
        """Atualiza a estrutura da tabela."""
        try:
            atualizar_tabela(cls.model)
            print("Atualização da tabela concluída com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar a tabela: {e}")

    @classmethod
    @session_manager
    def insert(cls, data, session):
        """Insere um novo registro no banco de dados e retorna o(s) ID(s) inserido(s) ou uma mensagem de erro."""
        if not cls.model:
            return "Erro: Nenhum modelo foi definido para esta operação."

        try:
            if isinstance(data, list):
                if not all(isinstance(obj, dict) for obj in data):
                    return "Erro: Todos os itens devem ser dicionários."

                instances = [cls.model(**obj) for obj in data]
                session.add_all(instances)
                session.flush()  # Garante que os IDs sejam gerados antes do commit
                return [instance.id for instance in instances]  # Retorna os IDs inseridos

            elif isinstance(data, dict):
                instance = cls.model(**data)
                session.add(instance)
                session.flush()  # Garante que o ID seja gerado
                return instance.id  # Retorna o ID inserido

            return "Erro: O formato de entrada não é válido."

        except Exception as e:
            return f"Erro ao inserir: {e}"

    @classmethod
    @session_manager
    def update(cls, where, with_, session):
        """Atualiza registros com base em um critério e retorna True se bem-sucedido ou uma mensagem de erro."""
        if not cls.model:
            return "Erro: Nenhum modelo foi definido para esta operação."

        if not isinstance(where, dict) or not isinstance(with_, dict):
            return "Erro: Os critérios de atualização devem ser dicionários."

        try:
            result = session.query(cls.model).filter_by(**where).update(with_, synchronize_session=False)

            if result == 0:
                return "Nenhum registro encontrado para atualização."

            return True  # Atualização bem-sucedida

        except Exception as e:
            return f"Erro ao atualizar: {e}"

    @classmethod
    @session_manager
    def delete(cls, where, session):
        """Deleta registros com base em um critério e retorna True se for bem-sucedido ou uma mensagem de erro."""
        if not cls.model:
            return "Erro: Nenhum modelo foi definido para esta operação."

        try:
            result = session.query(cls.model).filter_by(**where).delete()

            if result == 0:
                return "Nenhum registro encontrado para exclusão."

            return True  # Indica que a exclusão foi bem-sucedida

        except Exception as e:
            return f"Erro ao excluir: {e}"

    @classmethod
    @session_manager
    def get_by_field(cls, session, where, fields=None):
        """Busca registros pelo campo especificado e retorna uma lista de dicionários ou uma mensagem de erro."""
        if not cls.model:
            return "Erro: Nenhum modelo foi definido para esta operação."

        if not isinstance(where, dict):
            return "Erro: O critério de busca deve ser um dicionário."

        try:
            query = session.query(cls.model).filter_by(**where)

            if fields:
                valid_fields = [field for field in fields if hasattr(cls.model, field)]
                if not valid_fields:
                    return []

                query = query.with_entities(*[getattr(cls.model, field) for field in valid_fields])
                return [dict(zip(valid_fields, obj)) for obj in query.all()]
            else:
                return [
                    {key: value for key, value in obj.__dict__.items() if key != "_sa_instance_state"}
                    for obj in query.all()
                ]
        except Exception as e:
            return f"Erro ao buscar registros: {e}"
