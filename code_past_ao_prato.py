#importa os pacotes necessários
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define a lista de CNAE para o exercício
lista_cnae = [1011201,1011205,1013901,1013902]

# Definindo a composição da URL para acesso ao banco de dados
url='https://compras.dados.gov.br/'
modulo = 'fornecedores/v1/'
metodo = 'fornecedores'
formato = '.csv'
parametro1 = 'id_cnae='

# loop de aquisição de dados
dados = pd.DataFrame()                                          # Define uma dataframe vazia para salvar os dados
dados = pd.DataFrame()                                          # Define uma dataframe vazia para salvar os dados
for i in lista_cnae:                                            # Define o loop que irá percorrer a lista de CNAEs
    try:
        fonte = url+modulo+metodo+formato+'?'+parametro1+str(i) # Cria o link de acesso para aquisição dos dados na API
        tmp = pd.read_csv(fonte)                                # Cria uma DataFrame temporária a partir do link
        dados = pd.concat([dados,tmp], axis=0)                  # Concatena os dados adiquiridos em dados
    except Exception as e:
        dados=0
        with open("WARNING-READ-ME-DELETE-ME.txt", "w") as file:
            file.write("Error: "+str(e)+'\n')                       # Escreve o tipo de erro
            file.write("Data aquisition problem.\n")
            file.write("Delete this Warning and try Again")          # Escreve para aguardar e tentar novamente mais tarde
        print("Error: "+str(e)+'\n')
dados.to_csv('dados.csv')                                       # Salva os dados concatenados em um arquivo CSV

# Cria uima dataframe de trabalho a partir dos dados salvos
df = pd.read_csv('dados.csv')

# dicionario com o nome dos Estados Brasileiros e Suas Siglas
estados = {'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 'BA': 'Bahia',
           'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás',
           'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul', 'MG': 'Minas Gerais',
           'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná', 'PE': 'Pernambuco', 'PI': 'Piauí',
           'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RS': 'Rio Grande do Sul',
           'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina', 'SP': 'São Paulo',
           'SE': 'Sergipe', 'TO': 'Tocantins'}

# Cria uma coluna com os nomes dos estados para melhor visualização gráfica
df['Estado'] = df['UF'].replace(estados)

# Cria a figura com o gráfico em barras
fig, ax = plt.subplots(figsize=(10,5),dpi=150)                                                  # Define o tamanho e o DPI da figura
df_plot = df[['Id','Estado']].groupby('Estado').count().sort_values(by=('Id')).reset_index()    # Cria a dataframe por agrupamento para o plot
sns.barplot(data=df_plot,y='Estado',x='Id',order=df_plot['Estado'][::-1])                       # Com Seaborn realiza o plot
plt.gca().xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.5)              # Cria linhas crecejadas no gráfico
plt.title('Fornecedores de Carne por Estado')                                                   # Define o título da figura
plt.xlabel('Número de fornecedores por Estado')                                                 # Define o titulo do eixo X
plt.ylabel('Estado da federação')                                                               # Define o título do Eixo Y
ax.set_xticks(range(0, 45, 5))                                                                  # Divide o eixo x a cada 5
plt.savefig('fornecedores_estados.png', bbox_inches='tight')                                    # Sava o arquivo
