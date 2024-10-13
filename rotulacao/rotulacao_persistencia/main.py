import pandas as pd
import math
import os
import numpy
from datetime import datetime, timedelta

nomeTreino = '/home/saigg/Desktop/sandbox_scholles2/Datasets/classic/treino.csv'        # Sempre adequar ao path do seu computador
nomePredicao = '/home/saigg/Desktop/sandbox_scholles2/Datasets/classic/predicao.csv'

print('Lendo csvs...')

df1 = pd.read_csv(nomeTreino, sep=';')
df2 = pd.read_csv(nomePredicao, sep=';')

print('Concatenando...')

dataf = [df1,df2]
df = pd.concat(dataf)


def persistencia_queimada(originPoint, data_atras):
    km1 = 0.00898311
    km3 = 3*km1
    km5 = 5*km1
    km10 = 10*km1
    km15 = 15*km1
    p15km = 0
    p10km = 0
    p5km = 0
    p3km = 0
    p1km = 0    

    analysedDay = df.loc[(df['Dia'] == data_atras.day) & (df['Mes'] == data_atras.month) & (df['Ano'] == data_atras.year)]

    # separa o dataFrame nos focos que estão dentro do dia e da região e conta quantos são, se tiver algum então as variáveis contam um dia de persistência
    analysedRegion = analysedDay.loc[(analysedDay['Latitude'] >= originPoint[0] - km15) & (analysedDay['Latitude'] <= originPoint[0] + km15) & (analysedDay['Longitude'] >= originPoint[1] - km15) & (analysedDay['Longitude'] <= originPoint[1] + km15)]
    if len(analysedRegion) > 0:
        pers_list = analysedRegion['Persistencia em dias - Raio de 15km'].to_list()
        max_pers = max(pers_list)
        p15km = max_pers + 1

    analysedRegion = analysedRegion.loc[(analysedRegion['Latitude'] >= originPoint[0] - km10) & (analysedRegion['Latitude'] <= originPoint[0] + km10) & (analysedRegion['Longitude'] >= originPoint[1] - km10) & (analysedRegion['Longitude'] <= originPoint[1] + km10)]
    if len(analysedRegion) > 0:
        pers_list = analysedRegion['Persistencia em dias - Raio de 10km'].to_list()
        max_pers = max(pers_list)
        p10km = max_pers + 1

    analysedRegion = analysedRegion.loc[(analysedRegion['Latitude'] >= originPoint[0] - km5) & (analysedRegion['Latitude'] <= originPoint[0] + km5) & (analysedRegion['Longitude'] >= originPoint[1] - km5) & (analysedRegion['Longitude'] <= originPoint[1] + km5)]
    if len(analysedRegion) > 0:
        pers_list = analysedRegion['Persistencia em dias - Raio de 5km'].to_list()
        max_pers = max(pers_list)
        p5km = max_pers + 1

    analysedRegion = analysedRegion.loc[(analysedRegion['Latitude'] >= originPoint[0] - km3) & (analysedRegion['Latitude'] <= originPoint[0] + km3) & (analysedRegion['Longitude'] >= originPoint[1] - km3) & (analysedRegion['Longitude'] <= originPoint[1] + km3)]
    if len(analysedRegion) > 0:
        pers_list = analysedRegion['Persistencia em dias - Raio de 3km'].to_list()
        max_pers = max(pers_list)
        p3km = max_pers + 1

    analysedRegion = analysedRegion.loc[(analysedRegion['Latitude'] >= originPoint[0] - km1) & (analysedRegion['Latitude'] <= originPoint[0] + km1) & (analysedRegion['Longitude'] >= originPoint[1] - km1) & (analysedRegion['Longitude'] <= originPoint[1] + km1)]
    if len(analysedRegion) > 0:
        pers_list = analysedRegion['Persistencia em dias - Raio de 1km'].to_list()
        max_pers = max(pers_list)
        p1km = max_pers + 1

    return [p15km, p10km, p5km, p3km, p1km]

dia = df['Dia'].to_list()
mes = df['Mes'].to_list()
ano = df['Ano'].to_list()
originLatitude = df['Latitude'].to_list()
originLongitude = df['Longitude'].to_list()
persistencia1km = [0] * len(originLongitude)
persistencia3km = [0] * len(originLongitude)
persistencia5km = [0] * len(originLongitude)
persistencia10km = [0] * len(originLongitude)
persistencia15km = [0] * len(originLongitude)
df['Persistencia em dias - Raio de 1km'] = persistencia1km
df['Persistencia em dias - Raio de 3km'] = persistencia3km
df['Persistencia em dias - Raio de 5km'] = persistencia5km
df['Persistencia em dias - Raio de 10km'] = persistencia10km
df['Persistencia em dias - Raio de 15km'] = persistencia15km

for i in range(len(originLongitude)):
    os.system('cls' if os.name == 'nt' else 'clear') 
    print('{:.2f}% concluído'.format(i/len(originLatitude) * 100))

    # Ponto de origem a ser analizado
    originPoint = [originLatitude[i], originLongitude[i]]
    data_atual = datetime(ano[i], mes[i], dia[i])
    data_atras = data_atual - timedelta(days = 1)
    pers = persistencia_queimada(originPoint, data_atras)

    df.loc[i,'Persistencia em dias - Raio de 15km'] = pers[0]
    df.loc[i,'Persistencia em dias - Raio de 10km'] = pers[1]
    df.loc[i,'Persistencia em dias - Raio de 5km'] = pers[2]
    df.loc[i,'Persistencia em dias - Raio de 3km'] = pers[3]
    df.loc[i,'Persistencia em dias - Raio de 1km'] = pers[4]
    '''
    persistencia15km.append(pers[0])
    persistencia10km.append(pers[1])
    persistencia5km.append(pers[2])
    persistencia3km.append(pers[3])
    persistencia1km.append(pers[4])

df['Persistencia em dias - Raio de 1km'] = persistencia1km
df['Persistencia em dias - Raio de 3km'] = persistencia3km
df['Persistencia em dias - Raio de 5km'] = persistencia5km
df['Persistencia em dias - Raio de 10km'] = persistencia10km
df['Persistencia em dias - Raio de 15km'] = persistencia15km
'''

df2 = df.loc[(df['Ano'] == 2020)]
df = df.loc[(df['Ano'] < 2020)]

print('Salvando csvs...')
df.to_csv(nomeTreino, sep=';', index= False)
df2.to_csv(nomePredicao, sep=';', index= False)
