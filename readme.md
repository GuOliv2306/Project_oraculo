# Projeto Oráculo

Este projeto provê uma interface construída em Streamlit capaz de carregar arquivos de diferentes tipos (PDF, TXT, CSV) ou links de sites e de vídeos do YouTube. O objetivo é disponibilizar o conteúdo processado para consultas por meio de um chat interativo.

[GustaBot](https://gustabot.streamlit.app/)

## Estrutura de Arquivos

- **interface.py**  
  Arquivo principal da aplicação. Define a interface com o Streamlit (abas, botões, campos de interação) e organiza o fluxo de processamento.

- **load_documents.py**  
  Conjunto de funções usadas para carregar e processar os arquivos de diferentes formatos (PDF, TXT, CSV, site, YouTube), retornando o texto pronto para uso pelo modelo.

- **requirements.txt**  
  Lista de dependências necessárias para executar o projeto (Streamlit e bibliotecas relacionadas a processamento de texto, entre outras).

## Fluxo de Funcionamento

1. **Escolher Tipo de Arquivo**  
   Na aba “upload de arquivos”, você seleciona um dos formatos admitidos (site, Youtube, PDF, TXT ou CSV).  
   - Para “site” e “Youtube”, informe o link na caixa de texto.  
   - Para PDF, TXT ou CSV, faça o upload do arquivo no local indicado.

2. **Selecionar Provedor e Modelo**  
   Na aba “seleção de modelo”, é possível escolher:  
   - Provedor (ex.: `OPENAI`, `Groq`).  
   - Modelo específico (um dos disponíveis no provedor).  
   - A respectiva API key de acesso (caso necessária).

3. **Carregar Modelo**  
   Ao clicar no botão “Carregar modelo”, o projeto:  
   - Carrega e processa o arquivo/link escolhido (via `load_documents.py`).  
   - Formata essas informações para o `system_message`.  
   - Configura o pipeline de chat, vinculando as mensagens do usuário ao conteúdo carregado.

4. **Limpar Memória**  
   Esse botão reinicia o histórico de conversas para começar nova interação do zero.

5. **Campo de Chat**  
   Logo abaixo, há um componente de chat. Ao inserir texto (a pergunta/dúvida) e enviar, o modelo responde com base no conteúdo que foi carregado.

## Como Executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute o projeto:
   ```bash
   streamlit run interface.py
   ```
