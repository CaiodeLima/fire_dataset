import pandas as pd
import os

CicatrizPequena = []
CicatrizGrande = []

# Limpa o terminal
os.system('cls' if os.name == 'nt' else 'clear')
acertos = 0

# Path dos CSVs de treino e de predição
path = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/treino/CSVs/treino.csv'

# Abre os CSVs de treino e de predição
csv = pd.read_csv(path, sep = ';')
cicatrizes = csv['cicatrizPixels'].values.tolist()

print('Iniciado o processamento de dados...')
for i in cicatrizes:
    if i == 0:
        CicatrizGrande.append(0)
        CicatrizPequena.append(0)
    elif i < 50:
        CicatrizPequena.append(1)
        CicatrizGrande.append(0)
    elif i >= 50:
        CicatrizGrande.append(1)
        CicatrizPequena.append(0)

csv['cicatrizPequena'] = CicatrizPequena
csv['cicatrizGrande'] = CicatrizGrande

print('Salvando os dados...')
csv.to_csv(path, sep = ';', index = False)