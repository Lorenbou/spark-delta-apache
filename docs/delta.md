# Delta Lake

## O que é o Delta Lake?

**Delta Lake** é uma camada de armazenamento open-source que traz transações **ACID** ao Apache Spark.  
Desenvolvido pela Databricks e doado à Linux Foundation, é hoje um dos formatos de tabela mais utilizados em arquiteturas Lakehouse.

Funciona sobre sistemas de armazenamento como S3, Azure Data Lake Storage, Google Cloud Storage e sistema de arquivos local.

---

## Funcionalidades Principais

| Funcionalidade | Descrição |
|---|---|
| **Transações ACID** | Atomicidade, Consistência, Isolamento e Durabilidade em operações DML |
| **Transaction Log** | Cada operação é registrada em `_delta_log/` como arquivos JSON |
| **Time Travel** | Leitura de versões anteriores da tabela por número de versão ou timestamp |
| **Schema Enforcement** | Rejeita escritas que violam o schema definido |
| **Schema Evolution** | Permite adicionar colunas com `mergeSchema` |
| **DML completo** | Suporte nativo a `UPDATE`, `DELETE` e `MERGE INTO` |
| **Otimização** | `OPTIMIZE`, `VACUUM`, `Z-ORDER` para performance |

---

## Configuração do SparkSession

```python
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

builder = (
    SparkSession.builder
    .appName("DeltaLakeEcommerce")
    .master("local[*]")
    .config("spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()
```

!!! note "configure_spark_with_delta_pip"
    Ao instalar o `delta-spark` via pip, use sempre `configure_spark_with_delta_pip()`.
    Ele garante que o JAR correto seja carregado a partir do pacote instalado, sem
    necessidade de configurar `spark.jars.packages` manualmente.

---

## DDL — Criando Tabelas

```sql
CREATE TABLE IF NOT EXISTS customer_delta (
    customer_id INT,
    name        STRING,
    email       STRING,
    city        STRING
) USING delta;

CREATE TABLE IF NOT EXISTS product_delta (
    product_id INT,
    name       STRING,
    category   STRING,
    price      DOUBLE
) USING delta;

CREATE TABLE IF NOT EXISTS order_delta (
    order_id    INT,
    customer_id INT,
    product_id  INT,
    quantity    INT,
    unit_price  DOUBLE,
    status      STRING,
    order_date  STRING
) USING delta;
```

A cláusula `USING delta` instrui o Spark a armazenar os dados no formato Delta Lake, criando automaticamente a pasta `_delta_log/` com o histórico de transações.

---

## INSERT

```sql
INSERT INTO customer_delta VALUES
    (1, 'Ana Silva',   'ana@email.com',   'São Paulo'),
    (2, 'Bruno Costa', 'bruno@email.com', 'Rio de Janeiro'),
    (3, 'Carla Lima',  'carla@email.com', 'Curitiba');

INSERT INTO product_delta VALUES
    (1, 'Notebook',      'Eletronicos', 3500.00),
    (2, 'Mouse',         'Eletronicos',   89.90),
    (3, 'Cadeira Gamer', 'Moveis',      1200.00);

INSERT INTO order_delta VALUES
    (1, 1, 1, 1, 3500.00, 'pendente', '2024-01-10'),
    (2, 2, 2, 2,   89.90, 'aprovado', '2024-01-11'),
    (3, 3, 3, 1, 1200.00, 'pendente', '2024-01-12');
```

Cada `INSERT` cria uma nova **versão** no `_delta_log`, registrando quais arquivos Parquet foram adicionados.

---

## UPDATE

```python
# Atualizar status de um pedido
spark.sql("""
    UPDATE order_delta
    SET status = 'aprovado'
    WHERE order_id = 1
""")

# Atualizar preço de um produto
spark.sql("""
    UPDATE product_delta
    SET price = 3299.00
    WHERE product_id = 1
""")
```

O `UPDATE` no Delta Lake é implementado como uma operação de **copy-on-write**: os arquivos Parquet originais não são alterados; novos arquivos são escritos com os dados atualizados e o `_delta_log` registra a mudança.

---

## DELETE

```python
# Cancelar (remover) um pedido
spark.sql("""
    DELETE FROM order_delta
    WHERE order_id = 3
""")
```

Assim como o `UPDATE`, o `DELETE` é implementado como copy-on-write. Os dados removidos ainda existem nos arquivos físicos e podem ser recuperados via **Time Travel** até que `VACUUM` seja executado.

---

## Time Travel

Uma das funcionalidades mais poderosas do Delta Lake é a capacidade de ler versões históricas da tabela.

### Por número de versão

```python
spark.read.format("delta") \
    .option("versionAsOf", 0) \
    .table("order_delta") \
    .show()
```

### Por timestamp

```python
spark.read.format("delta") \
    .option("timestampAsOf", "2024-01-10") \
    .table("order_delta") \
    .show()
```

---

## Histórico de Transações

```python
from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "order_delta")
dt.history().select("version", "timestamp", "operation", "operationParameters").show(truncate=False)
```

Ou via SQL:

```sql
DESCRIBE HISTORY order_delta;
```

Cada linha representa uma operação (CREATE, WRITE, UPDATE, DELETE) com timestamp, métricas e parâmetros.

---

## Compatibilidade

| PySpark | delta-spark |
|---|---|
| 3.5.x | 3.2.x |
| 3.4.x | 2.4.x |
| 3.3.x | 2.2.x |

Consulte sempre a [tabela oficial de compatibilidade](https://docs.delta.io/latest/releases.html).

---

## Referências

- [delta.io — Site Oficial](https://delta.io/)
- [Delta Lake no GitHub](https://github.com/delta-io/delta)
- [Tabela de Releases e Compatibilidade](https://docs.delta.io/latest/releases.html)
- [Delta Lake API Python](https://docs.delta.io/latest/api/python/index.html)
