import math
import pandas as pd

def find_quadrante(lat, long, passo):

    distanciaX = 37/passo

    posicaoX = long-(-75)
    posicaoX = math.floor(posicaoX/passo)

    posicaoY = (7-lat)
    posicaoY = math.floor(posicaoY/passo)

    quadrante = posicaoX + (posicaoY*distanciaX)

    return quadrante

if __name__ == '__main__':
    
    quadrandes = []
    step = 0.25

    path = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/treino/CSVs/temp/treino.csv'
    csv = pd.read_csv(path, sep = ';')

    latitude = csv['latitude'].to_numpy()
    longitude = csv['longitude'].to_numpy()

    for i in range(len(latitude)): 
        quadrandes.append(find_quadrante(latitude[i], longitude[i], step))

    csv['zona_025'] = quadrandes
    print(csv)

    csv.to_csv(path, sep = ';', index = False)