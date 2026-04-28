# Apache Iceberg

## O que é o Apache Iceberg?

**Apache Iceberg** é um formato de tabela open-source de alto desempenho para datasets analíticos em grande escala.  
Foi criado pela Netflix e doado à Apache Software Foundation. É amplamente adotado por empresas como Netflix, Apple, Adobe e Airbnb.

Assim como o Delta Lake, traz transações ACID ao Apache Spark, mas com foco em **interoperabilidade** — suporta múltiplos motores de query (Spark, Flink, Trino, Hive, Presto) por meio de um formato de metadados aberto e padronizado.

---

## Funcionalidades Principais

| Funcionalidade | Descrição |
|---|---|
| **Transações ACID** | Operações atômicas com isolamento de snapshot |
| **Snapshots** | Cada operação cria um novo snapshot imutável |
| **Time Travel** | Leitura de versões anteriores por `snapshot-id` ou timestamp |
| **Schema Evolution** | Adicionar, renomear e remover colunas sem reescrever dados |
| **Partition Evolution** | Mudar o esquema de particionamento sem migração de dados |
| **Hidden Partitioning** | O usuário não precisa referenciar colunas de partição em queries |
| **DML completo** | `UPDATE`, `DELETE`, `MERGE INTO` via Spark extensions |

---

## Iceberg vs Delta Lake

| Característica | Delta Lake | Apache Iceberg |
|---|---|---|
| Instalação pip | `delta-spark` | Nenhuma (JAR via Maven) |
| Catálogo padrão | `spark_catalog` | Catálogo nomeado (`local`, `glue`, etc.) |
| Prefixo das tabelas | Sem prefixo | `<catalog>.<tabela>` |
| Histórico | `DESCRIBE HISTORY` / `.history()` | `.snapshots` / `.history` |
| Time Travel | `versionAsOf` | `snapshot-id` ou `as-of-timestamp` |
| Interoperabilidade | Principalmente Spark/Databricks | Spark, Flink, Trino, Hive, Presto |
| Partition Evolution | Limitado | Nativo e sem reescrita de dados |

---

## Configuração do SparkSession

O Iceberg **não tem pacote pip** para o runtime Spark. O JAR é carregado diretamente via Maven usando `spark.jars.packages`:

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("IcebergEcommerce")
    .master("local[*]")
    .config("spark.jars.packages",
            "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1")
    .config("spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.catalog.local",
            "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.local.type", "hadoop")
    .config("spark.sql.catalog.local.warehouse", "spark-warehouse/iceberg")
    .getOrCreate()
)
```

!!! note "Download do JAR"
    Na primeira execução, o Spark baixa o JAR `iceberg-spark-runtime-3.5_2.12:1.6.1` (~35 MB)
    do Maven Central. Requer conexão à internet. Nas execuções seguintes, o JAR fica em
    cache em `~/.ivy2/cache`.

!!! note "Sufixo Scala _2.12"
    O PySpark 3.5 é compilado com Scala 2.12. Use sempre o sufixo `_2.12` nas coordenadas Maven.
    Não use `_2.13`.

---

## DDL — Criando Tabelas

As tabelas Iceberg devem ser prefixadas com o nome do catálogo (`local.`):

```sql
CREATE TABLE IF NOT EXISTS local.customer_iceberg (
    customer_id INT,
    name        STRING,
    email       STRING,
    city        STRING
) USING iceberg;

CREATE TABLE IF NOT EXISTS local.product_iceberg (
    product_id INT,
    name       STRING,
    category   STRING,
    price      DOUBLE
) USING iceberg;

CREATE TABLE IF NOT EXISTS local.order_iceberg (
    order_id    INT,
    customer_id INT,
    product_id  INT,
    quantity    INT,
    unit_price  DOUBLE,
    status      STRING,
    order_date  STRING
) USING iceberg;
```

---

## INSERT

```sql
INSERT INTO local.customer_iceberg VALUES
    (1, 'Ana Silva',   'ana@email.com',   'São Paulo'),
    (2, 'Bruno Costa', 'bruno@email.com', 'Rio de Janeiro'),
    (3, 'Carla Lima',  'carla@email.com', 'Curitiba');

INSERT INTO local.product_iceberg VALUES
    (1, 'Notebook',      'Eletronicos', 3500.00),
    (2, 'Mouse',         'Eletronicos',   89.90),
    (3, 'Cadeira Gamer', 'Moveis',      1200.00);

INSERT INTO local.order_iceberg VALUES
    (1, 1, 1, 1, 3500.00, 'pendente', '2024-01-10'),
    (2, 2, 2, 2,   89.90, 'aprovado', '2024-01-11'),
    (3, 3, 3, 1, 1200.00, 'pendente', '2024-01-12');
```

---

## UPDATE

```python
# Atualizar status de um pedido
spark.sql("""
    UPDATE local.order_iceberg
    SET status = 'aprovado'
    WHERE order_id = 1
""")

# Atualizar preço de um produto
spark.sql("""
    UPDATE local.product_iceberg
    SET price = 3299.00
    WHERE product_id = 1
""")
```

---

## DELETE

```python
# Cancelar (remover) um pedido
spark.sql("""
    DELETE FROM local.order_iceberg
    WHERE order_id = 3
""")
```

---

## Snapshots e Histórico

O Iceberg registra cada operação como um **snapshot** imutável. Os metadados ficam em arquivos JSON na pasta `metadata/` da tabela.

### Listar snapshots

```python
spark.sql("SELECT * FROM local.order_iceberg.snapshots").show(truncate=False)
```

### Ver histórico de operações

```python
spark.sql("SELECT * FROM local.order_iceberg.history").show(truncate=False)
```

---

## Time Travel

### Por snapshot ID

```python
first_snapshot_id = (
    spark.sql("SELECT snapshot_id FROM local.order_iceberg.snapshots ORDER BY committed_at")
    .first()["snapshot_id"]
)

spark.read.format("iceberg") \
    .option("snapshot-id", first_snapshot_id) \
    .load("local.order_iceberg") \
    .show()
```

### Por timestamp

```python
spark.read.format("iceberg") \
    .option("as-of-timestamp", "2024-01-10T00:00:00.000") \
    .load("local.order_iceberg") \
    .show()
```

---

## Compatibilidade

| PySpark | iceberg-spark-runtime |
|---|---|
| 3.5.x | `iceberg-spark-runtime-3.5_2.12:1.6.x` |
| 3.4.x | `iceberg-spark-runtime-3.4_2.12:1.6.x` |
| 3.3.x | `iceberg-spark-runtime-3.3_2.12:1.6.x` |

---

## Referências

- [Apache Iceberg — Site Oficial](https://iceberg.apache.org/)
- [Iceberg Spark Getting Started](https://iceberg.apache.org/docs/1.6.1/spark-getting-started/)
- [iceberg-spark-runtime no Maven Central](https://search.maven.org/artifact/org.apache.iceberg/iceberg-spark-runtime-3.5_2.12)
- [Apache Iceberg no GitHub](https://github.com/apache/iceberg)
