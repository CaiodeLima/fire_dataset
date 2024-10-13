import pandas as pd
import glob
import os

path = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_meteorology/temporal/'

concatenado = pd.DataFrame()
arquivos = glob.glob(path+'*.csv')
csv1 = arquivos.pop(0)
primeiro = pd.read_csv(csv1, sep=',')
for file in arquivos:
    aux = pd.read_csv(file)
    frame = [primeiro, aux]
    primeiro = pd.concat([primeiro, aux], axis=0)

primeiro.to_csv("/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_meteorology/temporal/juntado.csv", sep=";", index=False)