# LINK PARA A API DESCOBERTO NO LINK:
# https://firms.modaps.eosdis.nasa.gov/api/area/html/46a281e523f5af5de14f8054329934c3/VIIRS_NOAA20_NRT/-85,-57,-32,14/2/
# PARA PUXAR OS DADOS DA API, BASTA UTILIZAR O LINK:
# https://firms.modaps.eosdis.nasa.gov/api/area/csv/46a281e523f5af5de14f8054329934c3/VIIRS_NOAA20_NRT/-85,-57,-32,14/2/YEAR-MON-DAY

from datetime import datetime
import requests
import pandas as pd
import glob
import os

def generateFIRMS():
    todayDate = datetime.today().strftime('%Y-%m-%d')    
    folder = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_firms/API/'    
    
    # Faz a requisição dos dados através da API
    pathFIRMS1 = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_firms/API/temp1.csv'
    apiURL1 = f"{'https://firms.modaps.eosdis.nasa.gov/api/area/csv/46a281e523f5af5de14f8054329934c3/VIIRS_NOAA20_NRT/-85,-57,-32,14/2/'}{todayDate}"
    apiURL1 = requests.get(apiURL1)

    pathFIRMS2 = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_firms/API/temp2.csv'
    apiURL2 = f"{'https://firms.modaps.eosdis.nasa.gov/api/area/csv/46a281e523f5af5de14f8054329934c3/VIIRS_SNPP_NRT/-85,-57,-32,14/2/'}{todayDate}"
    apiURL2 = requests.get(apiURL2)

    # Salva o texto do site em um arquivo .csv temporário
    with open(pathFIRMS1, 'w+') as f:
        f.write(apiURL1.text)

    with open(pathFIRMS2, 'w+') as f:
        f.write(apiURL2.text)    

    # Lê esse .csv ne salva os valores em uma variável
    firms1 = pd.read_csv(pathFIRMS1, sep = ',')
    firms2 = pd.read_csv(pathFIRMS2, sep = ',')

    frames = [firms1, firms2]

    firms = pd.concat(frames)
    firms = firms.reset_index()

    # Remove o arquivo temporário do csv, visto que ele não possui mais utilidade
    remover = glob.glob(folder+'*.csv')
    for f in remover:
        os.remove(f)

    return firms

if __name__ == '__main__':
    csv = generateFIRMS()
    print(csv)