from utils.session import session_manager
from utils.migration import atualizar_tabela
from models.actor import Actor

import logging


class ActorRepository:

    @staticmethod
    def update_structure():
        try:
            atualizar_tabela(Actor)
            print("Atualização da tabela 'actors' concluída com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar a tabela 'actors': {e}")

    @staticmethod
    @session_manager
    def insert(data, session):
        try:
            if isinstance(data, list):
                actors = [Actor(**actor_data) for actor_data in data]
                session.add_all(actors)  # Troca de bulk_save_objects() por add_all() para validações
                print(f"{len(actors)} atores inseridos com sucesso!")
            else:
                actor = Actor(**data)
                session.add(actor)
                print(f"Ator '{actor.name}' inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir ator(es): {e}")
            return False

    @staticmethod
    @session_manager
    def update(where, with_, session):
        try:
            result = session.query(Actor).filter_by(**where).update(with_, synchronize_session=False)
            print(f"{result} ator(es) atualizado(s) com sucesso.")
            return result
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar ator: {e}")
            return 0

    @staticmethod
    @session_manager
    def delete(where, session):
        try:
            query = session.query(Actor).filter_by(**where)
            count = query.count()  # Verifica quantos registros serão afetados
            if count == 0:
                print("Nenhum ator encontrado para deleção.")
                return 0

            result = query.delete()
            print(f"Ator deletado com sucesso! {result} registro(s) removido(s).")
            return result
        except Exception as e:
            logger.error(f"Erro ao deletar ator: {e}", exc_info=True)
            return 0

    @staticmethod
    @session_manager
    def get_by_field(session, where, fields=None):
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
        actor = session.query(Actor).filter(Actor.name == name).first()
        if actor:
            session.expunge(actor)
        return actor

    @staticmethod
    @session_manager
    def print_all(session):
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
