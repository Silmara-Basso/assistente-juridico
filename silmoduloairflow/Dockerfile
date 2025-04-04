# Deploy de Aplicação de IA Generativa com Airflow, LLM, RAG, ElasticSearch e Grafana

# Define a imagem base como a versão 2.10.2 do Apache Airflow
FROM apache/airflow:2.10.2

# Define o usuário como 'airflow' para garantir que o Airflow seja executado com permissões adequadas
USER airflow

# Define a variável de ambiente para o diretório principal do Airflow
ENV AIRFLOW_HOME=/opt/airflow/silmoduloairflow

# Define o diretório de trabalho no contêiner como o diretório principal do Airflow
WORKDIR /opt/airflow/silmoduloairflow

# Copia o arquivo requirements.txt do host para o diretório de trabalho no contêiner
COPY requirements.txt /opt/airflow/silmoduloairflow/requirements.txt

# Executa o comando para instalar o Apache Airflow e as dependências listadas em requirements.txt
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
