"""
repositories/crud_base_repository.py
Este módulo contém a classe CrudBaseRepository, responsável por operações genéricas de CRUD no banco de dados.
"""
from utils.session import session_manager
from utils.migration import atualizar_tabela
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, ProgrammingError, DatabaseError, SQLAlchemyError
from sqlalchemy import and_, or_

class CrudBaseRepository:
    """
    Classe base para repositórios CRUD (Create, Read, Update, Delete).
    Define métodos genéricos que podem ser reutilizados por subclasses específicas.
    """
    model = None  # Deve ser sobrescrito nas subclasses

    @classmethod
    def update_structure(cls):
        """
        Atualiza a estrutura da tabela no banco de dados.
        - Utiliza a função `atualizar_tabela` para aplicar alterações no esquema da tabela.
        - Captura e trata qualquer exceção que ocorra durante o processo.
        """
        try:
            atualizar_tabela(cls.model)
            print("Atualização da tabela concluída com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar a tabela: {e}")

    @classmethod
    @session_manager(commit=True)  # Dá commit, pois altera dados
    def insert(cls, data, session):
        """
        Insere um ou mais registros no banco de dados.
        - Aceita tanto um dicionário quanto uma lista de dicionários como entrada.
        - Retorna um dicionário com informações sobre o resultado da operação.
        """

        # Verifica se o modelo foi definido.
        if not cls.model:
            return {"success": False, "error": "Erro: Nenhum modelo foi definido para esta operação."}

        try:
            if isinstance(data, list): # Verifica se a entrada é uma lista.

                # Garante que todos os itens são dicionários.
                if not all(isinstance(obj, dict) for obj in data):
                    return {"success": False, "error": "Erro: Todos os itens devem ser dicionários."}

                instances = [cls.model(**obj) for obj in data]  # Cria instâncias do modelo a partir dos dados.
                session.add_all(instances)  # Adiciona todas as instâncias à sessão.
                session.flush()  # Garante que os IDs sejam gerados antes do commit.
                return {"success": True,
                        "data": [instance.id for instance in instances]}  # Retorna apenas a lista de IDs

            elif isinstance(data, dict): # Verifica se a entrada é um dicionário.
                instance = cls.model(**data)  # Cria uma instância do modelo a partir dos dados.
                session.add(instance)  # Adiciona a instância à sessão
                session.flush()  # Garante que o ID seja gerado
                return {"success": True, "data": instance.id}  # Retorna diretamente o ID

            return {"success": False, "error": "Erro: O formato de entrada não é válido."}

        except IntegrityError:
            # Desfaz as alterações na sessão.
            session.rollback()
            return {"success": False, "error": "Erro: Violação de integridade. Registro duplicado ou dados inválidos."}

    @classmethod
    @session_manager(commit=True)  # Dá commit, pois altera dados
    def update(cls, where, with_, session):
        """
        Atualiza registros no banco de dados com base em um critério.
        - `where` define os critérios de seleção dos registros.
        - `with_` define os novos valores para os campos.
        - Retorna um dicionário indicando sucesso ou erro.
        """

        if not cls.model:
            return {"success": False, "error": "Erro: Nenhum modelo foi definido para esta operação."}

        if not isinstance(where, dict) or not isinstance(with_, dict):
            return {"success": False, "error": "Erro: Os critérios de atualização devem ser dicionários."}

        try:
            result = session.query(cls.model).filter_by(**where).update(with_, synchronize_session=False)

            if result == 0:
                return {"success": False,
                        "error": "Nenhum registro encontrado para atualização."}  # 🔹 Retorna erro se nenhum registro for atualizado

            return {"success": True}

        except Exception as e:
            session.rollback()
            return {"success": False, "error": f"Erro ao atualizar: {e}"}


    # @classmethod
    # @session_manager(commit=True)  # Dá commit, pois altera dados
    # def update(cls, where, with_, session):
    #     """
    #     Atualiza registros no banco de dados com base em um critério.
    #     - `where` define os critérios de seleção dos registros.
    #     - `with_` define os novos valores para os campos.
    #     - Retorna um dicionário indicando sucesso ou erro.
    #     """
    #
    #     # Verifica se o modelo foi definido.
    #     if not cls.model:
    #         return {"success": False, "error": "Erro: Nenhum modelo foi definido para esta operação."}
    #
    #     # Valida os tipos de entrada.
    #     if not isinstance(where, dict) or not isinstance(with_, dict):
    #         return {"success": False, "error": "Erro: Os critérios de atualização devem ser dicionários."}
    #
    #     try:
    #         # Atualiza os registros.
    #         result = session.query(cls.model).filter_by(**where).update(with_, synchronize_session=False)
    #         # Verifica se algum registro foi encontrado.
    #         if result == 0:
    #             return {"success": False, "error": "Nenhum registro encontrado para atualização."}
    #
    #         # Indica sucesso na operação
    #         return {"success": True}
    #
    #     except Exception as e:
    #         return {"success": False, "error": f"Erro ao atualizar: {e}"}

    @classmethod
    @session_manager(commit=True)  # Dá commit, pois altera dados
    def delete(cls, where, session, ignore_if_not_found=False):
        """
        Exclui um ou mais registros no banco de dados com base em um critério.
        - `where` pode ser um dicionário (para exclusão simples) ou uma lista de filtros (para exclusão complexa).
        - Retorna um dicionário indicando sucesso ou erro.
        """

        # Verifica se o modelo foi definido.
        if not cls.model:
            return {"success": False, "error": "Erro: Nenhum modelo foi definido para esta operação."}

        try:
            if isinstance(where, dict):
                # 🔹 Excluir um único registro se where for dicionário
                query = session.query(cls.model).filter_by(**where)
            elif isinstance(where, list) and where:
                # 🔹 Excluir múltiplos registros se where for uma lista de expressões
                query = session.query(cls.model).filter(*where)
            else:
                return {"success": False,
                        "error": "Erro: O parâmetro 'where' deve ser um dicionário ou uma lista de filtros."}

            # Executa a exclusão
            deleted_count = query.delete(synchronize_session=False)

            # Verifica se nenhum registro foi excluído
            if deleted_count == 0 and not ignore_if_not_found:
                return {"success": False, "error": "Nenhum registro encontrado para exclusão."}

            # Retorna a quantidade de registros excluídos
            return {"success": True, "deleted_count": deleted_count}

        except Exception as e:
            return {"success": False, "error": f"Erro ao excluir registros: {e}"}

    @classmethod
    @session_manager(commit=False)  # Não dá commit, pois não altera dados
    def select(cls, session, where=None, fields=None, order_by=None, limit=None, offset=None, filters=None):
        """
        Busca registros no banco de dados com base em critérios opcionais.
        - `where`: Filtra registros com base em condições de igualdade.
        - `fields`: Especifica os campos a serem retornados.
        - `order_by`: Define a ordem dos resultados.
        - `limit`: Limita o número de resultados.
        - `offset`: Define o deslocamento inicial.
        - `filters`: Aplica filtros complexos usando operadores lógicos.
        - Retorna um dicionário contendo os dados ou um erro.
        """

        # Verifica se o modelo foi definido.
        if not cls.model:
            return {"success": False, "error": "Erro: Nenhum modelo definido."}

        # Inicializa a consulta.
        query = session.query(cls.model)

        # Aplica filtros de igualdade.
        if where and isinstance(where, dict):
            query = query.filter_by(**where)

        # Aplica filtros complexos.
        if filters and isinstance(filters, list):
            query = query.filter(and_(*filters))

        # Seleciona campos específicos.
        if fields:
            valid_fields = [getattr(cls.model, field) for field in fields if hasattr(cls.model, field)]
            if valid_fields:
                query = query.with_entities(*valid_fields)

        # Define a ordenação.
        if order_by:
            order_criteria = []
            for field in order_by:
                field_name, *direction = field.split()
                if hasattr(cls.model, field_name):
                    column = getattr(cls.model, field_name)
                    order_criteria.append(column.desc() if "desc" in direction else column.asc())
            if order_criteria:
                query = query.order_by(*order_criteria)

        # Limita o número de resultados.
        if limit:
            query = query.limit(limit)

        # Define o deslocamento inicial.
        if offset:
            query = query.offset(offset)

        # Executa a consulta e obtém os resultados.
        results = query.all()

        # Retorna os resultados.
        return {"success": True, "data": results}
