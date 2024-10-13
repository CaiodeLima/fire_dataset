import pandas as pd

nomeArquivo = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_meteorology/meteorologyData/2020/2020precipit.csv'

arquivo = pd.read_csv(nomeArquivo, sep=';')

print(arquivo)

arquivo = arquivo.drop_duplicates()

print(arquivo)

arquivo.to_csv(nomeArquivo, sep = ';', index = False)