# Usar a imagem oficial do Python como base
FROM python:3.12

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar script de espera
COPY wait-for-it.sh /app/wait-for-it.sh

# Definir permissões dentro do Docker (funciona no Windows)
RUN chmod +x /app/wait-for-it.sh

# Copiar os arquivos do projeto para dentro do container
COPY . /app

# Criar e ativar o ambiente virtual
RUN python -m venv venv

# Instalar dependências dentro do ambiente virtual
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Definir a variável de ambiente para evitar buffer no output do terminal
ENV PYTHONUNBUFFERED=1

# Comando para rodar a aplicação, esperando o PostgreSQL ficar pronto antes de iniciar
CMD ["/app/wait-for-it.sh", "db", "5432", "--", "/bin/bash", "-c", "source venv/bin/activate && python main.py"]
