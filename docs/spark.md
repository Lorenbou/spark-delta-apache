# Apache Spark / PySpark

## O que é o Apache Spark?

**Apache Spark** é um motor de processamento de dados distribuído, de código aberto e alto desempenho.  
Foi criado para superar as limitações do Hadoop MapReduce, processando dados predominantemente **em memória**, o que o torna até 100× mais rápido para certas cargas de trabalho.

Suporta:

- Processamento em batch (grandes volumes de dados)
- Processamento em stream (dados em tempo real)
- SQL (Spark SQL)
- Machine Learning (MLlib)
- Grafos (GraphX)

---

## Arquitetura

O Spark opera no modelo **Driver / Executors**:

```
┌─────────────────────────────────────┐
│            Driver Program            │
│  ┌──────────────────────────────┐   │
│  │        SparkContext           │   │
│  │  (coordena toda a execução)   │   │
│  └──────────────┬───────────────┘   │
└─────────────────┼───────────────────┘
                  │ distribui tarefas
        ┌─────────┼─────────┐
        ▼         ▼         ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │Executor │ │Executor │ │Executor │
   │ Task 1  │ │ Task 2  │ │ Task 3  │
   └─────────┘ └─────────┘ └─────────┘
```

| Componente | Função |
|---|---|
| **Driver** | Coordena a aplicação, cria o SparkContext, distribui tarefas |
| **Executor** | Processa as tarefas em cada nó do cluster |
| **SparkContext** | Ponto de entrada para recursos do cluster |
| **SparkSession** | API unificada (substitui SparkContext, SQLContext, HiveContext) |

---

## PySpark

**PySpark** é a API Python oficial do Apache Spark.  
Permite escrever código Python que é traduzido e executado pelo motor Spark via a biblioteca Py4J (ponte Python ↔ JVM).

### Por que usar PySpark?

- Python é a linguagem dominante em Data Science e Engenharia de Dados
- API expressiva e de alto nível (DataFrames, Spark SQL)
- Integração nativa com bibliotecas como Pandas, NumPy e Matplotlib
- Suporte a Jupyter Notebooks

---

## SparkSession

`SparkSession` é o ponto de entrada único para todas as funcionalidades Spark modernas.

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("MeuApp")
    .master("local[*]")
    .getOrCreate()
)
```

| Parâmetro | Descrição |
|---|---|
| `.appName("nome")` | Nome da aplicação exibido na Spark UI |
| `.master("local[*]")` | Modo de execução (local usa todos os núcleos da CPU) |
| `.config("chave", "valor")` | Configurações adicionais (catálogos, JARs, etc.) |
| `.getOrCreate()` | Retorna uma SparkSession existente ou cria uma nova |

---

## Modo Local (`local[*]`)

Em desenvolvimento, usamos `master("local[*]")`:

- **`local`** — 1 thread (sem paralelismo)
- **`local[2]`** — 2 threads
- **`local[*]`** — usa todos os núcleos disponíveis na máquina

Não é necessário um cluster Hadoop/YARN para rodar localmente. Ideal para desenvolvimento e testes.

---

## DataFrames e Spark SQL

O Spark trabalha com **DataFrames** — estruturas de dados distribuídas semelhantes a tabelas SQL ou DataFrames do Pandas.

```python
# Criar DataFrame a partir de dados inline
df = spark.createDataFrame([
    (1, "Ana Silva", "São Paulo"),
    (2, "Bruno Costa", "Rio de Janeiro"),
], schema=["id", "nome", "cidade"])

df.show()
```

O **Spark SQL** permite executar consultas SQL padrão sobre DataFrames e tabelas:

```python
df.createOrReplaceTempView("clientes")
spark.sql("SELECT * FROM clientes WHERE cidade = 'São Paulo'").show()
```

---

## Requisitos de Ambiente

```bash
# Java 11 ou 17 obrigatório
java -version

# Verificar PySpark
poetry run python -c "import pyspark; print(pyspark.__version__)"
```

---

## Referências

- [Apache Spark — Documentação Oficial](https://spark.apache.org/docs/3.5.3/)
- [PySpark API Reference](https://spark.apache.org/docs/3.5.3/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/3.5.3/sql-programming-guide.html)
