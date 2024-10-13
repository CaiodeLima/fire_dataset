from collections import Counter
import pandas as pd
import rasterio
import math
import os

os.system('cls' if os.name == 'nt' else 'clear')

# VARIÁVEIS GLOBAIS PARA MANTER ABERTO OS TIFFs
desmatamentoTIFF_Path = r'/home/scholles/Desktop/CENSIPAM/Codigos/TIFFs/DesmatamentosTerraBrasilis/PDigital2000_2021_AMZ.tif'
desmatamentoTIFF = rasterio.open(desmatamentoTIFF_Path)

coverPath = r'/home/scholles/Desktop/CENSIPAM/Codigos/TIFFs/MAPBiomasCoverage/brasil_coverage_2019.tif'
coverIMG = rasterio.open(coverPath)

pathFile = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotualcao_geral/teste.csv'
saveFile = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotualcao_geral/testeModificado.csv'

count = 0
countBack = 0

# VARIÁVEIS GLOBAIS DE CSVS DE PESQUISA
pathMethData = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_distanciaTerraSol/distancias.csv'
methData = pd.read_csv(pathMethData, sep=';')

pathMeteorologyData = '/home/saigg/Desktop/queimadas_datasets/rotulacao/rotulacao_meteorology/meteorologyData/2015/2015meteorology.csv'
pathAnoPassado = '/home/saigg/Desktop/queimadas_datasets/rotulacao/rotulacao_meteorology/meteorologyData/2014/2014meteorology.csv'

# Valor dos Pixels a serem checados (desde 2007)
pixelsAnos = [6,7,8,9,10,11,12,13,14,15,16,17,27]
# LEGENDA:
#d2007 = 06 ; d2008 = 07 ; d2009 = 08 ; d2010 = 09 ; d2011 = 10 ; d2012 = 11 ; d2013 = 12
#d2014 = 13 ; d2015 = 14 ; d2016 = 15 ; d2017 = 16 ; d2018 = 17 ; d2019 = 27 ; d2020 = 29 ;
#d2021 = 33

def salva_csv(csv):
    count += 1
    if count % 5000 == 0 and count > 0:
            print('Salvando...')
            csv.to_csv(saveFile, sep=';', index = False)
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Dados salvos')

def find_nearest_coords(latitude, longitude):
    if latitude > 0:
        lat1 = int(latitude) - 0.25
        lat2 = int(latitude) + 0.25
        lat3 = int(latitude) + 0.75
        lat4 = int(latitude) + 1.25

        resLat1 = abs(latitude - lat1)
        resLat2 = abs(latitude - lat2)
        resLat3 = abs(latitude - lat3)
        resLat4 = abs(latitude - lat4)
        
        if resLat1 < resLat2 and resLat1 < resLat3 and resLat1 < resLat4:
            nearLat = lat1
        
        if resLat2 <= resLat1 and resLat2 <= resLat3 and resLat2 <= resLat4:
            nearLat = lat2
        
        if resLat3 < resLat2 and resLat3 < resLat2 and resLat3 < resLat4:
            nearLat = lat3    

        if resLat4 < resLat1 and resLat4 < resLat2 and resLat4 < resLat3:
            nearLat = lat3

    if latitude < 0:
        lat1 = int(latitude) + 0.25
        lat2 = int(latitude) - 0.25
        lat3 = int(latitude) - 0.75
        lat4 = int(latitude) - 1.25

        resLat1 = abs(latitude - lat1)
        resLat2 = abs(latitude - lat2)
        resLat3 = abs(latitude - lat3)
        resLat4 = abs(latitude - lat4)
        
        if resLat1 < resLat2 and resLat1 < resLat3 and resLat1 < resLat4:
            nearLat = lat1
        
        if resLat2 <= resLat1 and resLat2 <= resLat3 and resLat2 <= resLat4:
            nearLat = lat2
        
        if resLat3 < resLat2 and resLat3 < resLat2 and resLat3 < resLat4:
            nearLat = lat3    

        if resLat4 < resLat1 and resLat4 < resLat2 and resLat4 < resLat3:
            nearLat = lat3

    if longitude > 0:
        long1 = int(longitude) - 0.25
        long2 = int(longitude) + 0.25
        long3 = int(longitude) + 0.75
        long4 = int(longitude) + 1.25

        resLong1 = abs(longitude - long1)
        resLong2 = abs(longitude - long2)
        resLong3 = abs(longitude - long3)
        resLong4 = abs(longitude - long4)
        
        if resLong1 < resLong2 and resLong1 < resLong3 and resLong1 < resLong4:
            nearLong = long1
        
        if resLong2 <= resLong1 and resLong2 <= resLong3 and resLong2 <= resLong4:
            nearLong = long2
        
        if resLong3 < resLong2 and resLong3 < resLong2 and resLong3 < resLong4:
            nearLong = long3    

        if resLong4 < resLong1 and resLong4 < resLong2 and resLong4 < resLong3:
            nearLong = long3

    if longitude < 0:
        long1 = int(longitude) + 0.25
        long2 = int(longitude) - 0.25
        long3 = int(longitude) - 0.75
        long4 = int(longitude) - 1.25

        resLong1 = abs(longitude - long1)
        resLong2 = abs(longitude - long2)
        resLong3 = abs(longitude - long3)
        resLong4 = abs(longitude - long4)
        
        if resLong1 < resLong2 and resLong1 < resLong3 and resLong1 < resLong4:
            nearLong = long1
        
        if resLong2 <= resLong1 and resLong2 <= resLong3 and resLong2 <= resLong4:
            nearLong = long2
        
        if resLong3 < resLong2 and resLong3 < resLong2 and resLong3 < resLong4:
            nearLong = long3    

        if resLong4 < resLong1 and resLong4 < resLong2 and resLong4 < resLong3:
            nearLong = long3              
    
    return nearLat, nearLong

# ---------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------#
# --------------- FUNÇÃO DE SEPARAR DATA, ADICIONAR DIA DO ANO E ESTAÇÃO --------------- #
# ---------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------#
def date_splitter(csv):
    file = csv
    day = []
    seasons = []

    # Separa as datas em colunas, além de acrescer as o dia do ano (1 a 365)
    file['dia365'] = pd.DatetimeIndex(file['datahora']).dayofyear
    file['ano'] = pd.DatetimeIndex(file['datahora']).year
    file['mes'] = pd.DatetimeIndex(file['datahora']).month
    file['dia'] = pd.DatetimeIndex(file['datahora']).day
    file['hora'] = pd.DatetimeIndex(file['datahora']).hour

    # Remove as colunas desnecessárias
    removeCollumns = ['datahora','satelite','regiaoespecial','pais']
    remover = file.columns.values.tolist()    
    for i in removeCollumns:
        remover.remove(i)    
    file = file[remover]

    # Adiciona a estação do ano, de acordo com a data
    day = file['dia365'].values.tolist()
    for i in day:
        if i <= 80 or i >= 355:
            seasons.append(1)
        elif i > 80 and i <= 172:
            seasons.append(2)
        elif i > 172 and i < 264:
            seasons.append(3)
        else:
            seasons.append(4)
    file.insert(5, 'season', seasons)

    # Reordena as colunas, para deixar o arquivo mais organizado
    newOrder = ['dia365', 'dia', 'mes', 'ano', 'hora', 'season', 'estado', 'municipio', 'bioma', 'diasemchuva', 'precipitacao', 'riscofogo', 'latitude', 'longitude', 'frp']
    file = file[newOrder]

    return file


# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
# --------------- FUNÇÃO PARA NUMERIFICAR ESTADOS E BIOMAS --------------- #
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
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

# ------------------------------------------------------------ #
# ------------------------------------------------------------ #
# --------------- ROTULAÇÃO DE ÁREAS DESMATADA --------------- #
# ------------------------------------------------------------ #
# ------------------------------------------------------------ #
def areaDesmatada_check(long,lati):
    for desmatamentoValue in desmatamentoTIFF.sample([(long, lati)]): 
        checkedArea = desmatamentoValue
    return checkedArea

def area_de_desmatamento_check(longitude, latitude):

    pixels = []
    
    # Valor na escala: 1 pixel -> 0,00027 graus decimais (dentro das coordenadas)
    step = 0.00027                  
    long = longitude - (10*step)    
    lat = latitude - (10*step)

    # Escaneia a área de um quadrado de 300mx300m ao redor do ponto, para ser escaneado,
    # com finalidade de checar se houveram queimadas naquele mês
    while long < longitude + (10*step):
        while lat < latitude + (10*step):
            which_month = areaDesmatada_check(long, lat)
            #print(which_month)
            pixels.append(which_month[0])
            lat += step
        long += step
        lat = latitude - (10*step)   

    # Checa por rastros de desmatamento na área. Basicamente se ele achar algum pixel referente à algum ano que
    # houve desmatamento na área, ele rotula como uma área propensa ao desmatamento
    for i in pixelsAnos:
        if pixels.count(i):
            areaDesmatada = 1
            break
        else:
            areaDesmatada = 0

    return areaDesmatada

def areaDesmatada_main(csv):
    file = csv

    # Coluna a ser criada
    column = ['areaDesmatada']
    # Condicional para checar se a coluna existe ou não
    for i in column:
        if i not in file.keys():
            file.insert(len(file.iloc[0]), i, math.nan)

    for i in range(len(file)):
        for j in range(len(column)):
            if pd.isna(file.loc[i, column[j]]):                
                # Checa se tivemos algum tipo de desmatamento na região
                file.loc[i, column[j]] = area_de_desmatamento_check(file['longitude'].iloc[i], file['latitude'].iloc[i])
                salva_csv(file)
    return file


# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
# --------------- ROTULAÇÃO DA VEGETAÇÃO/COBERTURA DO SOLO --------------- #
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

def cover_check_rasterio(long,lati):
    for cover_value in coverIMG.sample([(long, lati)]): 
        checkedCover = cover_value
    return checkedCover

def cover_check(longitude, latitude):

    # Valor na escala: 1 pixel -> 0,00027 graus decimais (dentro das coordenadas)
    step = 0.00027                  
    long = longitude - (10*step)    
    lat = latitude - (10*step)    
    pixels = []

    # Escaneia a área de um quadrado de 300mx300m ao redor do ponto, para ser escaneado,
    # com finalidade de checar que tipos de vegatação temos ali
    while long < longitude + (10*step):
        while lat < latitude + (10*step):
            which_cover = cover_check_rasterio(long, lat)
            #print(which_cover)
            pixels.append(which_cover[0])
            lat += step
        long += step
        lat = latitude - (10*step)   

    # Checa qual é o tipo de vegetação mais comum na área escaneada e rotula a vegetação como tal 
    cover = most_frequent(pixels)

    return cover

def coverage_main(csv):
    file = csv

    # Coluna a ser criada
    column = ['Uso do solo']
    # Condicional para checar se a coluna existe ou não
    for i in column:
        if i not in file.keys():
            file.insert(len(file.iloc[0]), i, math.nan)

    for i in range(len(file)):
        for j in range(len(column)):
            if pd.isna(file.loc[i, column[j]]):
                # Checa que tipo de vegetação temos naquela região
                file.loc[i, column[j]]= cover_check(file['longitude'].iloc[i], file['latitude'].iloc[i])
                salva_csv(file)

    return file

# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
# --------------- ROTULAÇÃO DISTANCIA DA TERRA PARA O SOL --------------- #
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
pathDistances = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_distanciaTerraSol/distancias.csv'
distancesData = pd.read_csv(pathDistances, sep=';')
distancias = distancesData['distance'].tolist()

def find_distance(dia):
    # Pesquisa a distância da terra de acordo com o dia dado
    distance = distancias[dia-1]
    return distance
    

def distanceSun_main(csv):
    file = csv
    dias = file['dia365'].tolist()    
    distancias = []

    for i in dias:
        distancias.append(find_distance(i))

    file['distanciaSol'] = distancias

    return file

def transformation(column):
  pi = 3.14159  
  max_value = column.max()
  sin_values = [math.sin((2*pi*x)/max_value) for x in list(column)]
  cos_values = [math.cos((2*pi*x)/max_value) for x in list(column)]
  return sin_values, cos_values

def sin_cos(csv):
    mes = csv['Mes'].values
    dia_ano = csv['Dia 365'].values

    mes_sin, mes_cos = transformation(mes)
    dia_ano_sin, dia_ano_cos = transformation(dia_ano)

    csv['Mes Sin'] = mes_sin
    csv['Mes Cos'] = mes_cos
    csv['Dia 365 Sin'] = dia_ano_sin
    csv['Dia 365 Cos'] = dia_ano_cos

    return csv

# ------------------------------------ #
# ------------------------------------ #
# --------------- MAIN --------------- #
# ------------------------------------ #
# ------------------------------------ #
if __name__ == '__main__':
    # Abre o arquivo desejado
    csvFocos = pd.read_csv(pathFile, sep = ',')    

    # Modifica o arquivo para adicionar as datas de forma separada (Dia 365, Dia, Mes, Ano) 
    csvFocos = date_splitter(csvFocos)
    
    # Numerifica os Biomas e Estados para leitura do modelo treinado (Bioma, Estado)
    csvFocos = convert_Bio_State(csvFocos)

    # Rotula se aquela área já foi desmatada depois de 2007 (Area Desmatada)
    csvFocos = areaDesmatada_main(csvFocos)

    # Rotula se aquela área já foi desmatada depois de 2007 (Uso do solo)
    csvFocos = coverage_main(csvFocos)

    # Rotula a qual distância tava a terra naquele dia (Distancia do sol)
    csvFocos = distanceSun_main(csvFocos)

    # Transformação seno e cosseno dos valores para que eles se tornem cíclicos (Mes sin, Mes cos, Dia 365 sin, Dia 365 cos)
    csvFocos = sin_cos(csvFocos)

    csvFocos.to_csv(saveFile, sep = ';', index = False)

    
