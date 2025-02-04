from utils.session import session_manager

class CrudBaseRepository:
    model = None  # Deve ser sobrescrito nas subclasses

    @staticmethod
    @session_manager
    def insert(data, session):
        try:
            if isinstance(data, list):
                if not all(isinstance(obj, dict) for obj in data):
                    print(
                        "Erro: A lista contém elementos que não são dicionários. Certifique-se de que todos os itens são dicionários contendo os dados corretos.")
                    return False

                print(f"Iniciando a inserção de {len(data)} registros no banco de dados...")

                instances = []
                for obj in data:
                    try:
                        instance = CrudBaseRepository.model(**obj)
                        instances.append(instance)
                    except Exception as e:
                        print(
                            f"Erro ao criar uma instância do modelo {CrudBaseRepository.model.__name__} com os dados {obj}: {e}")
                        return False

                session.add_all(instances)
                print(f"{len(instances)} registros foram adicionados ao banco de dados com sucesso.")

            elif isinstance(data, dict):
                print(f"Iniciando a inserção de um único registro no banco de dados: {data}")

                try:
                    instance = CrudBaseRepository.model(**data)
                    session.add(instance)
                    print(f"Registro inserido com sucesso: {instance}")
                except Exception as e:
                    print(
                        f"Erro ao criar e inserir uma instância do modelo {CrudBaseRepository.model.__name__} com os dados {data}: {e}")
                    return False

            else:
                print(
                    "Erro: O formato de entrada não é válido. Esperado um dicionário contendo os dados de um único registro ou uma lista de dicionários contendo múltiplos registros.")
                return False

            return True

        except Exception as e:
            print(f"Erro ao inserir: {e}")
            return False

    @staticmethod
    @session_manager
    def update(where, with_, session):
        try:
            result = session.query(CrudBaseRepository.model).filter_by(**where).update(with_, synchronize_session=False)
            print(f"{result} registro(s) atualizado(s) com sucesso.")
            return result
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar: {e}")
            return 0

    @staticmethod
    @session_manager
    def delete(where, session):
        try:
            result = session.query(CrudBaseRepository.model).filter_by(**where).delete()
            print(f"{result} registro(s) deletado(s) com sucesso.")
            return result
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            return 0

    @staticmethod
    @session_manager
    def get_by_field(session, where, fields=None):
        try:
            query = session.query(CrudBaseRepository.model).filter_by(**where)
            if fields:
                query = query.with_entities(*[getattr(CrudBaseRepository.model, field) for field in fields])
                return [dict(zip(fields, obj)) for obj in query.all()]
            else:
                return [
                    {key: value for key, value in obj.__dict__.items() if key != "_sa_instance_state"}
                    for obj in query.all()
                ]
        except Exception as e:
            print(f"Erro ao buscar registros: {e}")
            return []
