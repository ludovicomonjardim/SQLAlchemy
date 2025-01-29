# from sqlalchemy.exc import SQLAlchemyError
# from database import Database
from models.filme import Filme
from utils.session import session_manager
import logging


class FilmeRepository:

    @staticmethod
    @session_manager
    def insert(data, session):
        """Insere um ou vários filmes no banco."""
        try:
            if isinstance(data, list):  # 🔥 Se for uma lista, insere múltiplos registros
                filmes = [Filme(**filme_data) for filme_data in data]
                session.bulk_save_objects(filmes)
                print(f"{len(filmes)} filmes inseridos com sucesso!")
            else:  # 🔥 Se for um único dicionário, insere um filme
                filme = Filme(**data)
                session.add(filme)
                print(f"Filme '{filme.titulo}' inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir filme(s): {e}")
            return False

    @staticmethod
    @session_manager
    def update(where, with_, session):
        """Atualiza registros com base no filtro `where` e nos valores `with_`.

        Args:
            where (dict): Condições para localizar os registros a serem atualizados. Exemplo: {"titulo": "Matrix"}
            with_ (dict): Novos valores a serem atribuídos aos registros encontrados. Exemplo: {"ano": 2001}
            session (Session): Sessão ativa do SQLAlchemy.

        Returns:
            int: Número de registros modificados.
        """
        try:
            filmes = session.query(Filme).filter_by(**where).all()  # Buscar os registros antes de atualizar

            if not filmes:
                print("Nenhum filme encontrado para atualização.")
                return 0

            count = 0
            for filme in filmes:
                for key, value in with_.items():
                    if hasattr(filme, key):  # Garantir que o campo existe no modelo
                        setattr(filme, key, value)
                    else:
                        print(f"Aviso: O campo '{key}' não existe no modelo Filme e foi ignorado.")
                count += 1

            print(f"{count} filme(s) atualizado(s) com sucesso.")
            return count

        except Exception as e:
            print(f"Erro ao atualizar filme: {e}")
            return 0

    @staticmethod
    @session_manager
    def delete(where, session):
        """Deleta registros com base no filtro `where`."""
        try:
            result = session.query(Filme).filter_by(**where).delete()
            if result:
                print(f"Filme deletado com sucesso! {result} registro(s) removido(s).")
            else:
                print("Nenhum filme encontrado para deleção.")
            return result
        except Exception as e:
            print(f"Erro ao deletar filme: {e}")
            return 0

    @staticmethod
    @session_manager
    def get_by_field(session, where, fields=None):
        """Busca filmes com base nos critérios `where` e retorna os campos especificados (`fields`).

        Args:
            session (Session): Sessão do banco de dados.
            where (dict): Critérios de filtro (ex.: {"ano": 1999, "genero": "Ficção"}).
            fields (list, optional): Lista de colunas a serem retornadas (ex.: ["titulo", "ano"]).
                                     Retorna todos os campos se `None`.

        Returns:
            list: Lista de dicionários contendo os filmes encontrados.
        """
        try:
            query = session.query(Filme)

            # Aplicar filtro (where)
            query = query.filter_by(**where)

            # Aplicar seleção de colunas (fields)
            if fields:
                query = query.with_entities(*[getattr(Filme, field) for field in fields])
                filmes = query.all()
                return [dict(zip(fields, filme)) for filme in filmes]
            else:
                filmes = query.all()
                return [
                    {key: value for key, value in filme.__dict__.items() if key != "_sa_instance_state"}
                    for filme in filmes
                ]  # 🔥 Remove `_sa_instance_state` antes de retornar

        except Exception as e:
            print(f"Erro ao buscar filmes: {e}")
            return []

    @staticmethod
    @session_manager
    def get_by_titulo(titulo, session):
        """Busca um filme pelo título e retorna uma cópia desconectada."""
        filme = session.query(Filme).filter(Filme.titulo == titulo).first()
        if filme:
            session.expunge(filme)  # 🔥 Remove a ligação do objeto com a sessão
        return filme

    @staticmethod
    @session_manager
    def print_all(session):
        """Imprime todos os filmes da tabela."""
        filmes = session.query(Filme).all()
        if filmes:
            print()
            print("-" * 51)
            print(f"{'Título':<30} {'Gênero':<15} {'Ano':<5}")
            print("-" * 51)
            for filme in filmes:
                print(f"{filme.titulo:<30} {filme.genero:<15} {filme.ano:<5}")
        else:
            print("Nenhum filme encontrado na tabela.")


logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

@staticmethod
@session_manager
def insert(data, session):
    try:
        if isinstance(data, list):
            filmes = [Filme(**filme_data) for filme_data in data]
            session.bulk_save_objects(filmes)
            print(f"{len(filmes)} filmes inseridos com sucesso!")
        else:
            filme = Filme(**data)
            session.add(filme)
            print(f"Filme '{filme.titulo}' inserido com sucesso!")
        return True
    except Exception as e:
        logging.error(f"Erro ao inserir filme(s): {e}")
        return False