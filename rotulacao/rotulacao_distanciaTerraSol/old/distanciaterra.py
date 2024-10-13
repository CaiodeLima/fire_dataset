#rotulação distancia terra

import csv
import pandas as pd
import shutil,tempfile

temporario = open('predicao_completo.csv', 'w', newline = '')

arquivo = open('/home/saigg/Desktop/sandbox_scholles/treino/CSVs/predicao.csv', 'r')
distancias_csv = pd.read_csv('distancias.csv', sep = ';')
distancias = distancias_csv['distance'].values.tolist()

writer = csv.writer(temporario, delimiter = ';')
reader = csv.reader(arquivo, delimiter = ';')

i = 0 

for [dia365,dia,mes,ano,hora,season,estado,municipio,bioma,vegetacao,diasemchuva,precipitacao,riscofogo,latitude,longitude,frp,umidaderelativa,umidadeEspecifica,temperaturaMaxima,temperaturaMinima,areaDesmatada,cicatriz,cicatrizPixels] in reader:
    if i == 0:
        writer.writerow([dia365,dia,mes,ano,hora,season,estado,municipio,bioma,vegetacao,diasemchuva,precipitacao,riscofogo,latitude,longitude,frp,umidaderelativa,umidadeEspecifica,temperaturaMaxima,temperaturaMinima,areaDesmatada,'distanciaSol',cicatriz,cicatrizPixels])
        i = i + 1
    else:
        writer.writerow([int(dia365),int(dia),int(mes),int(ano),int(hora),int(season),estado,municipio,bioma,float(vegetacao),float(diasemchuva),float(precipitacao),float(riscofogo),float(latitude),float(longitude),frp,float(umidaderelativa),float(umidadeEspecifica),float(temperaturaMaxima),float(temperaturaMinima),float(areaDesmatada),distancias[int(dia365)-1],int(cicatriz),int(cicatrizPixels)])
arquivo.close()
temporario.close()


