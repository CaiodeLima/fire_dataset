import pandas as pd
import os

os.system('cls' if os.name == 'nt' else 'clear')

numberConfidence = []

pathFile = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/treino/CSVs/treino.csv'
file = pd.read_csv(pathFile, sep=';')

confidence = file['confidence'].to_numpy()

for i in confidence:
    if i == 'l':
        numberConfidence.append(0)
    if i == 'n':
        numberConfidence.append(1)
    if i == 'h':
        numberConfidence.append(2)

file['confidence'] = numberConfidence

file.to_csv(pathFile, sep=';', index = False)
