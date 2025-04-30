import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

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



def carrega_modelo(provedor,modelo,api_key):
    chat=CONFIG_MODELS[provedor]['chat'](model=modelo,api_key=api_key)
    st.session_state['chat']=chat


def pagina():
    st.header("🤖Bem vindo ao GustaBot",divider=True)
    st.write("Welcome to my bot!")

    chat_model=st.session_state.get("chat")
    memoria= st.session_state.get("memoria", MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat=st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    user_input = st.chat_input("Pergunte algo")
    if user_input:
        chat=st.chat_message("user")
        chat.markdown(user_input)

        chat=st.chat_message("ai")
        resposta= chat.write_stream(chat_model.stream(user_input))
        
        memoria.chat_memory.add_user_message(user_input)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria']=memoria

def sidebar():
    tabs=st.tabs(["upload de arquivos", "seleção de modelo"])
    with tabs[0]:
        tipo_arquivo=st.selectbox("Selecione o tipo de arquivo", TIPO_ARQUIVOS)
        if tipo_arquivo== "site":
            link=st.text_input("Cole o link aqui")
        if tipo_arquivo== "Youtube":
            link=st.text_input("Cole o link aqui")
        if tipo_arquivo== "pdf":
            arquivo=st.file_uploader("Selecione o arquivo aqui", type=["pdf"])
        if tipo_arquivo== "txt":
            arquivo=st.file_uploader("Selecione o arquivo aqui", type=["txt"])
        if tipo_arquivo== "csv":
            arquivo=st.file_uploader("Selecione o arquivo aqui", type=["csv"])
    with tabs[1]:
        provedor=st.selectbox("Selecione o provedor", CONFIG_MODELS.keys())
        modelo=st.selectbox("Selecione o modelo", CONFIG_MODELS[provedor]['modelo'])
        api_key=st.text_input(f"Insira a API key do provedor {provedor}", type="password",value=st.session_state.get(f"{provedor}_api_key", ""))
        st.session_state[f"{provedor}_api_key"]=api_key

        if st.button("Carregar modelo", use_container_width=True):
            chat=carrega_modelo(provedor,modelo,api_key)
            


def main():
    pagina()
    with st.sidebar:
        sidebar()

if __name__ == "__main__":
    main()