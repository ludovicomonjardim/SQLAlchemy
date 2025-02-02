#!/bin/sh
# Script para esperar o PostgreSQL ficar pronto antes de iniciar a aplicação

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until pg_isready -h "$host" -p "$port"; do
  >&2 echo "Aguardando PostgreSQL em $host:$port..."
  sleep 2
done

>&2 echo "PostgreSQL está pronto! Executando aplicação..."
exec $cmd
