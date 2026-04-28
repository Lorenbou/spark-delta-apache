FROM python:3.11-slim

# default-jdk-headless instala Java 17 no Debian Bookworm e cria o symlink
# /usr/lib/jvm/default-java automaticamente — funciona em AMD64 e ARM64
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-jdk-headless \
        procps \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV PYSPARK_PYTHON=python3
ENV PYTHONUNBUFFERED=1

# Instalar Poetry e desativar virtualenv (desnecessário em container)
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false

WORKDIR /app

# Copiar manifesto de dependências e instalar
COPY pyproject.toml ./
RUN poetry install --no-root --no-interaction --no-ansi

# Copiar o restante do projeto
COPY . .

# Criar diretório do warehouse do Spark
RUN mkdir -p /app/spark-warehouse

EXPOSE 8888 4040 8000
