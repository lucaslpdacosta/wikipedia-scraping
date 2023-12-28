import requests
from bs4 import BeautifulSoup
from collections import Counter
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
#from sklearn.preprocessing import normalize

######################################################################################

# WEB SCRAPING #
url = "https://pt.wikipedia.org/wiki/2023"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

for tag in soup.find_all(class_="reference"):
    tag.decompose()

content_div = soup.find('div', class_='mw-content-ltr mw-parser-output')

elementos_lists = content_div.find_all('ul')

remov_cits = [
    'Wikisource', 'vde', 'Media relacionados com 2023 no Wikimedia Commons',
    'Fisiologia ou Medicina — Katalin Karikó e Drew Weissman',
    'Física — Pierre Agostini, Ferenc Krausz e Anne L\'Huillier',
    'Química — Alexey Ekimov, Louis Brus e Moungi Bawendi',
    'Literatura — Jon Fosse', 'Paz — Narges Mohammadi',
    'Ciências Económicas em Memória de Alfred Nobel —', '2023 no Brasil',
    '2023 no cinema', '2023 no desporto', 'Mortes em 2023',
    '2023 na música', '2023 em Portugal'
]
remov_list = set()

for elementos_list in elementos_lists:
    ul_text = elementos_list.text.strip()

    if any(remov_cit in ul_text for remov_cit in remov_cits):
        continue

    for line in ul_text.split('\n'):
        if line not in remov_list:
            print(line)
            remov_list.add(line)

######################################################################################
# DASHBOARD #

csv_file_path = 'data_radar.csv'

df_radar = pd.read_csv(csv_file_path)

categorias_qtd = Counter(df_radar['Categoria'])

data_barras_1 = {
    "Mês": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
    "Quantidade": [34, 25, 24, 8, 18, 19, 10, 13, 17, 19, 16, 15]
}
df_barras = pd.DataFrame(data_barras_1)

data_barras_2 = {
    "Mês": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
    "Quantidade": [20, 15, 18, 10, 14, 12, 8, 11, 16, 14, 12, 9]
}
df_barras2 = pd.DataFrame(data_barras_2)

data_linhas = {
    "Mês": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
    "Política": [7, 4, 8, 4, 4, 7, 4, 3, 4, 4, 3, 3],
    "Economia": [1, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 2],
    "Arte": [1, 2, 2, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    "Falecimentos e Nascimentos": [6, 1, 1, 0, 3, 2, 0, 1, 1, 1, 2, 3],
    "Esporte": [2, 4, 3, 0, 1, 3, 2, 2, 5, 3, 3, 2],
    "Desastes": [11, 6, 4, 1, 3, 3, 3, 2, 1, 4, 2, 1],
    "Ecossistema": [1, 3, 2, 0, 3, 2, 1, 3, 4, 5, 4, 2],
    "Ciência e Tecnologia": [3, 4, 2, 4, 2, 2, 0, 1, 2, 3, 2, 2],
    "Turismo": [2, 1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0],
}
df_linha = pd.DataFrame(data_linhas)

app = dash.Dash(__name__)

app.layout = html.Div(style={'background': '#FFFFFF'},
                      children=[
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#242424', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='Técnicas de Análise de Dados', style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'}),
                 html.H2(children='DASHBOARD DE RETROSPECTIVA DE EVENTOS 2023', style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'}),
                 html.P(children="Componentes: Alesângela Bezerra da Fonseca - 20211038060018, Lucas Leão Prudêncio da Costa - 20211038600023", style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'})
             ]),

    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H2(children='INTRODUÇÃO', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '2em'}),
                 html.P(children="Para a realização da atividade, optamos pela raspagem de dados ao site https://pt.wikipedia.org/wiki/2023. O site em questão remete aos principais eventos do ano, os quais foram filtrados para nossa utilização. Então, criamos dataframes para categorizar cada um dos eventos utilizando o material filtrado proveniente da raspagem.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="Um dos gráficos que consideramos utilizar é o Radar Chart, este que, por sinal, quantifica as categorias a quais definimos. O gráfico pode ser visto abaixo:", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 dcc.Graph(
                     id='radar-chart',
                         figure=px.line_polar(
                         r=list(categorias_qtd.values()),
                         theta=list(categorias_qtd.keys()),
                         line_close=True,
                         labels={'theta': 'Categoria', 'r': 'Quantidade'},
                         title='Quantidade de eventos por categoria',
                         color_discrete_sequence=['darkgrey'],
                     ).update_layout(
                         polar=dict(
                             radialaxis=dict(visible=True),
                         ),
                         showlegend=False,
                         title=dict(text='Quantidade de eventos por categoria', x=0.5)
                     )
                     #).update_traces(fill='toself')

                 ),
                 html.H2(children='24.77%', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '5em'}),
                 html.P(children="É a porcentagem que representa a categoria de eventos mais abundante: Política.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'})
             ]),

    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#242424', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='COMPARATIVO EM QUANTIDADES', style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'}),
                 html.P(children="Na próxima seção, utilizamos gráficos de barras que determinam a quantidade de eventos por mês.", style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'})
             ]),

    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H2(children='GRÁFICO DE BARRAS - 2023', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="Optamos usar um gráfico de barras simples referente aos números de ocorrências por mês no ano de 2023. Em seguida, compararemos com os valores do ano passado.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 dcc.Graph(
                     id='barras-1',
                     figure=px.bar(
                         df_barras,
                         x='Mês',
                         y='Quantidade',
                         color='Quantidade',
                         labels={'Quantidade': 'Quantidade'},
                         color_continuous_scale='greys',
                     )
                 )
             ]),

    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H2(children='GRÁFICO DE BARRAS - 2022', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="O gráfico abaixo permite perceber a diferença de valores em comparação com o anterior.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 dcc.Graph(
                     id='barras-2',
                     figure=px.bar(
                         df_barras2,
                         x='Mês',
                         y='Quantidade',
                         color='Quantidade',
                         labels={'Quantidade': 'Quantidade'},
                         color_continuous_scale='greys',
                     )
                 )
             ]),

    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H2(children='2023', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '5em'}),
                 html.P(children="Foi um ano mais agitado, possuindo um quantitativo de 218 eventos - 49 a mais que a contraparte do ano passado, que possui 169.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'})
             ]),

    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#242424', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='QUANTIDADES DE EVENTOS POR MÊS', style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'}),
                 html.P(children="Nosso próximo tópico nos trás à uma visualização a partir de um gráfico de barras empilhadas.", style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'})
             ]),
                 html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H2(children='NÚMEROS DE EVENTOS POR MÊS', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="Nesta análise, o gráfico de barras empilhadas tem por objetivo demonstrar o número de eventos de cada tipo por mês no ano de 2023.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 dcc.Graph(
                     id='stacked-bar-chart',
                     figure=px.bar(
                         df_linha.melt(id_vars='Mês', var_name='Categoria', value_name='Quantidade'),
                         x='Mês',
                         y='Quantidade',
                         color='Categoria',
                         labels={'Quantidade': 'Quantidade'},
                         color_discrete_map={'Política': 'lightcoral', 'Economia': 'lightgoldenrodyellow', 'Arte': 'lightsteelblue', 'Falecimentos e Nascimentos': 'dimgray', 'Esporte': 'lightseagreen', 'Desastes': 'lightpink', 'Ecossistema': 'lightgreen', 'Ciência e Tecnologia': 'lightskyblue', 'Turismo': 'plum'},
                         barmode='stack'
                     )
                 )
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#242424', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='COM BASE NOS DADOS OBSERVADOS...', style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'}),
                 html.P(children="Podemos tirar conclusões interessantes quanto a relação quantidade-mês.", style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'})
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='❄', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '6em'}),
                 html.H2(children='JULHO', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="...Foi o mês mais tranquilo entre todos do ano.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='🔥', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '6em'}),
                 html.H2(children='JANEIRO', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="...Enquanto janeiro foi o mês mais agitado.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='DESASTRES', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H2(children='"Terroristas do Hamas lançam um ataque a partir da Faixa de Gaza, infiltrando-se no sul de Israel e provocando uma resposta militar completa das Forças de Defesa do país. O ataque deixou centenas de mortos e milhares de feridos."', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="- Janeiro foi o mês que mais apresentou eventos negativos durante o ano.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='POLÍTICA', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H2(children='"Brasil assume a presidência do G20."', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="- Março foi o mês que mais apresentou eventos políticos durante o ano.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='CIÊNCIA E TECNOLOGIA', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H2(children='"Como resposta ao lançamento de um satélite espião pelo vizinho do Norte, a Coreia do Sul lança seu primeiro satélite do tipo, a bordo do foguete Falcon 9 da SpaceX."', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="- Fevereiro e abril empatam como os meses com mais eventos dessa categoria.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='ECONOMIA', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H2(children='"O Brasil e a China assinam um acordo para negociar em suas próprias moedas, deixando de usar o dólar americano como intermediário."', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="- Março e dezembro empatam como os meses com mais eventos dessa categoria.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='ESPORTE', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H2(children='"O Manchester City conquista a Copa do Mundo de Clubes da FIFA pela 1.° vez, vencendo o Fluminense por 4×0 na final."', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="- Setembro foi um mês com maiores quantidades de eventos relacionados.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='ECOSSISTEMA', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H2(children='"Um terremoto de magnitude 6,4 atinge a região de Jajarkot, no Nepal, deixando mais de 150 mortos."', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="- Janeiro teve a maior quantidade de eventos sobre ecossistema.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='FALECIMENTOS E NASCIMENTOS', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H2(children='"A cantora Lisa Marie Presley, filha de Elvis Presley, morre aos 54 anos."', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="- Janeiro também foi o mês com maiores eventos envolvendo mortes ou nascimentos.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='ARTE', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H2(children='"Taylor Swift ganha 9 troféus no MTV VMA 2023 e bate o recorde de vitórias em uma noite de premiação do evento, que antes pertencia a Lady Gaga."', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="- Fevereiro e março aparecem com o mesmo número de eventos da mesma categoria.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
             ]),
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='TURISMO', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H2(children='"O Papa Francisco chega em Kinshasa para uma visita à República Democrática do Congo, a primeira visita papal ao país desde 1985, viajando para o Sudão do Sul em seguida."', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="- Janeiro e outubro têm a mesma quantidade de eventos de mesma categoria.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
             ]),                          
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#242424', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='CONCLUSÃO', style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'}),  
             ]),        
    html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.P(children="Realizar a raspagem de dados na Wikipedia nos possibilitou um resultado o qual pudemos tomar a liberdade para refiná-lo e adaptá-lo para nossas necessidades. Como prova, transformamos em informação visual a partir dos gráficos e demos sentido às analises citadas.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'})
             ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)