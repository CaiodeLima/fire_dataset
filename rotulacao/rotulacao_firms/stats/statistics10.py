import pandas as pd
import numpy as np
import math
import os

pathFile = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/AnosCSVs/2014.csv'
pathFIRMSData = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_firms/FIRMS_Files/fire_archive_2014.csv'

def insert_dia365(csv):
    fileCSV = csv
    fileCSV['dia365'] = pd.DatetimeIndex(fileCSV['acq_date']).dayofyear
    return fileCSV

if __name__ == '__main__':

    frp_mean = []
    frp_variance = []
    frp_std = []

    brightness_mean = []
    brightness_variance = []
    brightness_std = []

    bright_t31_mean = []
    bright_t31_variance = []
    bright_t31_std = []    

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

        frp = []
        brightness = []
        bright_t31 = []

        # Condicional para monitorar se o dia passou ou não
        if diaINPE[i] != diaAtual:
            diaAtual = diaINPE[i]
            dataframeDiario = FIRMSData.loc[(FIRMSData['dia365'] == diaAtual)]
            latFIRMS = dataframeDiario['latitude'].to_numpy()
            lonFIRMS = dataframeDiario['longitude'].to_numpy()
            frpFIRMS = dataframeDiario['frp'].to_numpy()
            brightnessFIRMS = dataframeDiario['brightness'].to_numpy()
            bright_t31FIRMS = dataframeDiario['bright_t31'].to_numpy()
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(diaAtual)

        for j in range(len(latFIRMS)):            
            
            # Calcula a distancia do foco de calor (INPE) com todos os outros pontos do FIRMS
            inpePoints = [latINPE[i], lonINPE[i]]
            firmsPoints = [latFIRMS[j], lonFIRMS[j]]
            distancia = math.dist(inpePoints, firmsPoints)

            #print(distancia)
            # Valor na escala: 1 grau decimal -> 111.11km
            # Neste caso, utilizamos um buffer de 5km
            if distancia <= 0.09:
                frp.append(frpFIRMS[j])
                brightness.append(brightnessFIRMS[j])
                bright_t31.append(bright_t31FIRMS[j])

        if len(frp) == 0:
            frp_mean.append(np.NaN)
            frp_variance.append(np.NaN)
            frp_std.append(np.NaN)

            brightness_mean.append(np.NaN)
            brightness_variance.append(np.NaN)
            brightness_std.append(np.NaN)

            bright_t31_mean.append(np.NaN)
            bright_t31_variance.append(np.NaN)
            bright_t31_std.append(np.NaN)

        else:
            frp_mean.append(np.mean(frp))
            frp_variance.append(np.var(frp))
            frp_std.append(np.std(frp))

            brightness_mean.append(np.mean(brightness))
            brightness_variance.append(np.var(brightness))
            brightness_std.append(np.std(brightness))

            bright_t31_mean.append(np.mean(bright_t31))
            bright_t31_variance.append(np.var(bright_t31))
            bright_t31_std.append(np.std(bright_t31))
    
    file['frp_mean_10'] = frp_mean
    file['frp_variance_10'] = frp_variance
    file['frp_std_10'] = frp_std

    file['brightness_mean_10'] = brightness_mean
    file['brightness_variance_10'] = brightness_variance
    file['brightness_std_10'] = brightness_std

    file['bright_t31_mean_10'] = bright_t31_mean
    file['bright_t31_variance_10'] = bright_t31_variance
    file['bright_t31_std_10'] = bright_t31_std    

    file.to_csv(pathFile, sep=';', index = False)
    print('Dados Rotulados!')