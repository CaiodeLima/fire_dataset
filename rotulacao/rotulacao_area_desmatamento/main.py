import pandas as pd
import math
import rasterio
from rasterio.plot import show
import os

#----------------------------------------------------------------
#---------------------VARIÁVEIS GLOBAIS--------------------------
nomeArquivo = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/AnosCSVs/2021.csv' # Sempre mudar o mês de acordo com o que está sendo rotulado
nomeBackup = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_area_desmatamento/Backup.csv'
desmatamentoTIFF_Path = r'/home/scholles/Desktop/CENSIPAM/Codigos/TIFFs/DesmatamentosTerraBrasilis/PDigital2000_2021_AMZ.tif'
desmatamentoTIFF = rasterio.open(desmatamentoTIFF_Path)
#----------------------------------------------------------------
#----------------------------------------------------------------

'''
d2007 = 06 ; d2008 = 07 ; d2009 = 08 ; d2010 = 09 ; d2011 = 10 ; d2012 = 11 ; d2013 = 12
d2014 = 13 ; d2015 = 14 ; d2016 = 15 ; d2017 = 16 ; d2018 = 17 ; d2019 = 27 ; d2020 = 29 ;
d2021 = 33
'''

# Valor dos Pixels a serem checados (desde 2007)
pixelsAnos = [6,7,8,9,10,11,12,13,14,15,16,17,27,29] 

def areaDesmatada_check(long,lati):
    for desmatamentoValue in desmatamentoTIFF.sample([(long, lati)]): 
        checkedArea = desmatamentoValue
    return checkedArea

def area_de_desmatamento_check(longitude, latitude):

    pixels = []
    
    # Valor na escala: 1 pixel -> 0,00027 graus decimais (dentro das coordenadas)
    step = 0.00027                  
    long = longitude - (10*step)    
    lat = latitude - (10*step)

    # Escaneia a área de um quadrado de 300mx300m ao redor do ponto, para ser escaneado,
    # com finalidade de checar se houveram queimadas naquele mês
    while long < longitude + (10*step):
        while lat < latitude + (10*step):
            which_month = areaDesmatada_check(long, lat)
            #print(which_month)
            pixels.append(which_month[0])
            lat += step
        long += step
        lat = latitude - (10*step)   

    # Checa por rastros de desmatamento na área. Basicamente se ele achar algum pixel referente à algum ano que
    # houve desmatamento na área, ele rotula como uma área propensa ao desmatamento
    for i in pixelsAnos:
        if pixels.count(i):
            areaDesmatada = 1
            break
        else:
            areaDesmatada = 0

    return areaDesmatada

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

    tamBack = len(back['dia'].values.tolist())
    tamFile = len(file['dia'].values.tolist())

    # Condicional apenas para casos extremos no qual uma possível queda do programa ocorrer durante
    # o "salvamento" no Backup.
    if tamBack > tamFile:
        print('CSV principal corrompido. Iniciando-se a partir do Backup...')        
        CSV = pd.read_csv(nomeBackup, sep = ';')
    else:
        print('Iniciando-se a partir da última execução...')
        CSV = pd.read_csv(nomeArquivo, sep = ';')    

    # Coluna a ser criada
    column = ['areaDesmatada']

    # Condicional para checar se a coluna existe ou não
    for i in column:
        if i not in CSV.keys():
            CSV.insert(len(CSV.iloc[0]), i, math.nan)

    for i in range(len(CSV)):
        for j in range(len(column)):
            if pd.isna(CSV.loc[i, column[j]]):                
                count += 1
                countBack +=1
                
                # Checa se tivemos algum tipo de desmatamento na região
                CSV.loc[i, column[j]] = area_de_desmatamento_check(CSV['longitude'].iloc[i], CSV['latitude'].iloc[i])

                if count > 2500:
                    CSV.to_csv(nomeArquivo, sep = ';', index = False)
                    count = 0
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(round(((i/tamFile)*100),2), '%', 'completo. Mês atual:', CSV['mes'].iloc[i])
                
                if countBack > 6666:
                    CSV.to_csv(nomeBackup, sep = ';', index = False)
                    countBack = 0
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Backup realizado.', round(((i/tamFile)*100),2), '%', 'completo. Mês atual:', CSV['mes'].iloc[i])
    
    CSV.to_csv(nomeArquivo, sep = ';', index = False)
    print('Rotulagem completa!')
