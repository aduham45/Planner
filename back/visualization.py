#!/usr/bin/env python
# coding: utf-8 


###############################################################################
#Fichier contenant les fonction permettant de visualiser les données
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#05/01/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import dataframes
import networkx as nx
import matplotlib.pyplot as plt
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
def waysVisualization(df):
    G=nx.from_pandas_edgelist(df, source='cityDep_id', target='cityArr_id', edge_attr='distance')
    nx.draw(G, with_labels=True, node_color='g', alpha=0.7, node_size=500, width=0.1,edge_color='g')
    plt.show()
"""
df = df_places
df.head()

limits = [(0,1),(1,10),(10,100),(100,1000)]
colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(75,21,30)","lightgrey"]
cities = []
scale=100

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[lim[0]:lim[1]]
    city = dict(
        type = 'scattergeo',
        locationmode = 'FRANCE states',
        lon = df_sub['lng'],
        lat = df_sub['lat'],
        marker = dict(
            size = df_sub['visits']/scale,
            color = colors[i],
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1]) )
    cities.append(city)

layout = dict(
        title = 'Répartition des différentes places à travers toute la France et nombre de visites annuelles',
        showlegend = True,
        geo = dict(
            scope='europe',
            projection=dict( type='albers' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 0)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

fig = dict( data=cities, layout=layout )
py.offline.plot( fig, validate=False, filename='d3-bubble-map-populations' )
"""
waysVisualization(dataframes.paramsToDf("'driving'"))
###############################################################################