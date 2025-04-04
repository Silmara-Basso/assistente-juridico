# Deploy de Aplicação de IA Generativa com Airflow, LLM, RAG, ElasticSearch e Grafana

# Imports
import time
import streamlit as st
from app.silelasticSearch import getEsClient, elasticSearch
from app.silllm import sil_gera_documento_id, sil_query, sil_captura_user_input, sil_captura_user_feedback
from app.silevaluation import evaluate

# Função principal
def main():

    # Configurações da página
    st.set_page_config(page_title="Projeto LLM", page_icon=":100:", layout="wide")

    # Barra lateral para configurações e informações da app
    st.sidebar.title("Testando LLM com Airflow")
    st.sidebar.subheader("Silmara Basso")
    st.sidebar.write("Deploy de Aplicação de IA Generativa com Airflow, LLM, RAG, ElasticSearch e Grafana")
    st.sidebar.markdown("---")

    # Cabeçalho principal
    st.title("Assistente Jurídico")
    st.write("Faça perguntas e receba respostas precisas sobre documentos jurídicos.")
    st.write("As perguntas devem ser e inglês pois o RAG foi criado com dados em inglês.")

    # Inicializando variáveis de sessão
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'docId' not in st.session_state:
        st.session_state.docId = None
    if 'userInput' not in st.session_state:
        st.session_state.userInput = ""
    if 'feedbackSubmitted' not in st.session_state:
        st.session_state.feedbackSubmitted = False

    # Caixa de entrada de texto
    userInput = st.text_input("Digite sua pergunta:")

    # Nome do índice do ElasticSearch
    indexName = "silindex"

    # Cria conexão cliente ao ElasticSearch (nosso módulo de RAG)
    try:
        esClient = getEsClient()
    except Exception as e:
        print(e)
        st.error("O ElasticSearch ainda está sendo carregado. Atualize a página e tente novamente.")

    # Botão de envio para processar a pergunta
    if st.button("Enviar"):
        if userInput:
            with st.spinner("Preparando a Resposta..."):
                try:
                    # Recupera documentos contextuais
                    ragOutputs = elasticSearch(esClient, userInput, indexName)
                    context = "".join([output['answer'] for output in ragOutputs])

                    # Avalia a resposta
                    evaluateResult = evaluate(lambda q: elasticSearch(esClient, userInput, indexName))

                    # Realiza a consulta ao modelo de linguagem
                    output, responseTime = sil_query({"inputs": {"question": userInput.replace("'", ""), "context": context}})
                    
                    result = output['answer'].replace("'", "")

                    # Gera um ID de documento
                    docId = sil_gera_documento_id(userInput, result)
                    
                    # Captura entrada do usuário
                    sil_captura_user_input(
                        docId, 
                        userInput.replace("'", ""), 
                        result, 
                        output['score'], 
                        responseTime,
                        evaluateResult['hit_rate'], 
                        evaluateResult['mrr']
                    )

                    # Atualiza o estado da sessão com o resultado
                    st.session_state.result = result
                    st.session_state.docId = docId
                    st.session_state.userInput = userInput.replace("'", "")
                    st.session_state.feedbackSubmitted = False

                except Exception as e:
                    print(e)
                    st.error("Erro ao processar a consulta. Verifique o ElasticSearch e tente novamente.")
        else:
            st.warning("Digite sua pergunta para continuar.")

    # Exibindo o resultado da consulta
    if st.session_state.result:
        st.subheader("Resposta:")
        st.write(st.session_state.result)

        # Seção de feedback de satisfação
        if not st.session_state.feedbackSubmitted:
            st.write("Você está satisfeito com a resposta?")
            feedback_col1, feedback_col2 = st.columns(2)
            with feedback_col1:
                if st.button("Satisfeito"):
                    sil_captura_user_feedback(st.session_state.docId, st.session_state.userInput, st.session_state.result, True)
                    st.session_state.feedbackSubmitted = True
                    st.success("Feedback registrado: Satisfeito")
            with feedback_col2:
                if st.button("Não Satisfeito"):
                    sil_captura_user_feedback(st.session_state.docId, st.session_state.userInput, st.session_state.result, False)
                    st.session_state.feedbackSubmitted = True
                    st.warning("Feedback registrado: Não Satisfeito")

if __name__ == "__main__":
    main()
