from utils.session import session_manager
from utils.migration import atualizar_tabela
from database import get_session
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, ProgrammingError, DatabaseError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

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
                return [instance.id]  # Retorna o ID inserido

            return "Erro: O formato de entrada não é válido."

        except IntegrityError as e:
            session.rollback()
            return "Erro: Violação de integridade. Registro duplicado ou dados inválidos."

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
    def delete(cls, where, session, ignore_if_not_found=False):
        """Deleta registros com base em um critério e retorna True se for bem-sucedido ou uma mensagem de erro."""
        if not cls.model:
            return "Erro: Nenhum modelo foi definido para esta operação."

        try:
            result = session.query(cls.model).filter_by(**where).delete()

            if result == 0:
                if not ignore_if_not_found:
                    return "Nenhum registro encontrado para exclusão."

            return True  # Indica que a exclusão foi bem-sucedida

        except Exception as e:
            return f"Erro ao excluir: {e}"

    @classmethod
    @session_manager
    def obtain(cls, session, where=None, fields=None, order_by=None, limit=None, offset=None, filters=None):
        """Busca registros com opções mais flexíveis.

        Parâmetros:
        - `where` (dict): Condições de igualdade (ex.: {"name": "John"}).
        - `fields` (list): Lista de colunas a serem retornadas (ex.: ["id", "name"]).
        - `order_by` (list): Lista de colunas para ordenar (ex.: ["name desc"]).
        - `limit` (int): Número máximo de registros a retornar.
        - `offset` (int): Número de registros a pular (paginação).
        - `filters` (list): Lista de expressões SQLAlchemy para filtros mais avançados.

        Retorna:
        - Lista de dicionários com os registros encontrados.
        """
        if not cls.model:
            return "Erro: Nenhum modelo definido."

        query = session.query(cls.model)

        # Aplicar filtros simples de igualdade
        if where and isinstance(where, dict):
            query = query.filter_by(**where)

        # Aplicar filtros personalizados (ex.: LIKE, >, <, IN)
        if filters and isinstance(filters, list):
            query = query.filter(and_(*filters))  # Combina múltiplas condições com AND

        # Selecionar campos específicos
        if fields:
            valid_fields = [getattr(cls.model, field) for field in fields if hasattr(cls.model, field)]
            if valid_fields:
                query = query.with_entities(*valid_fields)

        # Aplicar ordenação
        if order_by:
            order_criteria = []
            for field in order_by:
                field_name, *direction = field.split()
                if hasattr(cls.model, field_name):
                    column = getattr(cls.model, field_name)
                    order_criteria.append(column.desc() if "desc" in direction else column.asc())
            if order_criteria:
                query = query.order_by(*order_criteria)

        # Aplicar paginação
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        # Executar consulta e converter resultados para dicionário
        results = query.all()
        return [dict(zip(fields, obj)) for obj in results] if fields else [
            {key: value for key, value in obj.__dict__.items() if key != "_sa_instance_state"} for obj in results
        ]
