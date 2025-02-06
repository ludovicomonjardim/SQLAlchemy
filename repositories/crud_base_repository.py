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
        """Insere um novo registro no banco de dados."""
        if not cls.model:
            raise ValueError(f"{cls.__name__} must define 'model'.")

        try:
            if isinstance(data, list):
                if not all(isinstance(obj, dict) for obj in data):
                    print("Erro: Todos os itens devem ser dicionários.")
                    return False

                print(f"Iniciando a inserção de {len(data)} registros...")

                instances = [cls.model(**obj) for obj in data]
                session.add_all(instances)
                print(f"{len(instances)} registros inseridos com sucesso.")

            elif isinstance(data, dict):
                print(f"\nIniciando a inserção de um único registro: {data}")
                instance = cls.model(**data)
                session.add(instance)
                # print(f"Registro inserido com sucesso: {instance}")

            else:
                print("Erro: O formato de entrada não é válido.")
                return False

            return True

        except Exception as e:
            print(f"Erro ao inserir: {e}")
            return False

    @classmethod
    @session_manager
    def update(cls, where, with_, session):
        """Atualiza registros com base em um critério."""
        try:
            result = session.query(cls.model).filter_by(**where).update(with_, synchronize_session=False)
            print(f"{result} registro(s) atualizado(s) com sucesso.")
            return result
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar: {e}")
            return 0

    @classmethod
    @session_manager
    def delete(cls, where, session=None):
        """Deleta registros com base em um critério."""
        session = session or get_session()  # Criar sessão apenas se não for fornecida
        try:
            result = session.query(cls.model).filter_by(**where).delete()
            session.commit()
            print(f"{result} registro(s) deletado(s) com sucesso.")
            return result
        except Exception as e:
            session.rollback()
            print(f"Erro ao deletar: {e}")
            return 0

    @classmethod
    @session_manager
    def get_by_field(cls, session, where, fields=None):
        """Busca registros pelo campo especificado."""
        try:
            query = session.query(cls.model).filter_by(**where)

            if fields:
                valid_fields = [field for field in fields if hasattr(cls.model, field)]
                if not valid_fields:
                    print("Nenhum campo válido fornecido.")
                    return []

                query = query.with_entities(*[getattr(cls.model, field) for field in valid_fields])
                return [dict(zip(valid_fields, obj)) for obj in query.all()]
            else:
                return [
                    {key: value for key, value in obj.__dict__.items() if key != "_sa_instance_state"}
                    for obj in query.all()
                ]
        except Exception as e:
            print(f"Erro ao buscar registros: {e}")
            return []
