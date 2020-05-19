import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

#Título e sidebar
st.title("Análise de Sentimento de Companhias Aéreas Através de Tweets")
st.sidebar.title("Análise de Sentimento de Companhias Aéreas Através de Tweets")

st.markdown("Essa aplicação é um estudo da biblioteca 'streamlit' e analisa o sentimento dos usuários com relação às companhias aéreas através de tweets.")

#define o dataset
DATA_URL = ("Tweets.csv")

#lê o dataset e mantem salvo em cache para evitar gasto computacional desnecessário
@st.cache(persist = True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created']) #transformação para o datetime
    return data

#executa a função para leitura do ds
data = load_data()

#criação de radio btns para mostrar um tweet aleatório do sentimento escolhido (em inglês pq o ds inteiro é em inglês lol)
st.sidebar.subheader('Mostra um tweet aleatório')
random_tweet = st.sidebar.radio('Sentimento (em inglês):', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

#dá as opções para o usuário visualizar no. de tweet/sentimento através de um histograma ou pizza
st.sidebar.markdown('### Número de tweets por sentimento')
select = st.sidebar.selectbox('Tipo de gráfico', ['Histograma', 'Gráfico de Pizza'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Esconder", True):
    st.markdown('Número de tweets por sentimento')
    if select == 'Histograma':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

#filtrar o horário de postagem de cada tweet
st.sidebar.subheader("Quando e em que horário os usuários tweetaram?")
hour = st.sidebar.slider("Hora do dia:", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Esconder", True, key='1'):
    st.markdown("### Localização dos tweets com base no horário do dia")
    st.markdown("%i tweets entre %i:00 e %i:00" % (len(modified_data),hour, (hour+1)%24))
    st.map(modified_data)
    if sr.sidebar.checkbox("Show raw data", False):
        st.write(data)

st.sidebar.subheader('Escolha a companhia aérea específica que deseja analisar')
choice = st.sidebar.multiselect('Escolha a companha:', ('Us Airways', 'United', 'American Airlines', 'Soutwest', 'Delta Airlines', 'Virgin'))

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment', facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
st.plotly_chart(fig_choice)

st.sidebar.header('Nuvem de Palavras')
word_sentiment = st.sidebar.radio('Qual sentimento você deseja ver a nuvem de palavras?', ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox('Esconder', True, key=3):
    st.header('Nuvem de palavras para o sentimento %s'%(word_sentiment))
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ''.join(df['text'])
    processed_words = ''.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()