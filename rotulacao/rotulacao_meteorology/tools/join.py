import pandas as pd
import glob
import os

pathRAW_POWER = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_meteorology/temporal/'
pathFile = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_meteorology/meteorologyData/2019/2019precipit.csv'
file = pd.read_csv(pathFile, sep=';')

def arrumar():
    arquivos = glob.glob(pathRAW_POWER+'*.csv')    
    for file in arquivos:
        f = open(file, "r")
        linhas = f.readlines()
        f.close()

        nf = open(file, "w")
        newlinhas = linhas[20:]
        for line in newlinhas:
            nf.write(line)
        nf.close()

def juntarNovos():
    arquivos = glob.glob(pathRAW_POWER+'*.csv')
    csv1 = arquivos.pop(0)
    joinFile = pd.read_csv(csv1, sep=',')
    for file in arquivos:
        aux = pd.read_csv(file)
        joinFile = pd.concat([joinFile, aux], axis=0)

    return joinFile

def limpar():
    filelist = glob.glob(pathRAW_POWER+'*.csv')
    for f in filelist:
        os.remove(f)

if __name__ == '__main__':    

    arrumar()    
    newData = juntarNovos()
    newData.reset_index()
    limpar()

    file = pd.concat([file, newData], axis=0)
    file= file.drop_duplicates()

    file.to_csv(pathFile, sep=";", index=False)