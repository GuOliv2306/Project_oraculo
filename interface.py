import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from load_documents import *
import tempfile, os
from langchain.prompts import ChatPromptTemplate

MEMORIA=ConversationBufferMemory()


TIPO_ARQUIVOS=[
    "site",
    "Youtube",
    "pdf",
    "txt",
    "csv",
]

CONFIG_MODELS = {
    'OPENAI': {'modelo': ["o4-mini-2025-04-16", "gpt-4.1-mini-2025-04-14", "gpt-4.1-2025-04-14"], 'chat': ChatOpenAI},
    'Groq': {'modelo': ["gemma2-9b-it", "llama-3.3-70b-versatile", "llama-guard-3-8b"], 'chat': ChatGroq}
}

def carrega_documentos(tipo_arquivo, arquivo):
    if tipo_arquivo == "site":
        documents = carrega_site(arquivo)
    elif tipo_arquivo == "Youtube":
        documents = carrega_youtube(arquivo)
    elif tipo_arquivo == "pdf":
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(arquivo.read())
            temp_file_path = temp_file.name
            documents = carrega_pdf(temp_file_path)
    elif tipo_arquivo == "txt":
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(arquivo.read())
            temp_file_path = temp_file.name
            documents = carrega_txt(temp_file_path)
    elif tipo_arquivo == "csv":
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(arquivo.read())
            temp_file_path = temp_file.name
            documents = carrega_csv(temp_file_path)
    else:
        st.error("Tipo de arquivo não suportado.")
        return None
    
    return documents



def carrega_modelo(provedor,modelo,api_key,tipo_arquivo=None,arquivo=None):
    documents=carrega_documentos(tipo_arquivo,arquivo)
    
    # Escape das chaves no conteúdo dos documentos
    if documents:
        documents_escaped = str(documents).replace("{", "{{").replace("}", "}}")
    else:
        documents_escaped = ""

    system_message = '''Você é um assistente amigável chamado GustaBot.
    Você possui acesso às seguintes informações vindas 
    de um documento {0}: 

    ####
    {1}
    ####

    Utilize as informações fornecidas para basear as suas respostas.

    Sempre que houver $ na sua saída, substita por S.

    Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" 
    sugira ao usuário carregar novamente o Oráculo!'''.format(tipo_arquivo, documents_escaped)

    # Alterar o template para não usar placeholder
    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('human', "{input}")  # Removido placeholder de chat_history
    ])

    chat = CONFIG_MODELS[provedor]['chat'](model=modelo, api_key=api_key)

    chain=template | chat

    st.session_state['chain'] = chain

def pagina():
    st.header("🤖Bem vindo ao GustaBot",divider=True)

    chain_model=st.session_state.get("chain")
    if chain_model is None:
        st.info("Por favor, carregue um modelo primeiro!")
        st.stop()
    
    memoria= st.session_state.get("memoria", MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat=st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    user_input = st.chat_input("Pergunte algo")
    if user_input:
        chat=st.chat_message("user")
        chat.markdown(user_input)

        chat=st.chat_message("ai")
        # Remover o parâmetro chat_history
        resposta= chat.write_stream(chain_model.stream({"input": user_input}))
        
        memoria.chat_memory.add_user_message(user_input)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria']=memoria

def sidebar():
    tabs=st.tabs(["upload de arquivos", "seleção de modelo"])
    with tabs[0]:
        tipo_arquivo=st.selectbox("Selecione o tipo de arquivo", TIPO_ARQUIVOS)
        if tipo_arquivo== "site":
            arquivo=st.text_input("Cole o link aqui")
        elif tipo_arquivo== "Youtube":
            arquivo=st.text_input("Cole o link aqui")
        elif tipo_arquivo== "pdf":
            arquivo=st.file_uploader("Selecione o arquivo aqui", type=["pdf"])
        elif tipo_arquivo== "txt":
            arquivo=st.file_uploader("Selecione o arquivo aqui", type=["txt"])
        elif tipo_arquivo== "csv":
            arquivo=st.file_uploader("Selecione o arquivo aqui", type=["csv"])
    with tabs[1]:
        provedor=st.selectbox("Selecione o provedor", CONFIG_MODELS.keys())
        modelo=st.selectbox("Selecione o modelo", CONFIG_MODELS[provedor]['modelo'])
        api_key=st.text_input(f"Insira a API key do provedor {provedor}", type="password",value=st.session_state.get(f"{provedor}_api_key", ""))
        st.session_state[f"{provedor}_api_key"]=api_key

    if st.button("Carregar modelo", use_container_width=True):
        chat=carrega_modelo(provedor,modelo,api_key,tipo_arquivo,arquivo)

    if st.button("Limpar memória", use_container_width=True):
        st.session_state['memoria']=MEMORIA
        


def main():
    with st.sidebar:
        sidebar()
    pagina()
    

if __name__ == "__main__":
    main()