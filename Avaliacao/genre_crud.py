from repositories.genre_repository import GenreRepository
from models.genre import Genre
import names


class GenreCrud:
    def __init__(self):
        self.table_repo = GenreRepository()

        self.tabel_name = "genre"
        self.name_to_insert = names.get_full_name()
        self.id_inserted = None

        self.report()

        self.insert()
        self.report()

        self.update()
        self.report()

        self.delete()
        self.report()

        self.obtain()

    def report(self):
        print(f"\nLISTING all from table: {self.tabel_name.upper()}.")
        self.table_repo.report()

    def insert(self):
        print(f"\nINSERTING")
        print(f"Inserting - Name: {self.name_to_insert}")
        result = self.table_repo.insert({"name": self.name_to_insert})
        if not isinstance(result, str):
            self.id_inserted = result[0]
        print(f"Resultado do insert: {result} Name: {self.name_to_insert}")

    def update(self):
        novo_nome = names.get_full_name()

        print(f"\nUPDATING")
        print(f"Replacing - with: {novo_nome}")
        result = self.table_repo.update(with_={"name": novo_nome}, where={"id": self.id_inserted})
        print(f"Resultado do update: {result}")

    def delete(self):
        print(f"\nDELETING")
        print(f"Deleting - Id: {self.id_inserted}")
        message = self.table_repo.delete(where={"id": self.id_inserted})
        print(f"Resultado do delete: {message}")  # Exibe a resposta amigável

    def obtain(self):
        print(f"\nQUERYING")
        print(f"Querying - for ")
        records = self.table_repo.obtain(where=None,
                                        filters=[Genre.name.ilike("T%")],
                                        fields=["id", "name"],
                                        order_by=["name asc"],
                                        limit=10)
        print(f"Resultado do retrieve:")
        for record in records:
            print(record)
