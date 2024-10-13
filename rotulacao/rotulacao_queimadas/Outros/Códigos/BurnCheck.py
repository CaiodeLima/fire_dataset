import rasterio
from rasterio.plot import show

# Função simples apenas para ver se houve e checar qual mês em que ocorreu aquela queimada
def checagem_mes(long,lati):
    fp = r'D:\\CENSIPAM\\Codigos\\censipam_rotulacao\\amazonia_2020_mapabiomas.tif'
    img = rasterio.open(fp) 
    for month_value in img.sample([(long, lati)]): 
        month = month_value
    return month

def burned_check(longitude, latitude, current_month):
    step = 0.00027                  # Valor na escala: 1 pixel -> 0,00027 graus decimais (dentro das coordenadas)
    long = longitude - (10*step)    
    lat = latitude - (10*step)    
    pixels = []                     # Lista de valores dos pixels escaneados       

    # Escaneia a área de um quadrado de 300mx300m ao redor do ponto, para ser escaneado,
    # com finalidade de checar se houveram queimadas naquele mês
    while long < longitude + (10*step):
        while lat < latitude + (10*step):
            month = checagem_mes(long, lat)
            pixels.append(month[0])
            lat += step
        long += step
        lat = latitude - (10*step)    

    # Condicionais para ver se houve algum pixel de queimada relativa ao mês que está sendo avaliado
    if pixels.count(current_month) > 0:
        burned = '1'
    else:
        burned = '0'

    return burned, pixels.count(current_month)