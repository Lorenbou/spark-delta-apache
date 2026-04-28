# spark-delta-apache

Trabalho universitário da disciplina de **Arquitetura de Dados** demonstrando o uso de **Delta Lake** e **Apache Iceberg** com **Apache Spark (PySpark)**.

**Participantes:** Gabriel Minatto · Anderson dos Santos · Lorenzo

---

## Documentação

A documentação completa (MKDocs) está publicada em:

> **https://lorenbou.github.io/spark-delta-apache/**

---

## Estrutura do Projeto

```
spark-delta-apache/
├── notebooks/
│   ├── delta_lake.ipynb       # Delta Lake: DDL + INSERT/UPDATE/DELETE + Time Travel
│   └── apache_iceberg.ipynb   # Iceberg: DDL + INSERT/UPDATE/DELETE + Snapshots
├── docs/
│   ├── index.md               # Contextualização do projeto
│   ├── spark.md               # Apache Spark / PySpark
│   ├── delta.md               # Delta Lake
│   └── iceberg.md             # Apache Iceberg
├── Dockerfile                 # Imagem com Python 3.11 + Java 17 + dependências
├── docker-compose.yml         # Serviços: jupyter (8888) e mkdocs (8000)
├── pyproject.toml             # Dependências gerenciadas pelo Poetry
├── mkdocs.yml                 # Configuração da documentação
└── README.md
```

---

## Pré-requisitos

| Requisito | Verificação |
|---|---|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | `docker --version` |
| [Docker Compose](https://docs.docker.com/compose/) | `docker compose version` |
| Git | `git --version` |

> Não é necessário instalar Python, Java ou Poetry localmente. Tudo roda dentro dos containers.

---

## Reprodução do Ambiente com Docker Compose

### 1. Clonar o repositório

```bash
git clone https://github.com/Lorenbou/spark-delta-apache.git
cd spark-delta-apache
```

### 2. Construir as imagens e subir os serviços

```bash
docker compose up --build
```

Na **primeira execução**, o Docker irá:
- Baixar a imagem base `python:3.11-slim` (~50 MB)
- Instalar o OpenJDK 17
- Instalar todas as dependências Python via Poetry

As execuções seguintes usam o cache da imagem e sobem em segundos.

### 3. Acessar o JupyterLab

Abra no navegador:

```
http://localhost:8888
```

Não é necessária senha. Abra os notebooks na pasta `notebooks/`:

- [`delta_lake.ipynb`](notebooks/delta_lake.ipynb) — demonstração com **Delta Lake**
- [`apache_iceberg.ipynb`](notebooks/apache_iceberg.ipynb) — demonstração com **Apache Iceberg**

> Na **primeira execução** do notebook Iceberg, o Spark baixará o JAR do Iceberg (~35 MB) do Maven Central. O JAR fica em cache em `.ivy2/` para as próximas execuções.

### 4. Acessar o preview do MKDocs

```
http://localhost:8000
```

### 5. Acessar a Spark UI (durante a execução de um notebook)

```
http://localhost:4040
```

### 6. Parar os serviços

```bash
docker compose down
```

---

## Serviços Docker

| Serviço | Porta | Descrição |
|---|---|---|
| `jupyter` | `8888` | JupyterLab com PySpark + Delta Lake + Iceberg |
| `jupyter` | `4040` | Spark UI (disponível durante execução de notebooks) |
| `mkdocs` | `8000` | Preview da documentação MKDocs |

---

## Dependências da Imagem

| Biblioteca | Versão | Finalidade |
|---|---|---|
| Python | 3.11 | Linguagem base |
| OpenJDK | 17 | Runtime obrigatório para PySpark |
| `pyspark` | 3.5.3 | Motor de processamento distribuído |
| `delta-spark` | 3.2.0 | Suporte a tabelas Delta Lake |
| `jupyterlab` | ≥4.2.5 | Ambiente de notebooks |
| `ipykernel` | ≥6.29.5 | Kernel Python para Jupyter |
| `mkdocs` | ≥1.6.0 | Gerador de documentação |
| `mkdocs-material` | ≥9.5.0 | Tema da documentação |

> O **Apache Iceberg** é carregado via Maven em tempo de execução com a coordenada `org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1` — sem instalação pip adicional.

---

## Publicar a Documentação no GitHub Pages

Execute o comando dentro do container `jupyter`:

```bash
docker compose exec jupyter mkdocs gh-deploy
```

Ou rode localmente com Poetry (veja seção abaixo).

Após o deploy, ative o GitHub Pages no repositório:
**Settings → Pages → Source → Branch: `gh-pages` / `/ (root)`**

---

## Alternativa: Execução Local com Poetry

Caso prefira rodar sem Docker, instale os pré-requisitos ([Python 3.11](https://python.org), [Java 17](https://adoptium.net/), [Poetry](https://python-poetry.org/docs/#installation)) e execute:

```bash
# Instalar dependências
poetry install

# Registrar kernel Jupyter
poetry run python -m ipykernel install --user \
    --name spark-delta-apache \
    --display-name "Python (spark-delta-apache)"

# Abrir JupyterLab
poetry run jupyter lab

# Preview da documentação
poetry run mkdocs serve

# Publicar no GitHub Pages
poetry run mkdocs gh-deploy
```

---

## Referências

- [Apache Spark](https://spark.apache.org/docs/3.5.3/)
- [Delta Lake](https://delta.io/)
- [Apache Iceberg](https://iceberg.apache.org/)
- [Delta Lake × PySpark — Compatibilidade](https://docs.delta.io/latest/releases.html)
- [Iceberg Spark Runtime — Maven](https://search.maven.org/artifact/org.apache.iceberg/iceberg-spark-runtime-3.5_2.12)
- [Canal DataWay BR](https://www.youtube.com/@DataWayBR)
- [spark-delta (referência)](https://github.com/jlsilva01/spark-delta)
- [spark-iceberg (referência)](https://github.com/jlsilva01/spark-iceberg)
