# **Projeto Final de Aprendizagem Supervisionada — ReclamaRank**

**Nome Provisório:** ReclamaRank

**Objetivo:**  
O projeto faz parte da disciplina de Aprendizagem Supervisionada do curso de Ciência de Dados para Negócios (UFPB). O objetivo é desenvolver uma solução real e inovadora de Machine Learning, testando diferentes modelos supervisionados.  
No ReclamaRank, o desafio é calcular a **probabilidade de uma reclamação feita no site Consumidor.gov ser resolvida ou não** e **ranqueá-las por urgência**, oferecendo prioridade de atendimento baseada nessa probabilidade.

**Coleta e Modelagem de Dados:**  
- Fonte: Site [Consumidor.gov](https://www.consumidor.gov.br/)  
- Coleta: API pública que retorna o conteúdo HTML das reclamações.  
- Extração: Utilização do **BeautifulSoup** para extrair as seguintes informações:  
  - `company_name`
  - `status`
  - `date`
  - `report`
  - `company_response`
  - `response_date`
  - `rating_score`
  - `consumer_written_evaluation`
- Tratamento: Limpeza e modelagem dos dados, com pré-processamento textual.

**Modelos Testados:**  
- Regressão Logística 
- Rede Neural com Tensorflow

**Resultado:**  

O modelo com melhor desempenho foi a **Rede Neural**, considerado o modelo base para o sistema.

**<span style='color:red'>OBSERVAÇÃO**</span>

> Ao finalizar o desenvolvimento, percebi que apareceu uma nova label para `status`. Seria no caso: 'Não avaliado pelo consumidor', que indica que o cidadão não atualizou o status da reclamação.

Retirando essa label, os dados ficam com um balanceamento de cerca 50/50, além de reduzir o tamanho do banco de dados, o que talvez permita o upload para o GitHub. Não tinha percebido antes pois a primeira versão utilizava apenas 13500 linhas, e essas amostras não foram extraídas. Em breve atualizarei removendo essas labels.

**Desenvolvimento Futuro:**  
- **Banco de Dados**: Modelagem de três entidades principais:
  - Reclamações
  - Usuários
  - Empresas
- **Aplicativo Streamlit** com três áreas:
  - **Usuário**: 
    - Consultar informações e prioridades de suas reclamações
    - Registrar novas reclamações
    - Visualizar todas as reclamações
  - **Servidor** (Equipe Consumidor.gov):
    - Acesso a todas as reclamações cadastradas
  - **Empresa**:
    - Visualizar reclamações recebidas
    - Responder reclamações
    - *(Em desenvolvimento)* Sistema de predição da nota de atendimento
    - *(Em desenvolvimento)* Sugestor automático de respostas baseado em similaridade textual

**Ferramentas Utilizadas:**  
- Python
- Pandas
- Streamlit
- Scikit-Learn
- TensorFlow
- BeautifulSoup

**Autor:**  
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/pedrohmvv">
        <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/139015105?v=4" width="100px;" alt=""/>
        <br />
        <sub><b>Pedro Henrique</b></sub>
      </a>
      <br />
      <a href="https://github.com/pedrohmvv" target="_blank">
        <img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" alt="LinkedIn" style="padding-top: 10px;">
      </a>
    </td>
  </tr>
</table>
