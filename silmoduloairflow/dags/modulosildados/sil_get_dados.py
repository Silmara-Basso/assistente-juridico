# Deploy de Aplicação de IA Generativa com Airflow, LLM, RAG, ElasticSearch e Grafana

# Importa a função postgre_connection para estabelecer conexão com o banco de dados PostgreSQL
from modulosildados.silconnection import postgre_connection

# Função para extrair todos os dados da tabela 'sil_documentos' no banco de dados
def sil_extrai_dados():
    
    # Estabelece conexão com o banco de dados e cria um cursor
    conn, cur = postgre_connection()

    # Define a query SQL para selecionar todos os registros da tabela
    getAll = "SELECT * FROM sil_documentos"
    
    # Executa a query no banco de dados
    cur.execute(getAll)
    
    # Armazena todos os resultados da consulta em uma lista
    results = cur.fetchall()
    
    # Inicializa uma lista para armazenar todos os documentos extraídos
    allDocuments = []

    # Itera sobre cada resultado e adiciona o documento à lista
    for result in results:
        allDocuments.append(result)

    # Fecha o cursor e a conexão com o banco de dados
    cur.close()
    conn.close()

    # Retorna a lista com todos os documentos extraídos
    return allDocuments
