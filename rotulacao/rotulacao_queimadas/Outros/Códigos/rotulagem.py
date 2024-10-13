import pandas as pd
import math
import BurnCheck

count = 0
month = 10

nomeArquivo = 'D:\\CENSIPAM\\Codigos\\censipam_rotulacao\\Outubro\\Outubro2020.csv'
nomeBackup = 'D:\\CENSIPAM\\Codigos\\censipam_rotulacao\\Outubro\\Backup.csv'

# Abre a partir do Backup, assim o risco de se perder dados depois de uma possível interrupção cai
cicatriz = pd.read_csv(nomeBackup, sep = ';')

column = ['cicatriz']

columnFunctions = [BurnCheck.burned_check]

for i in column:
    if i not in cicatriz.keys():
        cicatriz.insert(len(cicatriz.iloc[0]), i, math.nan)

for i in range(len(cicatriz)):
    for j in range(len(column)):
        if pd.isna(cicatriz.loc[i, column[j]]):
            cicatriz.loc[i, column[j]], cicatriz.loc[i, 'cicatrizPixels'] = columnFunctions[j](cicatriz['longitude'].iloc[i], cicatriz['latitude'].iloc[i], month)
            cicatriz.to_csv(nomeArquivo, sep = ';', index = False)

            count += 1
            if count > 150:
                cicatriz.to_csv(nomeBackup, sep = ';', index = False) 
                count = 0
                print('Backup feito')