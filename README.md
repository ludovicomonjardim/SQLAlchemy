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
├── .dockerignore 
├── database.py                         # Configuração do banco (engine, conn e sessionmaker)
├── docker-compose-yml 
├── Dockerfile
├── main.py                             # Ponto de entrada do programa
├── requirements.txt
├── wait-for-it.sh
~~~~

# Resumo da Função de Cada Arquivo
## SQLAlchemy/
### Contém as subpastas models/, repositories/, utils/, além dos arquivos main.py e database.py.
- SQLAlchemy/database.py
     - Responsável pela configuração da engine e Session do SQLAlchemy.
     - Cria a conexão com o banco e inicializa as tabelas conforme os modelos ORM.
     - Fornece um gerenciador de conexão via get_connection().
- SQLAlchemy/main.py
     - Arquivo principal do projeto, onde as funções do repositório são chamadas.
     - Inicializa o banco de dados e executa operações CRUD (create, read, update, delete).
     - Demonstra o uso de SQL puro (não recomendado para produção).

## SQLAlchemy/models/
### Contém os modelos ORM, que definem as tabelas do banco de dados.
- models/base.py
    - Define a Base Declarativa do SQLAlchemy, usada como classe base para todos os modelos ORM.
- models/filme.py
    - Define a classe Filme, representando a tabela filmes.
    - Especifica os atributos da tabela, incluindo id, titulo, genero, ano, diretor, nota e ativo.
    - Inclui validações para colunas como ano e genero.

## SQLAlchemy/repositories/
### Contém os repositórios que encapsulam as consultas ao banco.
- repositories/filme_repository.py
    - Implementa a classe FilmeRepository, que contém métodos para:
        - Inserir (insert)
        - Atualizar (update)
        - Deletar (delete)
        - Buscar (get_by_field, get_by_titulo)
        - Listar (print_all)
    - Utiliza o decorador @session_manager para gerenciar transações.

## SQLAlchemy/utils/
### Contém utilitários gerais do projeto.
- utils/migration.py
    - Gerencia e atualiza automaticamente a estrutura das tabelas no banco de dados.
    - Verifica colunas ausentes e adiciona novas conforme o modelo definido.
    - Usa inspect() para comparar a estrutura existente e aplicar mudanças sem perder dados.
- utils/session.py
    - Define o decorador @session_manager para gerenciar sessões do SQLAlchemy.
    - Garante commit automático e faz rollback em caso de erro.
    - Centraliza a lógica de abertura e fechamento de sessões.
