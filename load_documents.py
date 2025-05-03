"""essa é uma função que carrega documentos de diferentes tipos de arquivos, como PDF, TXT, CSV, sites e vídeos do YouTube."""

from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader,WebBaseLoader, YoutubeLoader
import os
from time import sleep
import streamlit as st
from fake_useragent import UserAgent


def carrega_pdf(arquivo):
    """Carrega um arquivo PDF."""
    loader = PyPDFLoader(arquivo)
    list_documents = loader.load()
    documents= '\n\n'.join([doc.page_content for doc in list_documents])
    return documents
    

def carrega_txt(arquivo):
    """Carrega um arquivo TXT."""
    loader = TextLoader(arquivo)
    list_documents = loader.load()
    documents= '\n\n'.join([doc.page_content for doc in list_documents])
    return documents

def carrega_csv(arquivo):
    """Carrega um arquivo CSV."""
    loader = CSVLoader(arquivo)
    list_documents = loader.load()
    documents= '\n\n'.join([doc.page_content for doc in list_documents])
    return documents

def carrega_site(arquivo):
    """Carrega um site."""
    documents= ''
    for i in range(10):
        try:
            os.environ['USER_AGENT']=UserAgent().random
            loader = WebBaseLoader(arquivo,raise_for_status=True)
            list_documents = loader.load()
            documents= '\n\n'.join([doc.page_content for doc in list_documents])
            break
        except:
            print(f"Erro ao carregar o site na tentativa {i+1}")
            sleep(3)
            
    if documents == '':
        st.error("Não foi possível carregar o site")
    return documents

def carrega_youtube(video_id):
    """Carrega um vídeo do YouTube."""
    loader = YoutubeLoader.from_youtube_url(video_id,add_video_info=True, language="pt")
    list_documents = loader.load()
    documents= '\n\n'.join([doc.page_content for doc in list_documents])
    return documents