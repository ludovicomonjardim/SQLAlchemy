"""
manual_tests/cinema_session_crud.py
Este módulo fornece operações CRUD para a entidade CinemaSession.
"""

import logging
from repositories.cinema_session_repository import CinemaSessionRepository
from models.cinema_session import CinemaSession
from datetime import date, time


class CinemaSessionCrud:
    def __init__(self):
        self.table_repo = CinemaSessionRepository()

        self.tabel_name = "cinema_session"

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

        # Nova seção de cinema a ser inserida
        new_movie_session = {
            "movie_id": 1,
            "date": date.today(),
            "time": time(21, 30),
            "room": "Sala 1",
            "capacity": 100,
            "price": 25.00
        }

        result = self.table_repo.insert(new_movie_session)
        if result["success"]:
            self.ids_inserted = result["data"]
            print(f"✅ Sessão de cinema ID {self.ids_inserted} foi inserida com sucesso.")
        else:
            print(f"❌ Erro ao inserir sessão de cinema: {result['error']}")
            logging.error(result["error"])

    def insert_multi(self):
        print(f"\nINSERT MULTI - {self.tabel_name.upper()}")

        # Lista de sessões para inserir
        sessions_data = [
            {"movie_id": 1, "date": date.today(), "time": time(18, 00), "room": "Sala 2", "capacity": 80, "price": 22.00},
            {"movie_id": 2, "date": date.today(), "time": time(20, 00), "room": "Sala 3", "capacity": 120, "price": 30.00},
            {"movie_id": 3, "date": date.today(), "time": time(21, 30), "room": "Sala 1", "capacity": 100, "price": 28.00},
        ]

        result = self.table_repo.insert(sessions_data)
        if result["success"]:
            self.ids_inserted_multi = result["data"]
            print(f"✅ IDs inseridos com sucesso!")
        else:
            print(f"❌ Erro na inserção múltipla: {result['error']}")

    def update(self):
        print(f"\nUPDATE - {self.tabel_name.upper()}")
        new_data = {
            "price": 35.00,
            "capacity": 90
        }
        result = self.table_repo.update(where={"id": self.ids_inserted}, with_=new_data)
        if result["success"]:
            print(f"✅ A sessão de cinema ID: {self.ids_inserted} foi atualizada com sucesso.")
        else:
            print(f"❌ Erro ao atualizar sessão de cinema: {result['error']}")
            logging.error(result["error"])

    def delete(self):
        print(f"\nDELETE - {self.tabel_name.upper()}")
        if not self.ids_inserted:
            print("❌ Nenhum ID armazenado para exclusão.")
            return

        result = self.table_repo.delete(where={"id": self.ids_inserted})
        if result["success"]:
            print(f"✅ A sessão de cinema ID {self.ids_inserted} foi excluída com sucesso.")
        else:
            print(f"❌ Erro ao excluir sessão de cinema: {result['error']}")

    def delete_multi(self):
        print(f"\nDELETE MULTI - {self.tabel_name.upper()}")

        if not self.ids_inserted_multi:
            print("❌ Nenhum ID armazenado para exclusão.")
            return

        filters = [CinemaSession.id.in_(self.ids_inserted_multi)]

        result = self.table_repo.delete(filters)

        if result["success"]:
            print("✅ Registros excluídos com sucesso!")
        else:
            print(f"❌ Erro ao excluir múltiplos registros: {result['error']}")

    def select(self):
        print(f"\nSELECT - {self.tabel_name.upper()}")
        result = self.table_repo.select(where=None,
                                         filters=[CinemaSession.room.ilike("Sala%")],
                                         fields=["id", "date", "time", "room", "capacity", "price"],
                                         order_by=["date asc"],
                                         limit=10)

        if not result["success"]:
            print(f"❌ Erro ao recuperar seçoes de cinema: {result['error']}")
            return

        records = result["data"]

        print("Resultado do SELECT:")
        for record in records:
            print(f"✅ {record.id} | {record.date} | {record.time} | {record.room} | {record.capacity} | {record.price}")
