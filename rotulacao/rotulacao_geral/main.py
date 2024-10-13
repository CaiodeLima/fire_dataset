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


# VARIÁVEIS GLOBAIS DE CSVS DE PESQUISA
pathMethData = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotulacao_distanciaTerraSol/distancias.csv'
methData = pd.read_csv(pathMethData, sep=';')

# Valor dos Pixels a serem checados (desde 2007)
pixelsAnos = [6,7,8,9,10,11,12,13,14,15,16,17,27]
# LEGENDA:
#d2007 = 06 ; d2008 = 07 ; d2009 = 08 ; d2010 = 09 ; d2011 = 10 ; d2012 = 11 ; d2013 = 12
#d2014 = 13 ; d2015 = 14 ; d2016 = 15 ; d2017 = 16 ; d2018 = 17 ; d2019 = 27 ; d2020 = 29 ;
#d2021 = 33

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
    column = ['vegetacao']
    # Condicional para checar se a coluna existe ou não
    for i in column:
        if i not in file.keys():
            file.insert(len(file.iloc[0]), i, math.nan)

    for i in range(len(file)):
        for j in range(len(column)):
            if pd.isna(file.loc[i, column[j]]):
                # Checa que tipo de bioma temos naquela região
                file.loc[i, column[j]]= cover_check(file['longitude'].iloc[i], file['latitude'].iloc[i])

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

# ------------------------------------ #
# ------------------------------------ #
# --------------- MAIN --------------- #
# ------------------------------------ #
# ------------------------------------ #
if __name__ == '__main__':
    # Abre o arquivo desejado
    pathFile = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotualcao_geral/teste.csv'
    saveFile = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/rotulacao/rotualcao_geral/testeModificado.csv'
    csvFocos = pd.read_csv(pathFile, sep = ',')    

    # Modifica o arquivo para adicionar as datas de forma separada   
    csvFocos = date_splitter(csvFocos)
    
    # Numerifica os Biomas e Estados para leitura do modelo treinado
    csvFocos = convert_Bio_State(csvFocos)

    # Rotula se aquela área já foi desmatada depois de 2007
    csvFocos = areaDesmatada_main(csvFocos)

    # Rotula se aquela área já foi desmatada depois de 2007
    csvFocos = coverage_main(csvFocos)

    # Rotula a qual distância tava a terra naquele dia
    csvFocos = distanceSun_main(csvFocos)

    csvFocos.to_csv(saveFile, sep = ';', index = False)

    
