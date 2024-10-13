import pandas as pd
import math
import rasterio
from rasterio.plot import show
import os
from collections import Counter


#----------------------------------------------------------------
#---------------------VARIÁVEIS GLOBAIS--------------------------
nomeArquivo = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/AnosCSVs/2021.csv' # Sempre mudar o mês de acordo com o que está sendo rotulado
nomeBackup = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_vegetacao/Backup.csv'
coverPath = r'/home/scholles/Desktop/CENSIPAM/Codigos/TIFFs/MAPBiomasCoverage/brasil_coverage_2020.tif'
coverIMG = rasterio.open(coverPath)
#----------------------------------------------------------------
#----------------------------------------------------------------

def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

def cover_check_rasterio(long,lati):
    for cover_value in coverIMG.sample([(long, lati)]): 
        checkedCover = cover_value
    return checkedCover

def cover_check(longitude, latitude, mes):
    
    current_month = mes    

    # Valor na escala: 1 pixel -> 0,00027 graus decimais (dentro das coordenadas)
    step = 0.00027                  
    long = longitude - (10*step)    
    lat = latitude - (10*step)    
    pixels = []

    # Escaneia a área de um quadrado de 300mx300m ao redor do ponto, para ser escaneado,
    # com finalidade de checar que tipos de vegatação temos ali
    while long < longitude + (10*step):
        while lat < latitude + (10*step):
            which_cover = cover_check_rasterio(long, lat)
            #print(which_cover)
            pixels.append(which_cover[0])
            lat += step
        long += step
        lat = latitude - (10*step)   

    # Checa qual é o tipo de vegetação mais comum na área escaneada e rotula a vegetação como tal 
    cover = most_frequent(pixels)

    return cover, current_month

#--------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------MAIN---------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    # Setados os contadores
    count = 0
    countBack = 0

    # Feita a leitura dos arquivos
    back = pd.read_csv(nomeBackup, sep = ';')
    file = pd.read_csv(nomeArquivo, sep = ';')

    tamBack = len(back['mes'].values.tolist())
    tamFile = len(file['mes'].values.tolist())

    # Condicional apenas para casos extremos no qual uma possível queda do programa ocorrer durante
    # o "salvamento" no Backup.
    if tamBack > tamFile:
        print('CSV principal corrompido. Iniciando-se a partir do Backup...')        
        coverCSV = pd.read_csv(nomeBackup, sep = ';')
    else:
        print('Iniciando-se a partir da última execução...')
        coverCSV = pd.read_csv(nomeArquivo, sep = ';')    

    # Coluna a ser criada
    column = ['vegetacao']

    # Condicional para checar se a coluna existe ou não
    for i in column:
        if i not in coverCSV.keys():
            coverCSV.insert(len(coverCSV.iloc[0]), i, math.nan)

    for i in range(len(coverCSV)):
        for j in range(len(column)):
            if pd.isna(coverCSV.loc[i, column[j]]):                
                count += 1
                countBack +=1
                
                # Checa que tipo de bioma temos naquela região
                coverCSV.loc[i, column[j]], month = cover_check(coverCSV['longitude'].iloc[i], coverCSV['latitude'].iloc[i], coverCSV['mes'].iloc[i])

                # Salva o arquivo a cada 2500 iterações
                if count > 2500:
                    coverCSV.to_csv(nomeArquivo, sep = ';', index = False)
                    count = 0
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(round(((i/tamFile)*100),2), '%', 'completo. Mês atual:', month)
                
                # Faz um backup reserva a cada 6666 iterações
                if countBack > 6666:
                    coverCSV.to_csv(nomeBackup, sep = ';', index = False)
                    countBack = 0
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Backup realizado.', round(((i/tamFile)*100),2), '%', 'completo. Mês atual:', month)
    
    # Salva as últimas linhas do CSV
    coverCSV.to_csv(nomeArquivo, sep = ';', index = False)
    print('Rotulagem completa!')