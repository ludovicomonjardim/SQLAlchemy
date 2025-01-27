from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/cinema"

# Criação da engine
engine = create_engine(DATABASE_URL)

# Testando a conexão
try:
    with engine.connect() as connection:
        print("Conexão bem-sucedida!")

        result = connection.execute(text('SELECT * FROM public.filmes;'))

        # Consulta, incluindo o schema explicitamente
        # result = connection.execute(text("SELECT * FROM public.filmes;"))
        for row in result:
            print(row)  # Cada linha será uma tupla representando os dados
except Exception as e:
    print(f"Erro: {e}")
