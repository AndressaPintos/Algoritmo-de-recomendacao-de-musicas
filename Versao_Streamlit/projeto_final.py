from queue import Full
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances_argmin_min
from matplotlib.ticker import ScalarFormatter
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
import streamlit as st
from IPython.display import Image
import warnings
warnings.filterwarnings("ignore")

TabelaTeste = pd.read_csv('TabelaTestes.csv')
df = pd.read_csv('ds_modified.csv')
parametros = ['Valence','Acousticness','Danceability',
              'Duration_min','Energy','Instrumentalness',
              'Liveness','Loudness','Speechiness','Tempo',
              'Popularity','EnergyLiveness']
dados = df[parametros]

escala = RobustScaler()
dados_normalizados = escala.fit_transform(dados)

#Número de musicas de entrada e saída
entrada = 4
saida = 5

st.title("Algoritmo de recomendação de músicas usando clusterização")
st.write("A proposta do trabalho é desenvolver um algoritmo que recomende uma playlist (lista de músicas)"
+" com base em outra playlist, passada como entrada. Para isso,"
+" serão utilizados os conhecimentos adquiridos na disciplina Computação Científica e Análise de Dados sobre clusterização, PCA e manipulação de vetores.")

st.sidebar.header("Escolha o gênero das playlists")

Genero = 'PopF'

# Criar um botão
if st.sidebar.button("Pop"):
    Genero='PopF'
if st.sidebar.button("Rock alternativo"):
    Genero='PopM'
if st.sidebar.button("Heavy Metal"):
    Genero='Heavy Metal'
if st.sidebar.button("Clássica"):
    Genero='Classica'
if st.sidebar.button("Funk"):
    Genero='Funk'
if st.sidebar.button("Samba"):
    Genero='Samba'
if st.sidebar.button("Rap"):
    Genero='Rap'
   



#método do cotovelo
#sqr = []
#k_range = range(1, 50)
#for k in k_range:
#    kmeans = KMeans(n_clusters=k,init='k-means++',random_state=21)
#    kmeans.fit(dados_normalizados)
#    sqr.append(kmeans.inertia_)

#plt.figure(figsize=(16, 8))
#plt.plot(k_range, sqr, marker='o')
#plt.title('Método do Cotovelo')
#plt.xlabel('Quantidade de Clusters')
#plt.ylabel('Soma do Quadrado da distância entre os pontos e os seus centróides')
#plt.plot(9, sqr[8], marker='.', color='red', markersize=10)
#plt.text(9, sqr[10], f'{sqr[10]:.2f}', ha='right', va='bottom', fontsize=12, color='black')


#plt.xticks(range(1, 50, 1))
#plt.grid(axis='both', linestyle='--', alpha=0.7)

#plt.show()

st.header("Escolha da quantidade de clusters")
st.write("O primeiro passo antes de executar o algoritmo é definir a quantidade de clusters, pois a clusterização escolhida foi o K-means. Para isso, utilizo o Método do Cotovelo, gerando um gráfico que indica como a soma das distâncias quadráticas entre os pontos de dados e seus respectivos centróide diminui à medida que a quantidade de clusters aumenta:")
st.image("MC.png", caption="Método do cotovelo")

# **K-means**

k = 9
kmeans = KMeans(n_clusters=k, init='k-means++',random_state=21)
kmeans.fit(dados_normalizados)

df['cluster'] = kmeans.labels_

#**Cálculo do PCA - usado nas visualizações**"""

pca = PCA(n_components=3)
dados_pca = pca.fit_transform(dados_normalizados)

df['PCA1'] = dados_pca[:, 0]
df['PCA2'] = dados_pca[:, 1]
df['PCA3'] = dados_pca[:, 2]

# **Animação da clusterização**"""


#def update(frame):
 #   k = frame + 2
  #  kmeans = KMeans(n_clusters=k, init='k-means++',random_state=21)
   # kmeans.fit(dados_pca)
    #ax.clear()
    #ax.scatter(dados_pca[:, 0], dados_pca[:, 1], c=kmeans.labels_, cmap='viridis', s=50)
#    ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='red', marker='.', s=100)
 #   ax.set_title(f'Clusterização usando K-Means, com quantidade de clusters = {k}')


#fig, ax = plt.subplots(figsize=(10, 6))
#ani = animation.FuncAnimation(fig, update, frames=range(8), interval=1000, repeat=False)

#from IPython.display import HTML
#ani.save("animacaoKmeans.gif", writer="pillow")
#plt.close(fig)

st.header("Clusterização")

st.write("Obtida a quantidade de clusters, "
+"agora é preciso realizar a clusterização dos dados."
+" O algoritmo escolhido foi o K-means, que trabalha da seguinte forma")

st.write("1 - Seleciona os primeiros 9 centróides de forma aleatória (são pontos existentes nos dados)"
+" e adiciona os pontos no cluster do centróide mais pŕoximo."
+" Ou seja, aquele para o qual a distância euclidiana ao quadrado é a menor possível")

st.write("2 - Recalcula o valor do novo centróide, que agora é o ponto médio dos pontos. "
+"O cálculo é feito da seguinte forma: é criado um vetor S que é a soma de todos os vetores "
+"(pontos) de músicas que se encontram naquele cluster. "
+"Então divide-se esse vetor S pela quantidade de N pontos no cluster,"
+" ou seja, todas as suas 12 dimensões são divididas por essa quantidade N")

st.write("3 - Retorna para o item 2. até que não haja mais mudanças nos centróides "
+"(critério de convergência do algoritmo)")

st.write("Na aplicação, foi utilizado um inicializador no algoritmo K-means para que os primeiros centróides"
+" fossem escolhidos levando em consideração a dispersão dos dados."
+" Com isso, pontos mais distantes dos outros têm maior chance de serem escolhidos como centróide inicial.")

st.write("Um parâmetro também foi utilizado para controlar a aleatoriedade do processo de inicialização no K-means,"
+" garantindo consistência nos resultados. Começando sempre com os mesmos pontos iniciais")

st.image("animacaoKmeans.gif", caption="Clusterização (os pontos vermelhos são os centróides)")

# **Visualização dos clusters**"""

#Visualização da distribuição dos pontos em cada cluster, e visualização dos clusters

palettes = sns.color_palette("tab20", n_colors=9)

plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='cluster', palette='viridis')
plt.title('Distribuição dos pontos nos clusters')
plt.xlabel('Número do cluster')
plt.ylabel('Quantidade de pontos')
plt.savefig("Distribuição.png", dpi=300) 
plt.show()

plt.figure(figsize=(10, 6))
scatter_plot = sns.scatterplot(
    x=df['PCA1'],
    y=df['PCA2'],
    hue=df['cluster'],
    palette=palettes,
    alpha=0.7
)
plt.title('Distribuição dos clusters')
plt.savefig("Clusters.png", dpi=300) 
plt.show()
st.image("Distribuição.png", caption="Distribuição dos pontos nos clusters")
st.image("Clusters.png", caption="Distribuição dos clusters")

# características médias por cluster
cluster_summary = df.groupby('cluster')[parametros].mean()
print(cluster_summary)

# **Seleção da músicas usadas na entrada do algoritmo**"""

Lista_id_musicas = TabelaTeste.loc[TabelaTeste['Genero'] == Genero]['Musicas']
Lista_id_artistas = TabelaTeste.loc[TabelaTeste['Genero'] == Genero]['Artistas']
linha = df.loc[((df['Track'] == Lista_id_musicas.iloc[0]) & (df['Artist'] == Lista_id_artistas.iloc[0])) |
               ((df['Track'] == Lista_id_musicas.iloc[1]) & (df['Artist'] == Lista_id_artistas.iloc[1])) |
               ((df['Track'] == Lista_id_musicas.iloc[2]) & (df['Artist'] == Lista_id_artistas.iloc[2])) |
               ((df['Track'] == Lista_id_musicas.iloc[3]) & (df['Artist'] == Lista_id_artistas.iloc[3]))]

colunas = linha[['Valence','Acousticness','Danceability',
                 'Duration_min','Energy','Instrumentalness',
                 'Liveness','Loudness','Speechiness',
                 'Tempo','Popularity','EnergyLiveness']]
colunas = escala.transform(colunas)

pontos = [linha for linha in colunas[:entrada]]
musicas = np.stack([pontos[0], pontos[1], pontos[2],pontos[3]])
pontoMedio = np.mean(musicas, axis=0)
pontoMedio = pontoMedio.reshape(1, -1)
cluster = kmeans.predict(pontoMedio)

pca_pontoMedio = pca.transform(pontoMedio)
pca1 = pca_pontoMedio[0, 0]
pca2 = pca_pontoMedio[0, 1]
pca3 = pca_pontoMedio[0, 2]

dados_cluster = df[df['cluster'].isin(cluster)]


st.header("Playlist passada como entrada do algoritmo")
Entrada = pd.DataFrame({
    'Nome do Cantor': linha['Artist'], # Changed from linha[['Artist']] to linha['Artist']
    'Nome da Música': linha['Track'], # Changed from linha[['Track']] to linha['Track']
    'Cluster ao qual pertence': linha['cluster'] # Changed from linha[['cluster']] to linha['cluster']
})
st.table(Entrada)

# **Visualização do ponto médio das músicas**"""

plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=dados_cluster['PCA1'],
    y=dados_cluster['PCA2'],
    hue=dados_cluster['cluster'],
    palette='viridis',
    alpha=0.7
)

plt.scatter(
      pca1,
      pca2,
      s=150,
      edgecolor='black',
      color='red',
      label=f"Ponto Médio",
      marker='.'
    )

plt.title('Distribuição do cluster que contém o ponto médio')
plt.xlabel('PCA1')
plt.ylabel('PCA2')

plt.legend()
plt.savefig("PontoMedio.png", dpi=300) 
plt.show()

st.write("Após encontrar os valores dos 4 vetores de música, o algoritmo encontra o ponto médio deles. "
+"Após determinar esse ponto médio, determina-se a qual "
+"cluster esse ponto pertence, baseando-se na posição dos pontos em relação aos centróides")

st.image("PontoMedio.png", caption="Ponto médio das músicas")

# **Cálculo dos pontos com menor distância euclidiana para o ponto médio**"""

totalPontos = dados_cluster[parametros].values
totalPontos = escala.transform(totalPontos)

total_distancias = np.sum(np.linalg.norm(totalPontos[:, np.newaxis] - pontoMedio, axis=2), axis=1)

pontosProximosIndice = []
pontosProximos = []
pontosProximosInfo = []

musicas_entrada = set(linha['Track'])
musicas_repetidas = set()
indice_mais_proximo = np.argmin(total_distancias)

for _ in range(saida):

  track_artist = dados_cluster.iloc[indice_mais_proximo]['Track']

  while  track_artist in musicas_entrada or track_artist in musicas_repetidas:
    total_distancias[indice_mais_proximo] = np.inf
    indice_mais_proximo = np.argmin(total_distancias)
    track_artist = dados_cluster.iloc[indice_mais_proximo]['Track']

  musicas_repetidas.add(track_artist)


  indice_mais_proximo = np.argmin(total_distancias)
  pontosProximosIndice.append(indice_mais_proximo)
  pontosProximos.append(totalPontos[indice_mais_proximo])
  pontosProximosInfo.append(dados_cluster.iloc[indice_mais_proximo])
  total_distancias[indice_mais_proximo] = np.inf

Track=[]
Artist=[]

for i in range(saida):
    Track.append(pontosProximosInfo[i]['Track'])
    Artist.append(pontosProximosInfo[i]['Artist'])

# **Visualização do ponto médio e dos pontos que representam as músicas recomendadas**"""

fig = plt.figure(figsize=(16, 6))

ax1 = fig.add_subplot(121)
sns.scatterplot(
    x=dados_cluster['PCA1'],
    y=dados_cluster['PCA2'],
    hue=dados_cluster['cluster'],
    palette='viridis',
    alpha=0.7,
    s=50,
    legend="full",
    ax=ax1
)

ax1.scatter(
    pca1,
    pca2,
    color='red',
    edgecolor="black",
    s=200,
    marker="o",
    label=f"Ponto médio"
    )

colors = ['red', 'blue', 'yellow', 'orange','green']
for i,pt in enumerate(pontosProximos):
  pca_pontosProximos = pca.transform([pt])
  ax1.scatter(
      pca_pontosProximos[0, 0],
      pca_pontosProximos[0, 1],
      color=colors[i],
      edgecolor="black",
      s=300,
      marker="*",
      label=f"{i+1}º Ponto mais próximo"
      )

ax1.set_title("Visualização 2D")
ax1.set_xlabel('PCA1')
ax1.set_ylabel('PCA2')
ax1.legend()

ax2 = fig.add_subplot(122, projection='3d')


ax2.scatter(
        pca1,
        pca2,
        pca3,
        color='red',
        edgecolor="black",
        s=200,
        marker="o",
        label=f"Ponto médio"
    )

for i, pt in enumerate(pontosProximos):
  pca_pontosProximos = pca.transform([pt])
  ax2.scatter(
      pca_pontosProximos[0, 0],
      pca_pontosProximos[0, 1],
      pca_pontosProximos[0, 2],
      color=colors[i],
      edgecolor="black",
      s=300,
      marker="*",
      label=f"{i+1}º Ponto mais próximo"
  )

ax2.set_title("Visualização 3D")
ax2.set_xlabel('PCA1')
ax2.set_ylabel('PCA2')
ax2.set_zlabel('PCA3')
ax2.legend()

plt.tight_layout()
plt.savefig("3D.png", dpi=300) 
st.image("3D.png", caption="Visualização 2D e 3D dos pontos")
plt.show()

#cálculo do erro de cada ponto próximo para o ponto médio
st.header("Distância de cada música para o ponto médio")

st.write("Tendo encontrado o cluster ao qual ele pertence, seleciona-se todos os pontos daquele cluster,"
+" sendo somente esse pontos usados na próxima fase: procura-se,"
+" então, os 5 pontos mais próximos desse ponto médio,"
+" ou seja, aqueles com menor distância euclidiana ao quadrado para o ponto médio. ")

for i in range(5):
  st.write(f"Distância da música {i+1}: {np.linalg.norm(pontoMedio-pontosProximos[i])}")

st.write("Com isso, conseguimos a playlist mais parecidas com o ponto médio da playlist de entrada.")

st.header("Playlist Recomendada!")
Saida = pd.DataFrame({
    'Nome do Cantor': Artist, # Changed from linha[['Artist']] to linha['Artist']
    'Nome da Música': Track # Changed from linha[['Track']] to linha['Track']
})
st.table(Saida)


