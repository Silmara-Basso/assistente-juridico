# Deploy de Aplicação de IA Generativa com Airflow, LLM, RAG, ElasticSearch e Grafana

# Importa a biblioteca Elasticsearch para interagir com o serviço Elasticsearch
from elasticsearch import Elasticsearch

# Função para estabelecer a conexão com o cliente Elasticsearch
def getEsClient():

    # Inicializa um cliente Elasticsearch apontando para o serviço na URL especificada
    # Edite a linha abaixo com o nome do hostname do container do ElasticSearch conforme mostrado nas aulas
    esClient = Elasticsearch("http://9484b28efcbd:9200")
    
    # Retorna o cliente Elasticsearch para uso em outras funções
    return esClient 

# Função para realizar uma consulta no Elasticsearch
def elasticSearch(esClient, query, indexName):

    # Define a consulta de busca com um limite de 5 resultados
    searchQuery = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {

                        # Define a consulta usando o parâmetro 'query' fornecido
                        "query": query,

                        # Define os campos a serem pesquisados com ponderação maior para o campo 'question'
                        "fields": ["question^2", "text"],
                        
                        # Tipo de pesquisa configurado para usar os 'best_fields' para relevância
                        "type": "best_fields"
                    }
                }
            }
        }
    }

    # Executa a consulta no índice especificado usando o cliente Elasticsearch
    response = esClient.search(index=indexName, body=searchQuery)
    
    # Inicializa uma lista para armazenar os documentos resultantes
    resultDocs = []

    # Itera sobre os resultados da consulta para extrair o conteúdo dos documentos
    for hit in response['hits']['hits']:
        
        # Adiciona o conteúdo do documento à lista de resultados
        resultDocs.append(hit['_source'])

    # Retorna a lista de documentos encontrados
    return resultDocs
