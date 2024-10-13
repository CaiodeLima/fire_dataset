import math
import pandas as pd

if __name__ == '__main__':

    dia_sin = []
    mes_sin = []
    dia365_sin = []

    path = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/treino/CSVs/tamanho/predicao.csv'
    csv = pd.read_csv(path, sep = ';')

    dia = csv['dia'].to_numpy()
    mes = csv['mes'].to_numpy()
    dia365 = csv['dia365'].to_numpy()

    for i in range(len(dia)):
        diaseno = round((math.sin((math.pi/31)*dia[i])), 3)
        messeno = round((math.sin((math.pi/12)*mes[i])), 3)
        dia365seno = round((math.sin((math.pi/366)*dia365[i])), 4)
        dia_sin.append(diaseno)
        mes_sin.append(messeno)
        dia365_sin.append(dia365seno)

    csv['dia_sin'] = dia_sin
    csv['mes_sin'] = mes_sin
    csv['dia365_sin'] = dia365_sin

    csv.to_csv(path, sep=';', index = False)