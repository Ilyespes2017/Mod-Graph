# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mVEniof6NTjsLdJ1xgFBkZXKydgpaXeK
"""

! sudo apt-get install metis

! pip install Cluster_Ensembles

import numpy as np
import matplotlib.pyplot as plt
from random import choice
import community as cm
import networkx as nx


import Cluster_Ensembles as CE

Adj_matrix_sym = np.array ([[1,0,1,1,0],[0,1,0,0,1],[1,0,1,1,1],[1,0,1,1,0],[0,1,1,0,1]])


plt.spy(Adj_matrix_sym)
plt.show()

g_non_orient = nx.from_numpy_matrix(Adj_matrix_sym)

nx.draw(g_non_orient)
plt.title("graph no orienté")
plt.show()


#Generation d'un graphe à l'aide de la distribution erdos renyi
G = nx.erdos_renyi_graph(50, 0.1)

#Detection de communautés: application de l'algorithme de Louvain
partition = cm.best_partition(G)

print("partition", partition)


#Calcul de la modularité liée à cette partition
modularity_value = cm.modularity(partition, G )

print("modularity value", modularity_value)

#Visualisation du nombre de communautés retrouvé
vect_label = set(partition.values())


print("vect_label", vect_label)

size = int(len(set(partition.values())))

print("size", size)

#générer un vecteur de couleurs = au nombre de communautés 
colors = ["#"+''.join([choice('0123456789ABCDEF') for j in range(6)]) for i in range(size)]

#Affichage du graphe
pos = nx.spring_layout(G)

count = 0
for com in set(partition.values()) :
    list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20, node_color = (colors[count]))
    count += 1
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.axis("off")
plt.show

clustering_1 = [0,1,1,2,0,2,1,0,2,1]
clustering_2 = [0,1,2,0,0,2,2,1,2,1]
clustering_3 = [2,0,0,2,1,1,1,0,1,2]
cluster_runs = np.array([clustering_1, clustering_2, clustering_3])
print("cluster_runs", cluster_runs)




consensus_clustering_labels = CE.cluster_ensembles(cluster_runs, verbose = True, N_clusters_max = 3) 
print("consensus_clustering_labels", consensus_clustering_labels)

import pandas as pd 
  
  # reading csv file  
article = pd.read_csv("article.csv", sep="\t")
auteur =  pd.read_csv("auteur.csv", sep = ";")

article.describe()

article.groupby('year').agg('count')

#Supprimer les lignes qui n'ont pas d'abstract
article['abstract'].replace('',np.nan, inplace=True)
article.dropna(subset=['abstract'], inplace = True)

#Supprimer les lignes qui n'ont pas d'affliation
auteur['Affiliation'].replace('',np.nan, inplace=True)
auteur.dropna(subset=['Affiliation'], inplace = True)

article

docAut = pd.DataFrame(np.zeros((article.shape[0],len(auteur["Authors_Name"]))), columns =  auteur["Authors_Name"])

docAut

i=0
for x in article["authors"]:
  print(i)
  for j in x.split(", "):
    print(j)
    if (np.sum(j == auteur["Authors_Name"])>0):
      print("trouvé")
      docAut.ix[i,j] =1 
  i+=1

docAut

docAut.sum()

docAut.to_csv("docAut.csv", sep='\t')



