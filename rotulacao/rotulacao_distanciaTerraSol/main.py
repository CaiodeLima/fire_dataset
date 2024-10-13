import pandas as pd
import os

os.system('cls' if os.name == 'nt' else 'clear')

pathDistances = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_distanciaTerraSol/distancias.csv'
distancesData = pd.read_csv(pathDistances, sep=';')
distancias = distancesData['distance'].tolist()

def find_distance(dia):
    # Pesquisa a distância da terra de acordo com o dia dado
    distance = distancias[dia-1]

    return distance

#-------------------------------------------------------MAIN---------------------------------------------------------
if __name__ == '__main__':

    pathFile = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/treino/CSVs/predicao_atrasado.csv'
    file = pd.read_csv(pathFile, sep = ';')
    dias = file['dia365'].tolist()
    
    distancias = []

    count = 0

    for i in dias:
        distancias.append(find_distance(i))
        count += 1
        if count % 5000 == 0:
            print(100*(count/len(dias)),'%')

    file['distanciaSol'] = distancias

    print('Salvando')
    file.to_csv(pathFile, sep = ';', index = False)