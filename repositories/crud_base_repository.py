from utils.session import session_manager
from utils.migration import atualizar_tabela
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, ProgrammingError, DatabaseError, SQLAlchemyError
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
    @session_manager(commit=True)  # Dá commit, pois altera dados
    def insert(cls, data, session):
        """Insere um novo registro no banco de dados e retorna um dicionário de resposta."""
        if not cls.model:
            return {"success": False, "error": "Erro: Nenhum modelo foi definido para esta operação."}

        try:
            if isinstance(data, list):
                if not all(isinstance(obj, dict) for obj in data):
                    return {"success": False, "error": "Erro: Todos os itens devem ser dicionários."}

                instances = [cls.model(**obj) for obj in data]
                session.add_all(instances)
                session.flush()  # Garante que os IDs sejam gerados antes do commit
                return {"success": True,
                        "data": [instance.id for instance in instances]}  # Retorna apenas a lista de IDs

            elif isinstance(data, dict):
                instance = cls.model(**data)
                session.add(instance)
                session.flush()  # Garante que o ID seja gerado
                return {"success": True, "data": instance.id}  # Retorna diretamente o ID

            return {"success": False, "error": "Erro: O formato de entrada não é válido."}

        except IntegrityError:
            session.rollback()
            return {"success": False, "error": "Erro: Violação de integridade. Registro duplicado ou dados inválidos."}


    @classmethod
    @session_manager(commit=True)  # Dá commit, pois altera dados
    def update(cls, where, with_, session):
        """Atualiza registros com base em um critério e retorna um dicionário indicando sucesso ou erro."""
        if not cls.model:
            return {"success": False, "error": "Erro: Nenhum modelo foi definido para esta operação."}

        if not isinstance(where, dict) or not isinstance(with_, dict):
            return {"success": False, "error": "Erro: Os critérios de atualização devem ser dicionários."}

        try:
            result = session.query(cls.model).filter_by(**where).update(with_, synchronize_session=False)
            if result == 0:
                return {"success": False, "error": "Nenhum registro encontrado para atualização."}

            return {"success": True}

        except Exception as e:
            return {"success": False, "error": f"Erro ao atualizar: {e}"}

    @classmethod
    @session_manager(commit=True)  # Dá commit, pois altera dados
    def delete(cls, where, session, ignore_if_not_found=False):
        """Deleta um ou mais registros com base em um critério e retorna um dicionário indicando sucesso ou erro.

        - Se `where` for um dicionário, exclui pelo critério de igualdade.
        - Se `where` for uma lista de filtros, aplica `filter` com múltiplas condições.
        """

        if not cls.model:
            return {"success": False, "error": "Erro: Nenhum modelo foi definido para esta operação."}

        try:
            # 🔹 Excluir um único registro se where for dicionário
            if isinstance(where, dict):
                query = session.query(cls.model).filter_by(**where)
            # 🔹 Excluir múltiplos registros se where for uma lista de expressões
            elif isinstance(where, list) and where:
                query = session.query(cls.model).filter(*where)
            else:
                return {"success": False,
                        "error": "Erro: O parâmetro 'where' deve ser um dicionário ou uma lista de filtros."}

            deleted_count = query.delete(synchronize_session=False)

            if deleted_count == 0 and not ignore_if_not_found:
                return {"success": False, "error": "Nenhum registro encontrado para exclusão."}

            return {"success": True, "deleted_count": deleted_count}

        except Exception as e:
            return {"success": False, "error": f"Erro ao excluir registros: {e}"}

    # @classmethod
    # @session_manager(commit=True)  # Dá commit, pois altera dados
    # def delete(cls, where, session, ignore_if_not_found=False):
    #     """Deleta registros com base em um critério e retorna um dicionário indicando sucesso ou erro."""
    #     if not cls.model:
    #         return {"success": False, "error": "Erro: Nenhum modelo foi definido para esta operação."}
    #
    #     try:
    #         result = session.query(cls.model).filter_by(
    #             **where).delete()  # 🔴 Limitação: `filter_by` apenas aceita igualdade exata!
    #
    #         if result == 0 and not ignore_if_not_found:
    #             return {"success": False, "error": "Nenhum registro encontrado para exclusão."}
    #
    #         return {"success": True}
    #
    #     except Exception as e:
    #         return {"success": False, "error": f"Erro ao excluir: {e}"}
    #
    # @classmethod
    # @session_manager(commit=True)
    # def delete_multi(cls, filters, session):
    #     """Deleta múltiplos registros com base em uma lista de filtros."""
    #     if not cls.model:
    #         return {"success": False, "error": "Erro: Nenhum modelo foi definido para esta operação."}
    #
    #     if not isinstance(filters, list) or not filters:
    #         return {"success": False, "error": "Erro: O parâmetro 'filters' deve ser uma lista não vazia."}
    #
    #     try:
    #         query = session.query(cls.model).filter(*filters)  # 🔹 Usa `filter` para mais flexibilidade
    #         deleted_count = query.delete(synchronize_session=False)
    #
    #         if deleted_count == 0:
    #             return {"success": False, "error": "Nenhum registro encontrado para exclusão."}
    #
    #         return {"success": True, "deleted_count": deleted_count}
    #
    #     except Exception as e:
    #         return {"success": False, "error": f"Erro ao excluir múltiplos registros: {e}"}


    @classmethod
    @session_manager(commit=False)  # Não dá commit, pois não altera dados
    def select(cls, session, where=None, fields=None, order_by=None, limit=None, offset=None, filters=None):
        """Busca registros e retorna um dicionário contendo os dados ou um erro."""
        if not cls.model:
            return {"success": False, "error": "Erro: Nenhum modelo definido."}

        query = session.query(cls.model)

        if where and isinstance(where, dict):
            query = query.filter_by(**where)

        if filters and isinstance(filters, list):
            query = query.filter(and_(*filters))

        if fields:
            valid_fields = [getattr(cls.model, field) for field in fields if hasattr(cls.model, field)]
            if valid_fields:
                query = query.with_entities(*valid_fields)

        if order_by:
            order_criteria = []
            for field in order_by:
                field_name, *direction = field.split()
                if hasattr(cls.model, field_name):
                    column = getattr(cls.model, field_name)
                    order_criteria.append(column.desc() if "desc" in direction else column.asc())
            if order_criteria:
                query = query.order_by(*order_criteria)

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        results = query.all()
        return {"success": True, "data": results}
