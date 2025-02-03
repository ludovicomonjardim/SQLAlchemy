# Usar a imagem oficial do Python como base
FROM python:3.12

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Instalar o cliente PostgreSQL (para usar pg_isready)
RUN apt-get update && apt-get install -y postgresql-client

# Copiar os arquivos do projeto para dentro do container
COPY . /app

# Ajustar permissões do wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Criar e ativar o ambiente virtual
RUN python -m venv venv

# Instalar dependências dentro do ambiente virtual
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Definir a variável de ambiente para evitar buffer no output do terminal
ENV PYTHONUNBUFFERED=1

# Comando para rodar a aplicação, esperando o PostgreSQL ficar pronto antes de iniciar
#CMD ["/bin/bash", "-c", "/app/wait-for-it.sh db 5432 -- /bin/bash -c 'source venv/bin/activate && python main.py'"]
CMD ["/bin/bash", "-c", "/app/wait-for-it.sh db 5432 && exec /bin/bash -c 'source venv/bin/activate && python main.py'"]

