import pandas as pd
import glob
import os

path = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_meteorology/temporal/'

arquivos = glob.glob(path+'*.csv')
for file in arquivos:
    f = open(file, "r")
    linhas = f.readlines()
    f.close()

    nf = open(file, "w")
    newlinhas = linhas[20:]
    for line in newlinhas:
        nf.write(line)
    nf.close()