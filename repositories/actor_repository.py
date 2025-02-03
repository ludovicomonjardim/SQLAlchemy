from utils.session import session_manager
from utils.migration import atualizar_tabela
from models.actor import Actor
from models.movie_actor import MovieActor
import logging

class ActorRepository:

    @staticmethod
    def update_structure():
        """Atualiza a estrutura da tabela 'actors'."""
        try:
            atualizar_tabela(Actor)
            print("Atualização da tabela 'actors' concluída com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar a tabela 'actors': {e}")

    @staticmethod
    @session_manager
    def insert(data, session):
        """Insere um novo ator no banco de dados."""
        try:
            if isinstance(data, list):
                existing_names = {a.name for a in session.query(Actor).all()}
                actors = [Actor(**actor_data) for actor_data in data if actor_data["name"] not in existing_names]
                session.add_all(actors)
                session.commit()
                print(f"{len(actors)} atores inseridos com sucesso!")
                return len(actors)
            else:
                # Evitar duplicatas
                if session.query(Actor).filter_by(name=data["name"]).first():
                    print(f"Ator '{data['name']}' já existe. Inserção ignorada.")
                    return 0
                actor = Actor(**data)
                session.add(actor)
                session.commit()
                print(f"Ator '{actor.name}' inserido com sucesso!")
                return 1
        except Exception as e:
            session.rollback()
            print(f"Erro ao inserir ator(es): {e}")
            return 0

    @staticmethod
    @session_manager
    def update(where, with_, session):
        """Atualiza informações de um ator."""
        try:
            result = session.query(Actor).filter_by(**where).update(with_, synchronize_session=False)
            session.commit()
            print(f"{result} ator(es) atualizado(s) com sucesso.")
            return result
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar ator: {e}")
            return 0

    @staticmethod
    @session_manager
    def delete(where, session):
        """Remove um ator do banco, garantindo que todas as referências sejam apagadas antes."""
        try:
            query = session.query(Actor).filter_by(**where)
            actor = query.first()
            if not actor:
                print("Nenhum ator encontrado para deleção.")
                return 0

            # ✅ Remove relações antes de excluir o ator
            session.query(MovieActor).filter_by(actor_id=actor.id).delete(synchronize_session=False)
            session.commit()

            # ✅ Agora pode excluir o ator
            result = query.delete(synchronize_session=False)
            session.commit()

            # ✅ Buscar o ator de novo antes de imprimir seu nome
            deleted_actor = session.query(Actor).filter_by(**where).first()
            if deleted_actor is None:
                print(f"Ator deletado com sucesso! {result} registro(s) removido(s).")
                return result

            return 0
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao deletar ator: {e}", exc_info=True)
            return 0

    @staticmethod
    @session_manager
    def get_by_field(session, where, fields=None):
        """Busca um ator por um campo específico."""
        try:
            query = session.query(Actor).filter_by(**where)

            if fields:
                valid_fields = [field for field in fields if hasattr(Actor, field)]
                query = query.with_entities(*[getattr(Actor, field) for field in valid_fields])
                actors = query.all()
                return [dict(zip(valid_fields, actor)) for actor in actors]
            else:
                actors = query.all()
                return [
                    {key: value for key, value in actor.__dict__.items() if key != "_sa_instance_state"}
                    for actor in actors
                ]
        except Exception as e:
            logger.error(f"Erro ao buscar atores: {e}", exc_info=True)
            return []

    @staticmethod
    @session_manager
    def get_by_name(name, session):
        """Busca um ator pelo nome."""
        actor = session.query(Actor).filter(Actor.name == name).first()
        if actor:
            session.expunge(actor)
        return actor

    @staticmethod
    @session_manager
    def print_all(session):
        """Exibe todos os atores cadastrados."""
        actors = session.query(Actor).all()
        if actors:
            print()
            print("-" * 51)
            print(f"{'ID':<5} {'Nome':<45}")
            print("-" * 51)
            for actor in actors:
                print(f"{actor.id:<5} {actor.name:<45}")
        else:
            print("Nenhum ator encontrado na tabela.")


# Configuração do Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
