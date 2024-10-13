import pandas as pd
import math
import requests

#---------------------VARIÁVEIS GLOBAIS--------------------------
nomeArquivo = 'D:\\CENSIPAM\\Codigos\\censipam_umidade\\Outubro2020.csv' # Sempre adequar ao path do seu computador
nomeBackup = 'D:\\CENSIPAM\\Codigos\\censipam_umidade\\Backup.csv'       # Sempre adequar ao path do seu computador
#----------------------------------------------------------------

def check_Rhumidity(long, lat, datetime):    
    date = datetime[0:10]   # Operações simples, apenas para deixar a data no formato no qual a API lê
    year = date[6:10]
    month = date[3:5]
    day = date[0:2]

    APIDateFormat = f"{year}{month}{day}" # Conversão para o formato de data da API

    response = requests.get(f"{'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=RH2M,T2M_MAX,T2M_MIN&community=RE&longitude='}{long}{'&latitude='}{lat}{'&start='}{APIDateFormat}{'&end='}{APIDateFormat}{'&format=JSON'}").json()
    RelativeHumidity = response['properties']['parameter']['RH2M'][APIDateFormat] # Coleta o valor da umidade relativa do ar
    MaxTemp = response['properties']['parameter']['T2M_MAX'][APIDateFormat]       # Coleta o valor da temperatura máxima
    MinTemp = response['properties']['parameter']['T2M_MIN'][APIDateFormat]       # Coleta o valor da temperatura minima

    return RelativeHumidity, MinTemp, MaxTemp

#-------------------------------------------------------MAIN---------------------------------------------------------
if __name__ == '__main__':
    
    # Abre a partir do Backup, assim o risco de se perder dados depois de uma possível interrupção cai
    focosCSV = pd.read_csv(nomeBackup, sep = ';')
    
    back = pd.read_csv(nomeBackup, sep = ';')
    file = pd.read_csv(nomeArquivo, sep = ';')

    tamBack = len(back['datahora'].values.tolist())
    tamFile = len(file['datahora'].values.tolist())

    # Condicional apenas para casos extremos no qual uma possível queda do programa ocorrer durante
    # o "salvamento" no Backup.
    if tamFile > tamBack:
        print('Iniciado a partir do arquivo principal!')
        focosCSV = pd.read_csv(nomeArquivo, sep = ';')

    column = ['umidaderelativa']

    for i in column:
        if i not in focosCSV.keys():
            focosCSV.insert(len(focosCSV.iloc[0]), i, math.nan)

    count = 0
    countBack = 0

    for i in range(len(focosCSV)):
        for j in range(len(column)):
            if pd.isna(focosCSV.loc[i, column[j]]):
                focosCSV.loc[i, column[j]], focosCSV.loc[i, 'temperaturaMinima'], focosCSV.loc[i, 'temperaturaMaxima'] = check_Rhumidity(focosCSV['longitude'].iloc[i], focosCSV['latitude'].iloc[i], focosCSV['datahora'].iloc[i])
                count += 1
                countBack +=1
                
                # Salva a cada 10 dados coletados (se conseguirmos deixar o algoritmo mais rapido, podemos aumentar)
                if count > 10:
                    focosCSV.to_csv(nomeArquivo, sep = ';', index = False)
                    count = 0
                    print('10 dados salvos.')
                
                # Faz um backup a cada 55 dados coletados (se conseguirmos deixar o algoritmo mais rapido, podemos aumentar)
                if countBack > 55:
                    focosCSV.to_csv(nomeBackup, sep = ';', index = False) 
                    countBack = 0
                    print('Backup realizado (Armazenadas mais 55 pontos).')
    
    # Salva o arquivo uma última vez, para garantir que nenhum dado seja perdido
    focosCSV.to_csv(nomeArquivo, sep = ';', index = False)                