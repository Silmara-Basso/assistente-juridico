# Deploy de Aplicação de IA Generativa com Airflow, LLM, RAG, ElasticSearch e Grafana

# Importa a biblioteca psycopg2 para conectar-se ao banco de dados PostgreSQL
import psycopg2

# Importa RealDictCursor para retornar resultados como dicionários, permitindo acessar dados pelo nome da coluna
from psycopg2.extras import RealDictCursor

# Função para estabelecer conexão com o banco de dados PostgreSQL
def postgre_connection():

    # Cria a conexão com o banco de dados PostgreSQL, especificando nome do banco, usuário, senha, host e porta
    conn = psycopg2.connect(
        dbname="airflow",   # Nome do banco de dados
        user="airflow",     # Nome de usuário do banco
        password="airflow", # Senha do banco de dados
        host="postgres",    # Host onde o banco de dados está localizado
        port="5432"         # Porta usada para conexão
    )

    # Cria um cursor para executar comandos SQL, usando RealDictCursor para retornar os resultados como dicionários
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Retorna a conexão e o cursor para uso nas operações de banco de dados
    return conn, cur
