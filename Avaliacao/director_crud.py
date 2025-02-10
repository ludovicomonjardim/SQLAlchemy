"""
Avaliacao/director_crud.py
Este módulo fornece operações CRUD para a entidade Diretor.
"""

import logging
from repositories.director_repository import DirectorRepository
from models.director import Director
import names


class DirectorCrud:
    def __init__(self):
        self.table_repo = DirectorRepository()

        self.tabel_name = "director"
        self.name_to_insert = names.get_full_name()
        self.ids_inserted = None
        self.ids_inserted_multi = None

        self.report()

        self.insert()
        # self.report()

        self.update()
        # self.report()

        self.delete()
        # self.report()

        self.insert_multi()
        # self.report()

        self.delete_multi()
        # self.report()

        self.select()

    def report(self):
        print(f"\nREPORT - {self.tabel_name.upper()}")
        self.table_repo.report()

    def insert(self):
        print(f"\nINSERT - {self.tabel_name.upper()}")
        result = self.table_repo.insert({"name": self.name_to_insert})
        if result["success"]:
            self.ids_inserted = result["data"]
            print(f"O nome {self.name_to_insert}, ID: {self.ids_inserted}, foi inserido com sucesso.")
        else:
            logging.error(result["error"])

    def insert_multi(self):
        print(f"\nINSERT MULTI - {self.tabel_name.upper()}")

        # Lista de diretores para inserir
        directors_data = [
            {"name": "Walter Salles"},
            {"name": "Cacá Diegues"},
            {"name": "José Padilha"},
            {"name": "Glauber Rocha"},
        ]

        result = self.table_repo.insert(directors_data)
        if result["success"]:
            self.ids_inserted_multi = result["data"]
            if isinstance(self.ids_inserted_multi, list) and len(self.ids_inserted_multi) > 0:
                print("IDs inseridos com sucesso!")
            else:
                print("Nenhum registro foi inserido.")
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
        filters = [Director.id.in_(self.ids_inserted_multi)]

        # Chamando a função de exclusão múltipla
        result = self.table_repo.delete(filters)

        if result["success"]:
            print("Registros excluídos com sucesso!")
        else:
            print(f"Erro ao excluir múltiplos registros: {result['error']}")

    def select(self):
        print(f"\nSELECT - {self.tabel_name.upper()}")
        result = self.table_repo.select(where=None,
                                         filters=[Director.name.ilike("C%")],
                                         fields=["id", "name"],
                                         order_by=["name asc"],
                                         limit=10)

        if not result["success"]:
            print(f"Erro ao recuperar diretores: {result['error']}")
            return

        records = result["data"]
        print("Resultado do SELECT:")
        for record in records:
            print(f"{record.id} | {record.name}")
