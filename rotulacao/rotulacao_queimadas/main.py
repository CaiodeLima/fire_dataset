import pandas as pd
import math
import rasterio
from rasterio.plot import show
import os

#----------------------------------------------------------------
#---------------------VARIÁVEIS GLOBAIS--------------------------
nomeArquivo = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles-main/rotulacao_queimadas/2017.csv' # Sempre mudar o mês de acordo com o que está sendo rotulado
nomeBackup = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles-main/rotulacao_queimadas/Backup.csv'
queimadasPath = r'/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles-main/rotulacao_queimadas/TIFFs/brasil_queimadas_2017_mapabiomas.tif'
queimadasIMG = rasterio.open(queimadasPath)
#----------------------------------------------------------------
#----------------------------------------------------------------

def month_check(long,lati):
    for month_value in queimadasIMG.sample([(long, lati)]): 
        checkedMonth = month_value
    return checkedMonth

def burned_check(longitude, latitude, mes):
    
    pixels = [] 
    current_month = mes
    
    # Valor na escala: 1 pixel -> 0,00027 graus decimais (dentro das coordenadas)
    step = 0.00027
    long = longitude - (10*step)    
    lat = latitude - (10*step)    
     

    # Escaneia a área de um quadrado de 300mx300m ao redor do ponto, para ser escaneado,
    # com finalidade de checar se houveram queimadas naquele mês
    while long < longitude + (10*step):
        while lat < latitude + (10*step):
            which_month = month_check(long, lat)
            #print(which_month)
            pixels.append(which_month[0])
            lat += step
        long += step
        lat = latitude - (10*step)   

    # Condicionais para ver se houve algum pixel de queimada relativa ao mês que está sendo avaliado
    if pixels.count(current_month) > 0:
        burned = '1'

    else:
        burned = '0'

    return burned, pixels.count(current_month), current_month

#--------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------MAIN---------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    # Setados os contadores
    count = 0
    countBack = 0

    # Faz a leitura dos arquivos
    back = pd.read_csv(nomeBackup, sep = ';')
    file = pd.read_csv(nomeArquivo, sep = ';')

    tamBack = len(back['mes'].values.tolist())
    tamFile = len(file['mes'].values.tolist())

    # Condicional apenas para casos extremos no qual uma possível queda do programa ocorrer durante
    # o "salvamento" no Backup.
    if tamBack > tamFile:
        print('CSV principal corrompido. Iniciando-se a partir do Backup...')        
        focosCSV = pd.read_csv(nomeBackup, sep = ';')
    else:
        print('Iniciando-se a partir da última execução...')
        focosCSV = pd.read_csv(nomeArquivo, sep = ';')    

    column = ['cicatriz']

    for i in column:
        if i not in focosCSV.keys():
            focosCSV.insert(len(focosCSV.iloc[0]), i, math.nan)

    for i in range(len(focosCSV)):
        for j in range(len(column)):
            if pd.isna(focosCSV.loc[i, column[j]]):                
                count += 1
                countBack +=1
                
                # Checa se tivemos alguma queimada naquele mês do ano, naquele local
                focosCSV.loc[i, column[j]], focosCSV.loc[i, 'cicatrizPixels'], month = burned_check(focosCSV['longitude'].iloc[i], focosCSV['latitude'].iloc[i], focosCSV['mes'].iloc[i])

                # Salva o arquivo a cada 2500 iterações
                if count > 2500:
                    focosCSV.to_csv(nomeArquivo, sep = ';', index = False)
                    count = 0
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(round(((i/tamFile)*100),2), '%', 'completo. Mês atual:', month)
                
                # Faz um backup reserva a cada 6666 iterações
                if countBack > 6666:
                    focosCSV.to_csv(nomeBackup, sep = ';', index = False)
                    countBack = 0
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Backup realizado.', round(((i/tamFile)*100),2), '%', 'completo. Mês atual:', month)
    
    focosCSV.to_csv(nomeArquivo, sep = ';', index = False)
    print('Rotulagem completa!')