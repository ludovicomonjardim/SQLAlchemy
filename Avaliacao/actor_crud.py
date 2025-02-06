from repositories.actor_repository import ActorRepository


class ActorCrud:
    def __init__(self):
        self.tabel_name = "actor"
        self.table = ActorRepository()
        self.new_id = None

        self.list_all()
        self.insert("Tom Hanks")
        self.delete(self.new_id)



    def list_all(self):
        print(f"\nLISTING all from {self.tabel_name}...")
        self.table.print_all()

    def insert(self, name):
        print(f"\nINSERTING a new record in {self.tabel_name}...")
        self.table.insert({"name": name})
        self.new_id = self.table.get_by_field(where={"name": name}, fields=["id"])

        self.new_id = self.new_id[0]["id"]
        print(f"\nId de {name}: {self.new_id}")

        return self.new_id

    def delete(self, record_id):
        print(f"\nDELETING actor ID {record_id}...")
        message = self.table.delete({"id": record_id})
        print(message)  # Exibe a resposta amigável

    def update(self):
        print(f"\nINSERTING a new record in {self.tabel_name}...")
        self.table.insert({"title":"Matrix", "year":1999, "duration":148, "classification_id":4, "rating":9}),

    def query(self):
        print("\nQUERYING movies of the 'Drama' genre...")
        movies = self.table.get_by_field(where={"genre": "Drama"})
        for movie in movies:
            print(movie)  # Now the dictionaries will not contain `_sa_instance_state`
