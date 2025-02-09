import logging

from repositories.actor_repository import ActorRepository
from models.actor import Actor
import names


class ActorCrud:
    def __init__(self):
        self.table_repo = ActorRepository()

        self.tabel_name = "actor"
        self.name_to_insert = names.get_full_name()
        self.ids_inserted = None
        self.ids_inserted_multi = None

        self.report()

        self.insert()
        self.report()

        self.update()
        self.report()

        self.delete()
        self.report()

        self.insert_multi()
        self.report()

        self.delete_multi()
        self.report()

        self.select()

    def report(self):
        print(f"\nREPORT - {self.tabel_name.upper()}")
        self.table_repo.report()

    def insert(self):
        print(f"\nINSERT - {self.tabel_name.upper()}")
        result = self.table_repo.insert({"name": self.name_to_insert})
        if result["success"]:
            self.ids_inserted = result["data"]  # Agora receberá diretamente o ID
            print(f"Deveria ser uma lista com os IDs das inserções: {self.ids_inserted}")
            
            print(f"\nO nome {self.name_to_insert}, ID: {self.ids_inserted}, foi inserido com sucesso")
        else:
            logging.error(result["error"])

    def insert_multi(self):
        print(f"\nINSERT MULTI - {self.tabel_name.upper()}")

        # Lista de atores para inserir
        actors_data = [
            {"name": "Meryl Streep"},
            {"name": "Robert De Niro"},
            {"name": "Morgan Freeman"},
            {"name": "Cate Blanchett"},
        ]

        # Chamando a função de inserção múltipla
        result = self.table_repo.insert(actors_data)

        print(f"\nResultado da inserção múltipla: {result}")

        # Exibindo o resultado
        if result["success"]:
            self.ids_inserted_multi = result["data"]

            if isinstance(self.ids_inserted_multi, list) and len(self.ids_inserted_multi) > 0:
                print(f"IDs inseridos com sucesso: {self.ids_inserted_multi}")
            else:
                print(f"Nenhum registro foi inserido.")
        else:
            print(f"Erro na inserção múltipla: {result['error']}")

    def update(self):
        print(f"\nUPDATE - {self.tabel_name.upper()}")
        new_name = names.get_full_name()
        result = self.table_repo.update(where={"id": self.ids_inserted}, with_={"name": new_name})
        if result["success"]:
            print(f"O nome no ID: {self.ids_inserted} agora é {new_name}. Atualização bem-sucedida.")
        else:
            logging.error(result["error"])

    def delete(self):
        print(f"\nDELETE - {self.tabel_name.upper()}")
        result = self.table_repo.delete(where={"id": self.ids_inserted})

        # result = self.table_repo.delete(where={"id": 139})
        # result = self.table_repo.delete(where={"id": 140})
        # result = self.table_repo.delete(where={"id": 141})
        # result = self.table_repo.delete(where={"id": 142})

        if result["success"]:
            print("Exclusão bem-sucedida.")
        else:
            logging.error(result["error"])

    def delete_multi(self):
        print(f"\nDELETE MULTI - {self.tabel_name.upper()}")

        if not self.ids_inserted_multi:
            print("Nenhum ID armazenado para exclusão.")
            return

        # Criando filtro para excluir múltiplos IDs
        filters = [Actor.id.in_(self.ids_inserted_multi)]

        # Chamando a função de exclusão múltipla
        result = self.table_repo.delete(filters)

        if result["success"]:
            print(f"Registros excluídos com sucesso: {result['deleted_count']}")
        else:
            print(f"Erro ao excluir múltiplos registros: {result['error']}")

    def select(self):
        print(f"\nSELECT - {self.tabel_name.upper()}")

        records = self.table_repo.select(where=None,
                                        filters=[Actor.name.ilike("T%")],
                                        fields=["id", "name"],
                                        order_by=["name asc"],
                                        limit=10)
        print(f"Resultado do retrieve:")
        for record in records:
            print(record)
