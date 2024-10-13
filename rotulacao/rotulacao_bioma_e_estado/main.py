import pandas as pd

# ---------------- LEGENDAS ---------------- 

# Biomas:
# Amazonia = 1   Cerrado = 2   Pantanal = 3

# Estados:
# ACRE = 1   AMAZONAS = 2   RORAIMA = 3   PARA = 4   AMAPA = 5   MARANHAO = 6   RONDONIA = 7   MATO GROSSO = 8
# TOCANTINS = 9

# ------------------------------------------

def convert_Bio_State(csv):
    
    newFile = csv
    
    auxBioma = []
    auxEstado = []
    biomas = newFile['bioma']
    estados = newFile['estado']

    for i in range(len(biomas)):
        if biomas[i] == 'Amazonia':
            auxBioma.append(1)    
        if biomas[i] == 'Cerrado':
            auxBioma.append(2)
        if biomas[i] == 'Pantanal':
            auxBioma.append(3)

    for i in range(len(estados)):
        if estados[i] == 'ACRE':
            auxEstado.append(1)    
        if estados[i] == 'AMAZONAS':
            auxEstado.append(2)
        if estados[i] == 'RORAIMA':
            auxEstado.append(3)
        if estados[i] == 'PARA':
            auxEstado.append(4)
        if estados[i] == 'AMAPA':
            auxEstado.append(5)
        if estados[i] == 'MARANHAO':
            auxEstado.append(6)
        if estados[i] == 'RONDONIA':
            auxEstado.append(7)
        if estados[i] == 'MATO GROSSO':
            auxEstado.append(8)
        if estados[i] == 'TOCANTINS':
            auxEstado.append(9)

    newFile['bioma'] = auxBioma
    newFile['estado'] = auxEstado

    return newFile


if __name__ == '__main__':
    
    nomeArquivo = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/AnosCSVs/teste.csv'
    
    file = pd.read_csv(nomeArquivo, sep = ';')
    file = convert_Bio_State(file)
    file.to_csv(nomeArquivo, sep = ';', index = False)
