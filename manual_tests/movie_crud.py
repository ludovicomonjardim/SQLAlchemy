"""
manual_tests/movie_crud.py
Este módulo fornece operações CRUD para a entidade Movie.
"""

import logging
from repositories.movie_repository import MovieRepository
from models.movie import Movie


class MovieCrud:
    def __init__(self):
        self.table_repo = MovieRepository()

        self.tabel_name = "movie"
        self.default_data = {
            "title": "Matrix",
            "year": 1999,
            "duration": 136,
            "classification_id": 3,  # 🔹 ID de uma classificação existente
            "rating": 9,
            "active": True
        }
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
        result = self.table_repo.insert(self.default_data)
        if result["success"]:
            self.ids_inserted = result["data"]
            print(f"Filme ID {self.ids_inserted} foi inserido com sucesso.")
        else:
            print(f"Erro ao inserir filme: {result['error']}")
            logging.error(result["error"])

    def insert_multi(self):
        print(f"\nINSERT MULTI - {self.tabel_name.upper()}")

        # Lista de filmes para inserir
        movies_data = [
            {"title": "Gladiador", "year": 2000, "duration": 155, "classification_id": 4, "rating": 8, "active": True},
            {"title": "Clube da Luta", "year": 1999, "duration": 139, "classification_id": 5, "rating": 9, "active": True},
            {"title": "O Senhor dos Anéis", "year": 2001, "duration": 178, "classification_id": 5, "rating": 10, "active": True},
        ]

        result = self.table_repo.insert(movies_data)
        if result["success"]:
            self.ids_inserted_multi = result["data"]
            print("IDs inseridos com sucesso!")
        else:
            print(f"Erro na inserção múltipla: {result['error']}")

    def update(self):
        print(f"\nUPDATE - {self.tabel_name.upper()}")
        new_data = {"rating": 10, "duration": 140}
        result = self.table_repo.update(where={"id": self.ids_inserted}, with_=new_data)
        if result["success"]:
            print(f"O filme ID: {self.ids_inserted} foi atualizado com sucesso.")
        else:
            print(f"Erro ao atualizar filme: {result['error']}")
            logging.error(result["error"])

    def delete(self):
        print(f"\nDELETE - {self.tabel_name.upper()}")
        result = self.table_repo.delete(where={"id": self.ids_inserted})
        if result["success"]:
            print("Filme excluído com sucesso.")
        else:
            print(f"Erro ao excluir filme: {result['error']}")

    def delete_multi(self):
        print(f"\nDELETE MULTI - {self.tabel_name.upper()}")

        if not self.ids_inserted_multi:
            print("Nenhum ID armazenado para exclusão.")
            return

        filters = [Movie.id.in_(self.ids_inserted_multi)]

        result = self.table_repo.delete(filters)

        if result["success"]:
            print("Registros excluídos com sucesso!")
        else:
            print(f"Erro ao excluir múltiplos registros: {result['error']}")

    def select(self):
        print(f"\nSELECT - {self.tabel_name.upper()}")
        result = self.table_repo.select(where=None, fields=["id", "title", "year", "duration", "rating"], order_by=["title asc"], limit=10)

        if not result["success"]:
            print(f"Erro ao recuperar filmes: {result['error']}")
            return

        records = result["data"]  # 🔹 Obtendo a lista real de filmes

        print("Resultado do retrieve:")
        for record in records:
            print(f"{record.id} | {record.title:<25} | {record.year} | {record.duration} | {record.rating}")
