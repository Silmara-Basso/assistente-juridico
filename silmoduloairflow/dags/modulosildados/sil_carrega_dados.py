# Deploy de Aplicação de IA Generativa com Airflow, LLM, RAG, ElasticSearch e Grafana

# Importa as bibliotecas necessárias para manipulação de arquivos, hashing, dados e conexão com Elasticsearch
import os 
import orjsonl
import hashlib
import pandas as pd
from shutil import ExecError
from elasticsearch import Elasticsearch
from modulosildados.silconnection import postgre_connection
from modulosildados.sil_get_dados import sil_extrai_dados

# Função para gerar um ID único para cada documento com base no conteúdo
def sil_gera_id_documento(doc):

    # Combina parte do texto e a questão para criar uma string única
    combined = f"{doc['text'][:10]}-{doc['question']}"
    
    # Gera um hash MD5 a partir da string combinada
    hash_object = hashlib.md5(combined.encode())
    
    # Converte o hash para hexadecimal
    hash_hex = hash_object.hexdigest()
    
    # Extrai os primeiros 8 caracteres do hash como ID do documento
    document_id = hash_hex[:8]
    
    # Retorna o ID do documento gerado
    return document_id

# Função para criar a tabela 'sil_documentos' no banco de dados
def sil_cria_tabela():

    # Estabelece conexão com o banco de dados
    conn, cur = postgre_connection()
    
    try:

        # Query SQL para criar a tabela com colunas para ID, questão e resposta
        create = """
            CREATE TABLE sil_documentos (
                id SERIAL PRIMARY KEY,
                doc_id VARCHAR(10),
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            );
        """

        # Executa a criação da tabela
        cur.execute(create)

    except Exception as e:
        # Em caso de erro, imprime a exceção
        print(e)

        try:

            # Em caso de falha, tenta esvaziar a tabela existente
            create = """
                TRUNCATE TABLE sil_documentos;
            """
            cur.execute(create)

        except Exception as e:
            print(e)

    # Confirma a transação e fecha a conexão
    conn.commit()
    cur.close()
    conn.close()

# Função para inserir dados JSON na tabela 'sil_documentos'
def sil_insere_dados_json():

    # Inicializa uma lista para armazenar os dados a serem inseridos
    allData = []
    
    # Carrega os dados JSONL do arquivo especificado
    silDados = orjsonl.load(f"{os.getcwd()}/dags/dados/dataset1.jsonl")
    
    # Estabelece conexão com o banco de dados
    conn, cur = postgre_connection()

    # Query SQL para inserir dados na tabela
    insert_query = """
    INSERT INTO sil_documentos (doc_id, question, answer) VALUES (%s, %s, %s)
    """

    # Processa cada entrada no JSON para os primeiros 25 registros
    for data in silDados[0:25]:

        # Cria um dicionário com a questão e o texto do documento
        data = {
            "question": str(data['question']),
            "text": str(data['answer'])
        }
        
        # Gera um ID único para o documento
        docId = sil_gera_id_documento(data)
        
        # Adiciona os dados à lista de todos os dados para inserção
        allData.append((str(docId), str(data['question']), str(data['text'])))
            
    try:

        # Constrói a query de inserção com os dados preparados
        args = ','.join(cur.mogrify("(%s,%s,%s)", i).decode('utf-8')
                        for i in allData)
        insert_query = "INSERT INTO sil_documentos (doc_id, question, answer) VALUES" + (args)
        
        # Executa a query de inserção
        cur.execute(insert_query)
        
        # Confirma a transação e exibe mensagem de sucesso
        conn.commit()
        print("Dados Inseridos com Sucesso.")

    except Exception as e:
        # Em caso de erro, exibe a mensagem e desfaz a transação
        print(f"Error: {e}")
        conn.rollback()
    finally:
        # Fecha a conexão com o banco de dados
        cur.close()
        conn.close()
    
    return "Dados JSON Inseridos."

# Função para inserir dados CSV na tabela 'sil_documentos'
def sil_insere_dados_csv():

    # Estabelece conexão com o banco de dados
    conn, cur = postgre_connection()

    # Inicializa uma lista para armazenar os dados
    allData = []
    
    # Carrega os dados do CSV no caminho especificado
    silDados = pd.read_csv(f"{os.getcwd()}/dags/dados/dataset2.csv")

    # Processa as primeiras 25 linhas do CSV
    for index, row in silDados.head(25).iterrows():

        # Cria um dicionário com o título e texto do caso
        data = {
            "question": str(row['case_title']),
            "text": str(row['case_text'])
        }

        # Gera um ID único para o documento
        docId = sil_gera_id_documento(data)

        # Adiciona os dados à lista para inserção
        allData.append((str(docId), data['question'], data['text']))

    try:

        # Constrói a query de inserção para os dados processados
        args = ','.join(cur.mogrify("(%s,%s,%s)", i).decode('utf-8') for i in allData)
        insert_query = "INSERT INTO sil_documentos (doc_id, question, answer) VALUES" + (args)
                
        # Executa a query de inserção
        cur.execute(insert_query)

        # Confirma a transação e exibe mensagem de sucesso
        conn.commit()
        print("Dados Inseridos com Sucesso.")

    except Exception as e:
        # Em caso de erro, exibe a mensagem e desfaz a transação
        print(f"Error: {e}")
        conn.rollback()
    finally:
        # Fecha a conexão com o banco de dados
        cur.close()
        conn.close()

    return "Dados CSV Inseridos."

# Função para criar um índice no Elasticsearch e carregar dados
def sil_cria_indice():

    # Inicializa o cliente Elasticsearch com o endpoint especificado
    # Coloque o hostname do container do ElasticSearch criado no Docker Desktop conforme demonstrado nas aulas
    esClient = Elasticsearch("http://9484b28efcbd:9200")
    
    # Define configurações e mapeamentos para o índice
    indexSettings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "question": {"type": "text"},
                "text": {"type": "text"},
            }
        }
    }

    try:
        
        # Cria o índice no Elasticsearch com as configurações fornecidas
        esClient.indices.create(index=indexName, body=indexSettings)
    except:
        pass  # Ignora erro se o índice já existir

    # Extrai dados para indexação
    data = sil_extrai_dados()
    
    # Define o nome do índice para os dados
    indexName = "silindex"
    
    # Verifica se o índice existe e o exclui se for o caso
    if esClient.indices.exists(index=indexName):
        esClient.indices.delete(index=indexName)

    # Itera sobre os documentos e indexa cada um no Elasticsearch
    for doc in data:
        try:
            esClient.index(index=indexName, document=doc)
        except Exception as e:
            # Exibe mensagem de erro para documentos com problemas
            print(f"error message {e}")
            print(f"error doc: {doc}")

    return "Dados Carregados com Sucesso"
