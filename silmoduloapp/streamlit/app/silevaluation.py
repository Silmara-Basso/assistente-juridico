# Deploy de Aplicação de IA Generativa com Airflow, LLM, RAG, ElasticSearch e Grafana

# Imports
import pandas as pd

# Função para calcular a taxa de acerto (hit rate)
def hit_rate(relevance_total):

    # Inicializa o contador de acertos
    cnt = 0

    # Itera por cada linha para contar casos relevantes (True)
    for line in relevance_total:
        if True in line:
            cnt += 1

    # Retorna a taxa de acerto, dividindo o número de acertos pelo total de linhas
    return cnt / len(relevance_total)

# Função para calcular a média recíproca dos rankings (MRR - Mean Reciprocal Rank)
def mrr(relevance_total):

    # Inicializa a variável de pontuação
    score = 0

    # Itera sobre cada linha de relevância
    for line in relevance_total:

        # Itera sobre cada posição de ranking dentro da linha
        for rank in range(len(line)):

            # Verifica se a posição atual é relevante (True)
            if line[rank] == True:

                # Atualiza a pontuação com o valor recíproco do ranking
                score += 1 / (rank + 1)

                # Sai do loop interno ao encontrar a primeira posição relevante
                break

    # Retorna a média recíproca dos rankings, dividindo a pontuação total pelo número de linhas
    return score / len(relevance_total)

# Função para avaliar uma função de busca com base em dados históricos de verdade básica (ground truth)
def evaluate(search_function):

    # Lê o arquivo CSV com o dataset de verdade básica (ground truth)
    ground_truth = pd.read_csv("streamlit/app/dadosHistoricos/dataset.csv")

    # Converte os dados para um formato de lista de dicionários
    ground_truth = ground_truth.to_dict(orient="records")

    # Inicializa uma lista para armazenar a relevância de cada consulta
    relevance_total = []

    # Itera sobre cada consulta no ground truth
    for q in ground_truth:

        # Obtém o ID do documento esperado
        doc_id = q['document']

        # Executa a função de busca com a consulta atual
        results = search_function(q)

        # Cria uma lista de relevância, marcando True para documentos relevantes
        relevance = [d['doc_id'] == doc_id for d in results]
        
        # Adiciona a lista de relevância para a consulta atual
        relevance_total.append(relevance)
    
    # Retorna um dicionário com as métricas de avaliação (hit rate e MRR)
    return {
        "hit_rate": hit_rate(relevance_total),
        "mrr": mrr(relevance_total)
    }
