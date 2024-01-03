from googleapiclient.discovery import build
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
from textblob import TextBlob
import plotly.express as px
from wordcloud import WordCloud
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import re
from collections import Counter

#pip install google-api-python-client textblob pandas plotly wordcloud nltk gensim

nltk.download('stopwords')

# Coleta de Comentários do YouTube
chave_api = 'AIzaSyALMdBBTtO9szEhc9Mm_bX8Psc6GPfwiYU'
youtube = build('youtube', 'v3', developerKey=chave_api)

def coletar_comentarios(video_id, max_comentarios=100):
    comentarios = []
    datas = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_comentarios,
        textFormat="plainText"
    )
    response = request.execute()

    for item in response['items']:
        comentario = item['snippet']['topLevelComment']['snippet']['textDisplay']
        data = item['snippet']['topLevelComment']['snippet']['publishedAt']
        comentarios.append(comentario)
        datas.append(data)

    return comentarios, datas

video_id = 'N8Nf56srwcA'
comentarios, datas = coletar_comentarios(video_id, max_comentarios=100)

df_comentarios = pd.DataFrame({'comentario': comentarios, 'data': pd.to_datetime(datas)})

# Análise de Sentimento e Cálculo da Polaridade
def calcular_polaridade(texto):
    return TextBlob(texto).sentiment.polarity

df_comentarios['polaridade'] = df_comentarios['comentario'].apply(calcular_polaridade)
df_comentarios['polaridade'] = pd.to_numeric(df_comentarios['polaridade'], errors='coerce')
df_comentarios['polaridade'].fillna(0, inplace=True)

# Classificação de Sentimento
def classificar_sentimento(polaridade):
    if polaridade < -0.3:
        return 'negativo'
    elif polaridade > 0.3:
        return 'positivo'
    else:
        return 'neutro'

df_comentarios['sentimento'] = df_comentarios['polaridade'].apply(classificar_sentimento)

# Nuvem de palavras
def criar_imagem_nuvem_palavras(texto):
    plt.figure(figsize=(10, 5))
    nuvem_palavras = WordCloud(width=800, height=400, background_color='white', stopwords=stop_words).generate(texto)
    plt.imshow(nuvem_palavras, interpolation='bilinear')
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('utf-8')

stop_words = set(stopwords.words('english'))

# Concatenar todos os comentários para formar o texto para a nuvem de palavras
texto = " ".join(comentario for comentario in df_comentarios['comentario'])

imagem_nuvem_palavras = criar_imagem_nuvem_palavras(texto)

# Removendo stopwords e caracteres especiais
palavras = [palavra for palavra in texto.split() if palavra.lower() not in stop_words and re.match(r'^[a-zA-Z]+$', palavra)]
frequencias = Counter(palavras)
mais_comuns = frequencias.most_common(30)
palavras, frequencias = zip(*mais_comuns)

# Dashboard
app = Dash(__name__)

categorias_sentimento = ['negativo', 'neutro', 'positivo']
sentimento_counts = df_comentarios['sentimento'].value_counts().reindex(categorias_sentimento)


print(sentimento_counts)

cores = {'negativo': 'purple', 'neutro': 'pink', 'positivo': 'blue'}

dados_grafico = []
for categoria in categorias_sentimento:
    dados_grafico.append(
        go.Bar(
            x=[categoria], 
            y=[sentimento_counts[categoria]], 
            marker_color=cores[categoria],
            name=categoria
        )
    )

app.layout = html.Div(style={'background': '#FFFFFF'},
                      children=[
                          html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#242424', 'margin-bottom': '20px'},
             children=[
                 html.H1(children='Técnicas de Análise de Dados', style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'}),
                 html.H2(children='DASHBOARD ANÁLISE DE COMENTÁRIOS DO YOUTUBE', style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'}),
                 html.P(children="Componentes: Alesângela Bezerra da Fonseca - 20211038060018, Lucas Leão Prudêncio da Costa - 20211038600023", style={'fontFamily': 'Arial, sans-serif', 'color': '#FFFFFF'})
             ]),

        html.Div(style={'textAlign': 'center', 'padding': '20px', 'background': '#E8E8E8', 'width': '50%', 'margin': 'auto', 'border-radius': '10px', 'margin-bottom': '20px'},
             children=[
                 html.H2(children='INTRODUÇÃO', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '2em'}),
                 html.P(children="O objetivo deste projeto é analisar o sentimento e as tendências nos comentários de um vídeo específico do YouTube. Queremos entender melhor como o público reage ao conteúdo do vídeo, analizando como os sentimentos variam ao longo do tempo. Calculando cada comentário como positivo, negativo ou neutro. E mostrar as palavras mais frequentes nos comentários, o que pode dar insights sobre os tópicos mais discutidos.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H3(children='TÉCNICAS UTILIZADAS', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '2em'}),
                 html.P(children="Raspagem de Dados: Usamos a API do YouTube, que fez a coleta dos comentários de um vídeo específico.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="Processamento de Linguagem Natural (NLP): Aplicamos técnicas de NLP, como análise de sentimentos, usando a biblioteca TextBlob que criou uma nuvem de palavras para visualizar os termos mais frequentes nos comentários.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H3(children='COLETA E PREPARAÇÃO DOS DADOS', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '2em'}),
                 html.P(children="API do YouTube: Configuramos a API do YouTube para acessar os comentários, filtrando os dados relevantes.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="Limpeza dos Dados: Implementamos a remoção de stopwords que fosse retirada algumas palavras e caracteres irrelevantes.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.P(children="Análise de Sentimento: Utilizamos TextBlob para analisar a polaridade dos sentimentos nos comentários.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 html.H4(children='Distribuição de Sentimentos nos Comentários', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '2em'}),
                 html.P(children="Este gráfico de barras mostra a proporção de comentários positivos, negativos e neutros. Ele oferece uma visão geral do tom emocional dos comentários do vídeo.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                 # Gráfico de Distribuição de Sentimentos
                 dcc.Graph(
                        id='sentiment-bar-chart',
                        figure={
                            'data': [
                                go.Bar(
                                    x=[categoria], 
                                    y=[sentimento_counts[categoria]], 
                                    marker_color=cores[categoria],
                                    name=categoria
                                ) for categoria in categorias_sentimento
                            ],
                            'layout': {
                                'title': 'Distribuição de Sentimentos',
                                'xaxis': {'title': 'Sentimento'},
                                'yaxis': {'title': 'Quantidade'}
                            }
                        }
                    ),
                    html.H4(children='Nuvem de palavras Mais Comuns nos Comentários', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '2em'}),
                    html.P(children="A nuvem de palavras destaca as palavras mais frequentes nos comentários. Palavras maiores indicam maior frequência, oferecendo insights sobre os temas mais discutidos.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                    #  Nuvem de Palavras
                    html.Img(src=imagem_nuvem_palavras),

                    html.H4(children='Gráfico de Palavras Mais Frequentes', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '2em'}),
                    html.P(children="Este gráfico de barras exibe as palavras mais frequentes e suas contagens, revelando os termos mais destacados e recorrentes nos comentários.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                    # Gráfico de Palavras Mais Frequentes
                    dcc.Graph(
                        id='frequent-words-chart',
                        figure={
                            'data': [
                                {'x': palavras, 'y': frequencias, 'type': 'bar', 'name': 'Frequência'},
                            ],
                            'layout': {
                                'title': 'Palavras Mais Frequentes',
                                'xaxis': {'title': 'Palavra'},
                                'yaxis': {'title': 'Frequência'},
                            }
                        }
                    ),

                    html.H4(children='Evolução dos Sentimentos ao Longo do Tempo', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '2em'}),
                    html.P(children="Este gráfico de linha traça a variação dos sentimentos (positivo, negativo, neutro) ao longo do tempo, mostrando como as reações do público mudaram no decorrer do tempo.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'}),
                    # Tendência de Sentimentos ao Longo do Tempo
                    dcc.Graph(
                        id='sentiment-trend',
                        figure=px.line(df_comentarios.set_index('data').resample('W')['polaridade'].mean(), 
                            y='polaridade', 
                            title='Tendência de Sentimentos ao Longo do Tempo', 
                            labels={'y':'Polaridade Média', 'data':'Data'})
                    ),
                    
                    html.H4(children='Conclusão', style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38', 'font-size': '2em'}),
                    html.P(children="Este projeto nos proporcionou a capacidade de analisar sentimentos e tendências em comentários de vídeos do YouTube. Utilizando técnicas de processamento de linguagem natural, conseguimos identificar a predominância de sentimentos positivos, negativos ou neutros, além de destacar palavras-chave e tendências ao longo do tempo. Essa análise fornece insights valiosos sobre as reações e percepções do público, auxiliando na compreensão e no aprimoramento de estratégias de conteúdo.", style={'fontFamily': 'Arial, sans-serif', 'color': '#232C38'})                    
             ]),
             
                      ])


if __name__ == '__main__':
    app.run_server(debug=True)
