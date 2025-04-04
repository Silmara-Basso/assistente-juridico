# Deploy de Aplicação de IA Generativa com Airflow, LLM, RAG, ElasticSearch e Grafana

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import timedelta

# Importa funções personalizadas para manipulação de dados do módulo 'modulosildados'
from modulosildados.sil_carrega_dados import sil_cria_tabela, sil_insere_dados_json, sil_insere_dados_csv, sil_cria_indice

# Define argumentos padrão para as tarefas do DAG
defaultArguments = {
    "owner": "Silmara Basso",   # Nome do proprietário do DAG
    "start_date": days_ago(1),         # Define a data de início como um dia atrás
    "retries": 1,                      # Número de tentativas de reexecução em caso de falha
    "retry_delay": timedelta(hours=1)  # Intervalo de uma hora entre tentativas de reexecução
}

# Cria a DAG com o nome 'Carrega_Dados_LLM'
dag = DAG(
    "Carrega_Dados_LLM",
    default_args=defaultArguments,                       # Usa os argumentos padrão definidos acima
    schedule_interval="0 0 * * *",                       # Define a execução diária à meia-noite
    description="Carrega os dados para o módulo de RAG"  # Descrição da DAG
)

# Define a tarefa para criar a tabela, usando a função 'sil_cria_tabela' do módulo
sil_tarefa_cria_tabela = PythonOperator(
    task_id="tarefa_cria_tabela",     # Identificador único da tarefa
    python_callable=sil_cria_tabela,  # Função Python a ser executada
    dag=dag                           # DAG a qual a tarefa pertence
)

# Define a tarefa para carregar dados JSON, usando a função 'sil_insere_dados_json'
sil_tarefa_carrega_json = PythonOperator(
    task_id="tarefa_carrega_json",          # Identificador único da tarefa
    python_callable=sil_insere_dados_json,  # Função Python a ser executada
    dag=dag                                 # DAG a qual a tarefa pertence
)

# Define a tarefa para carregar dados CSV, usando a função 'sil_insere_dados_csv'
sil_tarefa_carrega_csv = PythonOperator(
    task_id="tarefa_carrega_csv",          # Identificador único da tarefa
    python_callable=sil_insere_dados_csv,  # Função Python a ser executada
    dag=dag                                # DAG a qual a tarefa pertence
)

# Define a tarefa para criar o índice, usando a função 'sil_cria_indice'
sil_tarefa_cria_indice = PythonOperator(
    task_id="tarefa_cria_indice",     # Identificador único da tarefa
    python_callable=sil_cria_indice,  # Função Python a ser executada
    dag=dag                           # DAG a qual a tarefa pertence
)

# Define a ordem de execução das tarefas na DAG
# Primeiro cria a tabela, depois carrega os dados JSON, seguido pelos dados CSV, e por último cria o índice no ElasticSearch
# Isso define a estratégia de RAG
sil_tarefa_cria_tabela >> sil_tarefa_carrega_json >> sil_tarefa_carrega_csv >> sil_tarefa_cria_indice




