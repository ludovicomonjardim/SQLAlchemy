# Estrutura do projeto:

~~~~ 
SQLAlchemy/
├── .github/
│   ├── workflows
│       ├── ci-cd.yml
├── venv/
├── Avaliacao/
│   ├── __init__.py                     # Inicializa o pacote models (opcional)
│   ├── actor_crud.py
│   ├── cinema_session_crud.py
│   ├── classification_crud.py
│   ├── director_crud.py
│   ├── genre_crud.py
│   ├── movie_crud.py
│   ├── ticket_crud.py
├── models/
│   ├── __init__.py                     # Inicializa o pacote models (opcional)
│   ├── actor.py
│   ├── base.py
│   ├── cinema_session.py
│   ├── classification.py
│   ├── director.py
│   ├── genre.py
│   ├── movie.py
│   ├── movie_actor.py
│   ├── movie_director.py
│   ├── movie_genre.py
│   ├── ticket.py
├── repositories/
│   ├── __init__.py                     # Inicializa o pacote repositories (opcional)
│   ├── actor_repository.py             # Repositório para Atores
│   ├── cinema_session_repository.py    # Repositório para seções
│   ├── classification_repository.py    # Repositório para classificações
│   ├── crud_base_repository.py         # Repositório base com CRUD
│   ├── director_repository.py          # Repositório para diretores
│   ├── genre_repository.py             # Repositório para Gêneros 
│   ├── movie_actor_repository.py       # Repositório para atores
│   ├── movie_director_repository.py    # Repositório para diretores
│   ├── movie_repository.py             # Repositório para Filme
│   ├── ticket_repository.py            # Repositório para Ingresso 
├── utils/                              # Pasta para utilitários
│   ├── __init__.py                     # Inicializa o pacote utils (opcional)
│   ├── migration.py                    # Atualiza automaticamente a estrutura das tabelas no banco
│   ├── session.py                      # Gerenciamento de sessões (decorador)
│   ├── populate.py 
├── tests/                              # Pasta para teste
│   ├── __init__.py                     # Inicializa o pacote utils (opcional)
│   ├── test_actor_repository.py
├── .dockerignore 
├── database.py                         # Configuração do banco (engine, conn e sessionmaker)
├── docker-compose-yml 
├── Dockerfile
├── main.py                             # Ponto de entrada do programa
├── requirements.txt
├── wait-for-it.sh
~~~~

