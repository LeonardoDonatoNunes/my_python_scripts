# Para executar o python, primeiro executar as funções abaixo:
  
  # Executar no console do R
    # install.packages('reticulate')
    # library(reticulate)
    # use_virtualenv("RETICULATE_PYTHON")
    # use_python("C:\\Users\\user\\AppData\\Local\\R-MINI~1\\envs\\R-RETI~1\\python.exe")
    
  # Para instalar bibliotecas python que não estão instaladas no ambiente virtual
  
    # py_install("pandas") 
    # py_install("requests") 
    # py_install("json") 
    # py_install("pymongo") 
    # py_install("pprint") 
    # py_install("datetime") 
    
# Para sair do ambiente python basta pressionar Esc no pronpt

# Importa os pacotes python
import pandas as pd
import requests
import json
from pymongo import MongoClient
import pprint
import datetime


        # Os dados para o exemplo foram obtidos do [Portal Brasileiro de Dados Abertos](https://dados.gov.br/).
        # 
        # Nome do conjunto de dados: [Vendas de veículos pelas concessionárias - Automóveis](https://dados.gov.br/dataset/7384-vendas-de-veiculos-pelas-concessionarias-automoveis)
        # 
        # Conceito: Valor da produção de veículos automotores no País. Refletem o desempenho das vendas das empresas associadas a(o): estoque e venda de veículos pelas concessionárias produção e vendas de veículos e congêneres produção e vendas de motociclos
        



# Requisição GET para obter os dados no formato JSON.


r = requests.get(url='https://api.bcb.gov.br/dados/serie/bcdata.sgs.7384/dados?formato=json')


# Visualizar os primeiros 5 documentos do arquivo
r.json()[0:5]

# Cria a conexao com o MongoDB
con = MongoClient('localhost', 27017)

# Lista os BD's 
con.list_database_names()

# Deleta o BD 'vendas_automoveis' que será criado novamente no próximo bloco.
con.drop_database('vendas_automoveis')
con.list_database_names()


# Cria o BD e a coleção para inserir os dados no BD
novo_bd = con['vendas_automoveis']
nova_colecao = novo_bd['vendas']
con.list_database_names()

# Conecta novamente o BD, a coleção vendas e insere os dados JSON coletados no BD.
db = con['vendas_automoveis']

# Carrega o bd
vendas = db.vendas
resultado = vendas.insert_many(r.json())


# Busca os dados do BD e configura os campos de data como datetime e o de valor como número.
df = pd.DataFrame(list(vendas.find()))
df['data'] = pd.to_datetime(df['data'], dayfirst=True)
df['valor'] = pd.to_numeric(df['valor'])

# informações do data frame
df.info()

# Primeiras linhas do data frame
df.head()
