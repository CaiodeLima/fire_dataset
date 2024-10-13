import matplotlib.pyplot as plt
import pandas as pd

## Read fire data ( gathered from queimadas website)

file = "/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/treino/scikit/CSVs/predicao.csv"
data_pd = pd.read_csv(file, sep = ';')

pixCicatriz = data_pd['cicatrizPixels'].values.tolist()
cicatrizes = data_pd['cicatriz'].values.tolist()

RemoveZeros = data_pd['cicatrizPixels'].values.tolist()
RemoveZeros = [i for i in RemoveZeros if i != 0]

print('Número de focos de calor COM cicatrizes de queimada geradas:', cicatrizes.count(1))
print('Número de focos de calor SEM cicatrizes de queimada geradas:', cicatrizes.count(0))
print('Percentual de "geração de cicatrizes":', round(((1-(pixCicatriz.count(0)/len(pixCicatriz)))*100),2), '%')
print('Percentual de "não geração de cicatrizes":', round(((pixCicatriz.count(0)/len(pixCicatriz))*100),2), '%')

plt.hist(RemoveZeros, 400)
#plt.plot(data_pd['frp'], '.')
plt.title('2020\\nHistograma para o número de pixels detectados \\n de cicatrizes de queimada para cada foco de calor')
plt.show()
