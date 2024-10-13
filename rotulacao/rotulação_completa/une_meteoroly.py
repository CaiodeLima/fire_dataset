import pandas as pd
import math

for ano in range(2020,2021):
    path1 = f"{'/home/saigg/Desktop/queimadas_datasets/rotulacao/rotulacao_meteorology/meteorologyData/'}{ano}{'/'}{ano}{'meteorology.csv'}"
    path2 = f"{'/home/saigg/Desktop/queimadas_datasets/rotulacao/rotulacao_meteorology/meteorologyData/'}{ano}{'/'}{ano}{'precipit.csv'}"

    print('Lendo csvs')
    csv1 = pd.read_csv(path1, sep = ';')
    csv2 = pd.read_csv(path2, sep = ';')

    for key in csv2.keys():
        if key not in csv1.keys():
            csv1.insert(len(csv1.iloc[0]), key, math.nan)

    for i in range(len(csv1)):
        lat = csv1.loc[i,'LAT']
        lon = csv1.loc[i,'LON']
        day = csv1.loc[i,'DY']
        mon = csv1.loc[i,'MO']
        year = csv1.loc[i,'YEAR']

        linha = csv2.loc[(csv2['LAT'] == lat) & (csv2['LON'] == lon) & (csv2['DY'] == day) & (csv2['MO'] == mon) & (csv2['YEAR'] == year)]
        if len(linha) > 0:
            for key in ['PS','WS10M','WS10M_MAX','WS10M_MIN','WS10M_RANGE','WD10M','WS50M','WS50M_MAX','WS50M_MIN','WS50M_RANGE','WD50M','PRECTOTCORR']:
                csv1.loc[i,key] = linha[key].to_list()[0]

    print('Terminado ano',ano)

    path3 = f"{'/home/saigg/Desktop/queimadas_datasets/rotulacao/rotulacao_meteorology/meteorologyData/'}{ano}{'/'}{ano}{'complete.csv'}"
    csv1.to_csv(path3, sep = ';', index = False)
