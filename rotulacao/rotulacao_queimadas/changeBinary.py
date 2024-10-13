import pickle
import pandas as pd
import os

newCicatriz = []
tamanho = 300

# Limpa o terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Path dos CSVs de treino e de predição
path = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/treino/CSVs/tamanho/predicao.csv'

# Abre os CSVs de treino e de predição
csv = pd.read_csv(path, sep = ';')
cicatrizes = csv['cicatrizPixels'].values.tolist()

print('Iniciado o processamento de dados...')
for i in cicatrizes:
    if i < tamanho:
        newCicatriz.append(0)
    elif i >= tamanho:
        newCicatriz.append(1)

csv['cicatriz300'] = newCicatriz

print('Salvando os dados...')
csv.to_csv(path, sep = ';', index = False)