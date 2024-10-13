import pandas as pd
import math
import os

os.system('cls' if os.name == 'nt' else 'clear')

#---------------------VARIÁVEIS GLOBAIS--------------------------
nomeArquivo = '/home/scholles/Desktop/CENSIPAM/Codigos/queimadas_datasets/test/2020.csv'        # Sempre adequar ao path do seu computador
nomeBackup = '/home/scholles/Desktop/CENSIPAM/Codigos/queimadas_datasets/test/Backup2020.csv'       # Sempre adequar ao path do seu computador
pathMethData = '/home/scholles/Desktop/CENSIPAM/Codigos/queimadas_datasets/rotulacao/rotulacao_meteorology/meteorologyData/2020/2020meteorology.csv'

methData = pd.read_csv(pathMethData, sep=';')
#----------------------------------------------------------------

# Série de condicionais para se saber qual é o ponto mais próximo que possui dados metereológicos coletados
def find_nearest_coords(latitude, longitude):
    if latitude > 0:
        lat1 = int(latitude) - 0.25
        lat2 = int(latitude) + 0.25
        lat3 = int(latitude) + 0.75
        lat4 = int(latitude) + 1.25

        resLat1 = abs(latitude - lat1)
        resLat2 = abs(latitude - lat2)
        resLat3 = abs(latitude - lat3)
        resLat4 = abs(latitude - lat4)
        
        if resLat1 < resLat2 and resLat1 < resLat3 and resLat1 < resLat4:
            nearLat = lat1
        
        if resLat2 <= resLat1 and resLat2 <= resLat3 and resLat2 <= resLat4:
            nearLat = lat2
        
        if resLat3 < resLat2 and resLat3 < resLat2 and resLat3 < resLat4:
            nearLat = lat3    

        if resLat4 < resLat1 and resLat4 < resLat2 and resLat4 < resLat3:
            nearLat = lat3

    if latitude < 0:
        lat1 = int(latitude) + 0.25
        lat2 = int(latitude) - 0.25
        lat3 = int(latitude) - 0.75
        lat4 = int(latitude) - 1.25

        resLat1 = abs(latitude - lat1)
        resLat2 = abs(latitude - lat2)
        resLat3 = abs(latitude - lat3)
        resLat4 = abs(latitude - lat4)
        
        if resLat1 < resLat2 and resLat1 < resLat3 and resLat1 < resLat4:
            nearLat = lat1
        
        if resLat2 <= resLat1 and resLat2 <= resLat3 and resLat2 <= resLat4:
            nearLat = lat2
        
        if resLat3 < resLat2 and resLat3 < resLat2 and resLat3 < resLat4:
            nearLat = lat3    

        if resLat4 < resLat1 and resLat4 < resLat2 and resLat4 < resLat3:
            nearLat = lat3

    if longitude > 0:
        long1 = int(longitude) - 0.25
        long2 = int(longitude) + 0.25
        long3 = int(longitude) + 0.75
        long4 = int(longitude) + 1.25

        resLong1 = abs(longitude - long1)
        resLong2 = abs(longitude - long2)
        resLong3 = abs(longitude - long3)
        resLong4 = abs(longitude - long4)
        
        if resLong1 < resLong2 and resLong1 < resLong3 and resLong1 < resLong4:
            nearLong = long1
        
        if resLong2 <= resLong1 and resLong2 <= resLong3 and resLong2 <= resLong4:
            nearLong = long2
        
        if resLong3 < resLong2 and resLong3 < resLong2 and resLong3 < resLong4:
            nearLong = long3    

        if resLong4 < resLong1 and resLong4 < resLong2 and resLong4 < resLong3:
            nearLong = long3

    if longitude < 0:
        long1 = int(longitude) + 0.25
        long2 = int(longitude) - 0.25
        long3 = int(longitude) - 0.75
        long4 = int(longitude) - 1.25

        resLong1 = abs(longitude - long1)
        resLong2 = abs(longitude - long2)
        resLong3 = abs(longitude - long3)
        resLong4 = abs(longitude - long4)
        
        if resLong1 < resLong2 and resLong1 < resLong3 and resLong1 < resLong4:
            nearLong = long1
        
        if resLong2 <= resLong1 and resLong2 <= resLong3 and resLong2 <= resLong4:
            nearLong = long2
        
        if resLong3 < resLong2 and resLong3 < resLong2 and resLong3 < resLong4:
            nearLong = long3    

        if resLong4 < resLong1 and resLong4 < resLong2 and resLong4 < resLong3:
            nearLong = long3              
    
    return nearLat, nearLong

def find_meth_data(long, lat, year, month, day):    

    # Checa qual é o ponto mais próximo a se colar os dados metereológicos 
    lat, long = find_nearest_coords(lat, long)

    # Pesquisa o tempo daquele dia, baseado nas coordenadas mais próximas + data
    idx = methData.loc[(methData['LAT'] == lat) & (methData['LON'] == long) & (methData['YEAR'] == year) & (methData['MO'] == month) & (methData['DY'] == day)]
    
    relativeHumidity = idx['RH2M'].iloc[0]
    specificHumidity = idx['QV2M'].iloc[0]
    tempMax = idx['T2M_MAX'].iloc[0]
    tempMin = idx['T2M_MIN'].iloc[0]

    return relativeHumidity, specificHumidity, tempMax, tempMin

#-------------------------------------------------------MAIN---------------------------------------------------------
if __name__ == '__main__':
    
    # Setagem das variáveis para contagem
    count = 0
    countBack = 0

    # Abre a partir do Backup, assim o risco de se perder dados depois de uma possível interrupção cai
    focosCSV = pd.read_csv(nomeBackup, sep=';')    

    back = pd.read_csv(nomeBackup, sep=';')
    file = pd.read_csv(nomeArquivo, sep=';')
    tamBack = len(back['dia'].values.tolist())
    tamFile = len(file['dia'].values.tolist())

    # Condicional apenas para casos extremos no qual uma possível queda do programa ocorrer durante
    # o "salvamento" no Backup.
    if tamBack > tamFile:
        print('CSV principal corrompido. Iniciando-se a partir do Backup...')        
        focosCSV = pd.read_csv(nomeBackup, sep=';')
    else:
        print('Iniciando-se a partir da última execução...')
        focosCSV = pd.read_csv(nomeArquivo, sep=';')

    # Coluna a ser criada
    column = ['umidaderelativa_real']
    
    # Condicional para checar se a coluna existe ou não
    for i in column:
        if i not in focosCSV.keys():
            focosCSV.insert(len(focosCSV.iloc[0]), i, math.nan)    

    for i in range(len(focosCSV)):
        for j in range(len(column)):
            if pd.isna(focosCSV.loc[i, column[j]]):
                count += 1
                countBack +=1
                try:
                    focosCSV.loc[i, column[j]], focosCSV.loc[i, 'umidadeEspecifica_real'], focosCSV.loc[i, 'temperaturaMaxima_real'], focosCSV.loc[i, 'temperaturaMinima_real'] = find_meth_data(focosCSV['longitude'].iloc[i], focosCSV['latitude'].iloc[i], focosCSV['ano'].iloc[i], focosCSV['mes'].iloc[i], focosCSV['dia'].iloc[i])
                except:
                    print(focosCSV['longitude'].iloc[i], focosCSV['latitude'].iloc[i], focosCSV['ano'].iloc[i], focosCSV['mes'].iloc[i], focosCSV['dia'].iloc[i])
                
                if count > 5000:
                    focosCSV.to_csv(nomeArquivo, sep=';', index = False)
                    count = 0
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('5000 dados salvos.', round(((i/tamFile)*100),2), '%', 'completo.')
                
                # Faz um backup a cada 11666 dados coletados
                if countBack > 11666:
                    focosCSV.to_csv(nomeBackup, sep=';', index = False) 
                    countBack = 0
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Backup realizado (Armazenados mais 11666 pontos).', round(((i/tamFile)*100),2), '%', 'completo.')
    
    # Salva o arquivo uma última vez, para garantir que nenhum dado seja perdido
    focosCSV.to_csv(nomeArquivo, sep=';', index = False)
    print('Dados meteorológicos preenchidos com sucesso!')                
