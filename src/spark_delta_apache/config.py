from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
import logging

def get_spark_delta_session(app_name="DeltaLakeApp"):
    """
    Configura uma SparkSession otimizada para Delta Lake.
    """
    builder = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.warehouse.dir", "/app/spark-warehouse")
        .config("spark.ui.showConsoleProgress", "false")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()

def get_spark_iceberg_session(app_name="IcebergApp"):
    """
    Configura uma SparkSession otimizada para Apache Iceberg.
    """
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1")
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.local.type", "hadoop")
        .config("spark.sql.catalog.local.warehouse", "/app/spark-warehouse/iceberg")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )

def setup_logging(spark_context=None):
    """
    Configura o logging para evitar verbosidade excessiva.
    """
    # Silencia o log4j do Spark (Internal)
    logging.getLogger("py4j").setLevel(logging.ERROR)
    
    if spark_context:
        spark_context.setLogLevel("ERROR")
