from models.filme import Filme
from utils.session import session_manager
from utils.migration import atualizar_tabela
import logging


class FilmeRepository:
    """
    Repositório responsável pelas operações de banco de dados para a entidade Filme.

    Métodos incluem inserção, atualização, deleção e busca de registros na tabela 'filmes'.
    """

    @staticmethod
    def atualiza():
        """
        Atualiza a estrutura da tabela 'filmes', garantindo que a estrutura seja substituída corretamente.

        Este método verifica a estrutura atual da tabela e adiciona colunas ausentes conforme o modelo definido.
        """
        try:
            atualizar_tabela(Filme)
            print("Atualização da tabela 'filmes' concluída com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar a tabela 'filmes': {e}")

    @staticmethod
    @session_manager
    def insert(data, session):
        """
        Insere um ou vários filmes no banco de dados.

        Args:
            data (dict | list[dict]): Um dicionário representando um filme ou uma lista de dicionários para inserção em massa.
            session (Session): Sessão ativa do SQLAlchemy.

        Returns:
            bool: True se a inserção for bem-sucedida, False caso contrário.
        """
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
            print(f"Erro ao inserir filme(s): {e}")
            return False

    @staticmethod
    @session_manager
    def update(where, with_, session):
        """
        Atualiza registros na tabela 'filmes' com base nos critérios fornecidos.

        Args:
            where (dict): Condições para localizar os registros a serem atualizados (exemplo: {"titulo": "Matrix"}).
            with_ (dict): Valores a serem atribuídos aos registros encontrados (exemplo: {"ano": 2001}).
            session (Session): Sessão ativa do SQLAlchemy.

        Returns:
            int: Número de registros modificados.
        """
        try:
            filmes = session.query(Filme).filter_by(**where).all()
            if not filmes:
                print("Nenhum filme encontrado para atualização.")
                return 0

            count = 0
            for filme in filmes:
                for key, value in with_.items():
                    if hasattr(filme, key):
                        if getattr(filme, key) != value:  # Atualiza apenas se for diferente
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
        """
        Remove registros da tabela 'filmes' com base nos critérios fornecidos.

        Args:
            where (dict): Condições para localizar os registros a serem deletados (exemplo: {"titulo": "Matrix"}).
            session (Session): Sessão ativa do SQLAlchemy.

        Returns:
            int: Número de registros removidos.
        """
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
        """
        Busca filmes com base nos critérios especificados e retorna os campos solicitados.

        Args:
            session (Session): Sessão ativa do SQLAlchemy.
            where (dict): Critérios de filtro para a consulta (exemplo: {"ano": 1999, "genero": "Ficção"}).
            fields (list[str], opcional): Lista de colunas a serem retornadas (exemplo: ["titulo", "ano"]).
                                          Se None, retorna todos os campos.

        Returns:
            list[dict]: Lista de dicionários representando os filmes encontrados.
        """
        try:
            query = session.query(Filme).filter_by(**where)

            if fields:
                query = query.with_entities(*[getattr(Filme, field) for field in fields])
                filmes = query.all()
                return [dict(zip(fields, filme)) for filme in filmes]
            else:
                filmes = query.all()
                return [
                    {key: value for key, value in filme.__dict__.items() if key != "_sa_instance_state"}
                    for filme in filmes
                ]  # Remove `_sa_instance_state` antes de retornar
        except Exception as e:
            print(f"Erro ao buscar filmes: {e}")
            return []

    @staticmethod
    @session_manager
    def get_by_titulo(titulo, session):
        """
        Busca um filme pelo título.

        Args:
            titulo (str): Nome do filme a ser buscado.
            session (Session): Sessão ativa do SQLAlchemy.

        Returns:
            Filme | None: O objeto Filme encontrado ou None se não existir.
        """
        filme = session.query(Filme).filter(Filme.titulo == titulo).first()
        if filme:
            session.expunge(filme)  # Remove a ligação do objeto com a sessão para evitar efeitos colaterais
        return filme

    @staticmethod
    @session_manager
    def print_all(session):
        """
        Imprime todos os filmes da tabela 'filmes' em formato tabular.

        Args:
            session (Session): Sessão ativa do SQLAlchemy.
        """
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


# Configuração do logging para capturar erros
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
