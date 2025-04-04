# assistente-juridico
Assistente Jurídico usando IA Generativa com Airflow, LLM, RAG, ElasticSearch e Grafana


# Instruções Para Execução do Projeto

1- Crie sua conta no HuggingFace, acesse o site abaixo e crie sua chave gratuita (token) para a API:

https://huggingface.co/settings/tokens

2- Edite o arquivo abaixo e altere o valor de HUGGINGFACE_KEY para sua chave.

docker-compose.yaml

`    environment:`

`      - HUGGINGFACE_KEY=<coloque-aqui-sua-chave> `

3- Crie os containers:

`docker compose up --build -d`

Ajuste o nome do host do Elasticserch abrindo o terminal do container
`bash`
`hostname`

Altere o hostname do ElasticSearch nos arquivos silelasticSearch.py e sil_carrega_dados.py

5- Abra o navegador e acesse o Airflow para ativar a DAG:

localhost:8080

username: airflow
password: airflow

6- Abra o navegador e acesse a app web para interagir com o LLM (espere alguns segundos até o ElasticSearch finalizar a indexação):

localhost:8501

![interface](/images/Dag.png)

Execução da Dag
![interface](/images/dag2.png)

Exemplos de perguntas:

- Can the landlord avoid liability for breaching this obligation if the state of disrepair is caused by the tenant's actions?
- Why did the plaintiff wait seven months to file an appeal?
- Can you provide more details on the clarification provided in Note 1?

![interface](/images/app.png)


7- Abra o navegador e acesse o Grafana para carregar o dashboard.

localhost:3000

username: admin
password: admin

Steps para configuração:

- Troque a senha
- Cria a conexão (New Data Source) com o banco Postgre do Airflow ( o correto é ter outra maquina e banco para esta base, mas devido ao consumo de recursos optei por usar o do Airflow)
- Carregue o json que esta dentro da pasta sildashboardgrafana
- Edite e salve cada uma das visualizações para atualizar os dados

Agora é só enviar perguntas na app de IA Generativa e monitorar pelo Dashboard do Grafana.


![interface](/images/Grafana.png)
