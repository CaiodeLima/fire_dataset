import pandas as pd
import math
import os
import numpy

os.system('cls' if os.name == 'nt' else 'clear')

pathFile = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/AnosCSVs/2020.csv'
pathFIRMSData = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_firms/FIRMS_Files/fire_archive_2020.csv'

def insert_dia365(csv):
    fileCSV = csv
    fileCSV['dia365'] = pd.DatetimeIndex(fileCSV['acq_date']).dayofyear
    return fileCSV

if __name__ == '__main__':

    menorDistancia = 10000000000
    #frp = []
    brightness = []
    confidence = []
    bright_t31 = []

    # Faz a leitura dos arquivos
    file = pd.read_csv(pathFile, sep=';')
    FIRMSData = pd.read_csv(pathFIRMSData, sep=';')

    # Criação dos arrays para melhor performance do programa
    diaINPE = file['dia365'].to_numpy()
    latINPE = file['latitude'].to_numpy()
    lonINPE = file['longitude'].to_numpy()

    FIRMSData = insert_dia365(FIRMSData)

    diaAtual = 0
    for i in range(len(diaINPE)):
        
        # Condicional para monitorar se o dia passou ou não
        if diaINPE[i] != diaAtual:
            diaAtual = diaINPE[i]
            dataframeDiario = FIRMSData.loc[(FIRMSData['dia365'] == diaAtual)]
            latFIRMS = dataframeDiario['latitude'].to_numpy()
            lonFIRMS = dataframeDiario['longitude'].to_numpy()
            frpFIRMS = dataframeDiario['frp'].to_numpy()
            brightnessFIRMS = dataframeDiario['brightness'].to_numpy()
            confidenceFIRMS = dataframeDiario['confidence'].to_numpy()
            bright_t31FIRMS = dataframeDiario['bright_t31'].to_numpy()
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(diaAtual)

        for j in range(len(latFIRMS)):
            # Calcula a distancia do foco de calor (INPE) com todos os outros pontos do FIRMS
            distancia = math.sqrt((latINPE[i] - latFIRMS[j])**2 + (lonINPE[i] - lonFIRMS[j])**2)

            # Sempre mantém endereço do valor dos menores termos
            if distancia < menorDistancia:
                idx = j                
                menorDistancia = distancia
        
        #frp.append(frpFIRMS[idx])
        brightness.append(brightnessFIRMS[idx])
        confidence.append(confidenceFIRMS[idx])
        bright_t31.append(bright_t31FIRMS[idx])

        menorDistancia = 10000000000

    #file['frp'] = frp    
    file['confidence'] = confidence
    file['brightness'] = brightness
    file['bright_t31'] = bright_t31

    file.to_csv(pathFile, sep=';', index = False)
    print('Dados Rotulados!')