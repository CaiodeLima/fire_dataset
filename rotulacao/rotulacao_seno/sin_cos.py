import pandas as pd
import math
import os

def transformation(column):
  pi = 3.14159  
  max_value = column.max()
  sin_values = [math.sin((2*pi*x)/max_value) for x in list(column)]
  cos_values = [math.cos((2*pi*x)/max_value) for x in list(column)]
  return sin_values, cos_values

# Limpa o terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Path dos CSVs de treino e de predição
path = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles2/Datasets/classic/predicao.csv'

# Abre os CSVs de treino e de predição
csv = pd.read_csv(path, sep = ';')
mes = csv['Mes'].values
dia_ano = csv['Dia 365'].values

mes_sin, mes_cos = transformation(mes)
dia_ano_sin, dia_ano_cos = transformation(dia_ano)

csv['Mes Sin'] = mes_sin
csv['Mes Cos'] = mes_cos
csv['Dia 365 Sin'] = dia_ano_sin
csv['Dia 365 Cos'] = dia_ano_cos

print(csv)

print('Salvando os dados...')
csv.to_csv(path, sep = ';', index = False)