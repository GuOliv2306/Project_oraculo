"""essa é uma função que carrega documentos de diferentes tipos de arquivos, como PDF, TXT, CSV, sites e vídeos do YouTube."""

from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader,WebBaseLoader, YoutubeLoader
import os


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

def carrega_site(url):
    """Carrega um site."""
    loader = WebBaseLoader(url)
    list_documents = loader.load()
    documents= '\n\n'.join([doc.page_content for doc in list_documents])
    return documents

def carrega_youtube(video_id):
    """Carrega um vídeo do YouTube."""
    loader = YoutubeLoader.from_youtube_url(video_id,add_video_info=True, language="pt")
    list_documents = loader.load()
    documents= '\n\n'.join([doc.page_content for doc in list_documents])
    return documents