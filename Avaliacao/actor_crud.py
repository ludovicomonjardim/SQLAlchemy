from repositories.actor_repository import ActorRepository


class ActorCrud:
    def __init__(self):
        self.tabel_name = "actor"
        self.table = ActorRepository()

        self.name_to_insert = "Tomasio Hanks"
        self.id_inserted = None

        self.list_all()
        self.insert()
        self.update()

        self.list_all()
        self.delete()

    def list_all(self):
        print(f"\nLISTING all from {self.tabel_name}...")
        self.table.print_all()

    def insert(self):
        print(f"\nINSERTING a new record in {self.tabel_name}...")
        result = self.table.insert({"name": self.name_to_insert})
        if not isinstance(result, str):
            self.id_inserted = result[0]

        print(f"Resultado do insert: {result}")

    def delete(self):
        print(f"\nDELETING actor ID {self.id_inserted}...")
        message = self.table.delete(where={"id": self.id_inserted})
        print(f"Resultado do delete: {message}")  # Exibe a resposta amigável

    def update(self):
        print(f"\nUPDATING a record in {self.tabel_name}...")
        result = self.table.update(with_={"name": "Antônio Ranques"}, where={"id": self.id_inserted})
        print(f"Resultado do update: {result}")

    def retrieve(self, conditions=None, fields_to_retrieve=None):
        print(f"\nQUERYING a record in {self.tabel_name}...")
        result = self.table.get_by_field(where=conditions, fields=fields_to_retrieve)
        print(f"Resultado do retrieve: {result}")
