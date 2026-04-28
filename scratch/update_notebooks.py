import json
import os

def update_notebook(path, old_code_prefix, new_code):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            if old_code_prefix in source:
                cell['source'] = [line + "\n" for line in new_code.split("\n")]
                # Remove trailing newline from last line if it exists
                if cell['source'][-1] == "\n":
                    cell['source'].pop()
                break
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

# Delta Lake Notebook
delta_new_code = """import sys
import os
# Adiciona o diretório src ao path para permitir importação do pacote local
sys.path.append(os.path.abspath("../src"))

from spark_delta_apache import get_spark_delta_session, setup_logging

# Configurar logging e criar SparkSession via pacote local
setup_logging()
spark = get_spark_delta_session("DeltaLakeEcommerce")
spark"""

update_notebook('notebooks/delta_lake.ipynb', 'from delta import configure_spark_with_delta_pip', delta_new_code)

# Iceberg Notebook
iceberg_new_code = """import sys
import os
# Adiciona o diretório src ao path para permitir importação do pacote local
sys.path.append(os.path.abspath("../src"))

from spark_delta_apache import get_spark_iceberg_session, setup_logging

# Configurar logging e criar SparkSession via pacote local
setup_logging()
spark = get_spark_iceberg_session("IcebergEcommerce")
spark"""

update_notebook('notebooks/apache_iceberg.ipynb', 'org.apache.iceberg:iceberg-spark-runtime', iceberg_new_code)
