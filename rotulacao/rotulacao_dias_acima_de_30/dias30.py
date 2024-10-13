import pandas as pd
import math
import os
import numpy
from datetime import datetime, timedelta

path = '/home/saigg/Desktop/queimadas_datasets/train/2015.csv'
pathMethData = '/home/saigg/Desktop/queimadas_datasets/rotulacao/rotulacao_meteorology/meteorologyData/2015/2015meteorology.csv'
pathAnoPassado = '/home/saigg/Desktop/queimadas_datasets/rotulacao/rotulacao_meteorology/meteorologyData/2014/2014meteorology.csv'

methData = pd.read_csv(pathMethData, sep=';')
anopassado = pd.read_csv(pathAnoPassado, sep=';')

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

def calcula_dia_acima30(long, lat, year, month, day, past, temperatura):
    if past == 1:
        index = anopassado.loc[(anopassado['LAT'] == lat) & (anopassado['LON'] == long) & (anopassado['YEAR'] == year) & (anopassado['MO'] == month) & (anopassado['DY'] == day)]
    else:
        index = methData.loc[(methData['LAT'] == lat) & (methData['LON'] == long) & (methData['YEAR'] == year) & (methData['MO'] == month) & (methData['DY'] == day)]

    if temperatura == 'MAX':
        temp = index['T2M_MAX'].iloc[0]
    if temperatura == 'MED':
        temp = index['T2M'].iloc[0]

    if temp < 30:
        return 0
    else:
        data_atual = datetime(year, month, day)
        data_anterior = data_atual - timedelta(days = 1)
        newYear = data_anterior.year
        newMonth = data_anterior.month
        newDay = data_anterior.day
        if newYear == year:
            return 1 + calcula_dia_acima30(long, lat, newYear, newMonth, newDay, past, temperatura)
        else:
            return 1 + calcula_dia_acima30(long, lat, newYear, newMonth, newDay, 1, temperatura)

def find_meth_data(long, lat, year, month, day, max_or_med):    

    # Checa qual é o ponto mais próximo a se colar os dados metereológicos 
    lat, long = find_nearest_coords(lat, long)

    data_atual = datetime(year, month, day)
    data_atras = data_atual - timedelta(days = 1)

    if max_or_med == 0:
        if data_atras.year != data_atual.year:
            idx = anopassado.loc[(anopassado['LAT'] == lat) & (anopassado['LON'] == long) & (anopassado['YEAR'] == data_atras.year) & (anopassado['MO'] == data_atras.month) & (anopassado['DY'] == data_atras.day)]
            dias_max = calcula_dia_acima30(long, lat, data_atras.year, data_atras.month, data_atras.day, 1, 'MAX')
        else:
            idx = methData.loc[(methData['LAT'] == lat) & (methData['LON'] == long) & (methData['YEAR'] == data_atras.year) & (methData['MO'] == data_atras.month) & (methData['DY'] == data_atras.day)]
            dias_max = calcula_dia_acima30(long, lat, data_atras.year, data_atras.month, data_atras.day, 0, 'MAX')
        return dias_max
    else:
        if data_atras.year != data_atual.year:
            idx = anopassado.loc[(anopassado['LAT'] == lat) & (anopassado['LON'] == long) & (anopassado['YEAR'] == data_atras.year) & (anopassado['MO'] == data_atras.month) & (anopassado['DY'] == data_atras.day)]
            dias_med = calcula_dia_acima30(long, lat, data_atras.year, data_atras.month, data_atras.day, 1, 'MED')
        else:
            idx = methData.loc[(methData['LAT'] == lat) & (methData['LON'] == long) & (methData['YEAR'] == data_atras.year) & (methData['MO'] == data_atras.month) & (methData['DY'] == data_atras.day)]
            dias_med = calcula_dia_acima30(long, lat, data_atras.year, data_atras.month, data_atras.day, 0, 'MED')
        return dias_med

    precipitation = idx['PRECTOTCORR'].iloc[0]

    return dias_max, dias_med

print('Lendo csv...')

focosCSV = pd.read_csv(path, sep=';')


column = ['Num de dias acima de 30 graus (temp max)','Num de dias acima de 30 graus (temp media)']
    
# Condicional para checar se a coluna existe ou não
for i in column:
    if i not in focosCSV.keys():
        focosCSV.insert(len(focosCSV.iloc[0]), i, math.nan) 

count = 0
countBack = 0

for i in range(len(focosCSV)):
    os.system('cls' if os.name == 'nt' else 'clear') 
    print('{:.2f}% concluído'.format(i/len(focosCSV) * 100))
    count += 1
    for j in range(len(column)):
        if pd.isna(focosCSV.loc[i, column[j]]):

            try:
                focosCSV.loc[i, column[j]] = find_meth_data(focosCSV['Longitude'].iloc[i], focosCSV['Latitude'].iloc[i], focosCSV['Ano'].iloc[i], focosCSV['Mes'].iloc[i], focosCSV['Dia'].iloc[i], j)
            except:
                focosCSV.loc[i, column[j]] = 0

            if count % 5000 == 0 and count > 0:
                print('Salvando...')
                focosCSV.to_csv(path, sep=';', index = False)
                os.system('cls' if os.name == 'nt' else 'clear')
                print('Dados salvos')
                    

print('Salvando (FINAL)... Favor, não fechar este programa.')
focosCSV.to_csv(path, sep=';', index = False)
print('Dados meteorológicos preenchidos com sucesso!')