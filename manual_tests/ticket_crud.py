"""
manual_tests/ticket_crud.py
Este módulo fornece operações CRUD para a entidade Ticket.
"""

import logging
from repositories.ticket_repository import TicketRepository
from models.ticket import Ticket
from datetime import datetime, UTC


class TicketCrud:
    def __init__(self):
        self.table_repo = TicketRepository()

        self.tabel_name = "ticket"
        self.ids_inserted = None
        self.ids_inserted_multi = None

        self.report()

        self.insert()
        # self.report()

        self.insert_multi()
        # self.report()

        self.select()

    def report(self):
        print(f"\nREPORT - {self.tabel_name.upper()}")
        self.table_repo.report()

    def insert(self):
        print(f"\nINSERT - {self.tabel_name.upper()}")

        new_ticket = {
            "cinema_session_id": 1,  # ID de uma sessão existente no banco
            "customer": "John Doe",
            "purchase_date": datetime.now(UTC)
        }

        result = self.table_repo.insert(new_ticket)
        if result["success"]:
            self.ids_inserted = result["data"]
            print(f"✅ Ingresso ID {self.ids_inserted} foi inserido com sucesso.")
        else:
            print(f"❌ Erro ao inserir ingresso: {result['error']}")
            logging.error(result["error"])

    def insert_multi(self):
        print(f"\nINSERT MULTI - {self.tabel_name.upper()}")

        # Lista de ingressos para inserir
        tickets_data = [
            {"cinema_session_id": 1, "customer": "Alice Johnson", "purchase_date": datetime.now(UTC)},
            {"cinema_session_id": 2, "customer": "Bob Smith", "purchase_date": datetime.now(UTC)},
            {"cinema_session_id": 3, "customer": "Charlie Brown", "purchase_date": datetime.now(UTC)},
        ]

        result = self.table_repo.insert(tickets_data)
        if result["success"]:
            self.ids_inserted_multi = result["data"]
            print(f"✅ IDs inseridos com sucesso!")
        else:
            print(f"❌ Erro na inserção múltipla: {result['error']}")

    def select(self):
        print(f"\nSELECT - {self.tabel_name.upper()}")
        result = self.table_repo.select(where=None,
                                         filters=[Ticket.customer.ilike("A%")],
                                         fields=["id", "cinema_session_id", "customer", "purchase_date"],
                                         order_by=["purchase_date desc"],
                                         limit=10)

        if not result["success"]:
            print(f"❌ Erro ao recuperar ingressos: {result['error']}")
            return

        records = result["data"]

        print("Resultado do SELECT:")
        for record in records:
            print(f"✅ {record.id} | {record.cinema_session_id} | {record.customer:<30} | {record.purchase_date}")
