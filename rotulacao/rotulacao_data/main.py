import pandas as pd

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

if __name__ == '__main__':
    # Abre o arquivo desejado
    pathFile = '/home/scholles/Desktop/CENSIPAM/Codigos/sandbox_scholles/AnosCSVs/teste.csv'
    initialFile = pd.read_csv(pathFile, sep = ',') 

    # Modifica o arquivo para adicionar as datas de forma separada   
    fileRemovedCollumns = date_splitter(initialFile)
    fileRemovedCollumns.to_csv(pathFile, sep=';', index = False) 
