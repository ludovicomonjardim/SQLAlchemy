"""
Avaliacao/classification_crud.py
Este módulo fornece operações CRUD para a entidade Classificação.
"""

import logging
from repositories.classification_repository import ClassificationRepository
from models.classification import Classification


class ClassificationCrud:
    def __init__(self):
        self.table_repo = ClassificationRepository()

        self.tabel_name = "classification"

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
        new_classification = {
            "name": "PG-13",
            "description": "Acompanhamento recomendado p/ menores de 13 anos.",  # 🔹 Ajuste para <= 50 caracteres
            "min_age": 13
        }
        result = self.table_repo.insert(new_classification)
        if result["success"]:
            self.ids_inserted = result["data"]
            print(f"A classificação {new_classification['name']}, ID: {self.ids_inserted}, foi inserida com sucesso.")
        else:
            print(f"Erro ao inserir classificação: {result['error']}")
            logging.error(result["error"])

    def insert_multi(self):
        print(f"\nINSERT MULTI - {self.tabel_name.upper()}")

        # Lista de classificações para inserir
        classifications_data = [
            {"name": "G", "description": "Livre para todas as idades.", "min_age": 0},
            {"name": "PG", "description": "Acomp. sugerido p/ menores de 10 anos.", "min_age": 10},
            {"name": "PG-13", "description": "Acomp. recomendado p/ menores de 13 anos.", "min_age": 13},
            {"name": "R", "description": "Restrito p/ menores de 17 anos sem acomp.", "min_age": 17},
            {"name": "NC-17", "description": "Não recomendado p/ menores de 18 anos.", "min_age": 18},
        ]

        result = self.table_repo.insert(classifications_data)

        print(f"\nResultado da inserção múltipla: {result}")

        if result["success"]:
            self.ids_inserted_multi = result["data"]
            if isinstance(self.ids_inserted_multi, list) and len(self.ids_inserted_multi) > 0:
                print(f"IDs inseridos com sucesso: {self.ids_inserted_multi}")
            else:
                print("Nenhum registro foi inserido.")
        else:
            print(f"Erro na inserção múltipla: {result['error']}")

    def update(self):
        print(f"\nUPDATE - {self.tabel_name.upper()}")
        new_data = {
            "description": "Nova descrição válida",
            "min_age": 15
        }
        result = self.table_repo.update(where={"id": self.ids_inserted}, with_=new_data)
        if result["success"]:
            print(f"A classificação no ID: {self.ids_inserted} foi atualizada com sucesso.")
        else:
            print(f"Erro ao atualizar classificação: {result['error']}")
            logging.error(result["error"])

    def delete(self):
        print(f"\nDELETE - {self.tabel_name.upper()}")
        if not self.ids_inserted:
            print("Nenhum ID armazenado para exclusão.")
            return

        # Tentando excluir a classificação inserida
        result = self.table_repo.delete(where={"id": self.ids_inserted})

        if result["success"]:
            print(f"A classificação ID {self.ids_inserted} foi excluída com sucesso.")
        else:
            print(f"Erro ao excluir classificação: {result['error']}")

    def delete_multi(self):
        print(f"\nDELETE MULTI - {self.tabel_name.upper()}")

        if not self.ids_inserted_multi:
            print("Nenhum ID armazenado para exclusão.")
            return

        # Criando filtro para excluir múltiplos IDs
        filters = [Classification.id.in_(self.ids_inserted_multi)]

        # Chamando a função de exclusão múltipla
        result = self.table_repo.delete(filters)

        if result["success"]:
            print(f"Registros excluídos com sucesso: {result['deleted_count']}")
        else:
            print(f"Erro ao excluir múltiplos registros: {result['error']}")

    def select(self):
        print(f"\nSELECT - {self.tabel_name.upper()}")
        records = self.table_repo.select(where=None,
                                         filters=[Classification.name.ilike("P%")],
                                         fields=["id", "name", "description", "min_age"],
                                         order_by=["name asc"],
                                         limit=10)
        print("Resultado do retrieve:")
        for record in records:
            print(record)
