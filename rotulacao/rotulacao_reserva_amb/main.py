'''
código que checa se dado ponto cai dentro de um poligono de um arquivo .shp, serve para criar features binárias do tipo 'PRESENTE EM AREA INDIGENA? 1 / 0' por ex.
'''

import os
from tkinter import E
from pkg_resources import ensure_directory
from pytz import all_timezones
import geopandas as gpd #uma das piores bibliotecas das quais tive o desprazer de tabalhar, sinceramente
import pandas as pd
gpd.options.use_pygeos = True
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface

def check_presence(endereco_shapefile, latitude, longitude):

    polygon = gpd.GeoDataFrame.from_file(endereco_shapefile, geometry='geometry')

    points = []

    for i in range(len(latitude)):
        aux = Point(longitude[i],latitude[i])
        points.append(aux)

    pointsDF = gpd.GeoDataFrame(geometry=points)
    #pointsDF.to_file('/home/scholles/Desktop/CENSIPAM/Codigos/queimadas_datasets/rotulacao/rotulacao_indigenas/shape/pontos.shp')

    within = gpd.sjoin(polygon, pointsDF, op='contains', how='inner')
    
    return within

if __name__ == "__main__":
    
    reservaAmbiental = []

    end = '/home/scholles/Desktop/CENSIPAM/Codigos/queimadas_datasets/rotulacao/rotulacao_reserva_amb/shape/UNC_21_BR_CEM_V2.shp'
    path = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles2/Datasets/classic/treino.csv'
    
    df = pd.read_csv(path, sep=';')
    latitudeList = df['Latitude'].to_list()
    longitudeList = df['Longitude'].to_list()

    pointsInside = check_presence(end, latitudeList, longitudeList)
    index = pointsInside['index_right'].to_list()
    print(len(index))

    '''
    csvSize = len(longitudeList)
    reservaAmbiental = [0] * csvSize

    for i in index:
        reservaAmbiental[i] = 1    
    
    df['Reserva Ambiental'] = reservaAmbiental
    df.to_csv(path, sep=';', index = False)
    '''