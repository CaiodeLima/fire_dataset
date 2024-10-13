import matplotlib.pyplot as plt
import pandas as pd
import glob
import os

path_dir = 'D:\\CENSIPAM\\Codigos\\sandbox_scholles\\rotulacao\\rotulacao_meteorology\\meteorologyData\\2021\\dez.csv'

combined_csv = pd.read_csv(path_dir, sep = ";")

x = [x for x in list(combined_csv['LON'])]
y = [y for y in list(combined_csv['LAT'])]

plt.scatter(x, y, s=1, c='red')
plt.show()