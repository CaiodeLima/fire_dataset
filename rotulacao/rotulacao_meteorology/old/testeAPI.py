import pandas as pd
import math
import requests

long = -63.1413
lat = -2.8194

datetime = '2020/10/01 16:18:00'
date = datetime[0:10]   # Operações simples, apenas para deixar a data no formato no qual a API lê
year = date[0:4]
month = date[5:7]
day = date[8:10]

APIDateFormat = f"{year}{month}{day}" # Conversão para o formato de data da API
response = requests.get(f"{'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=RH2M,T2M_MAX,T2M_MIN&community=RE&longitude='}{long}{'&latitude='}{lat}{'&start='}{APIDateFormat}{'&end='}{APIDateFormat}{'&format=JSON'}").json()
RelativeHumidity = response['properties']['parameter']['RH2M'][APIDateFormat] # Coleta o valor da umidade relativa do ar
MaxTemp = response['properties']['parameter']['T2M_MAX'][APIDateFormat]       # Coleta o valor da temperatura máxima
MinTemp = response['properties']['parameter']['T2M_MIN'][APIDateFormat]       # Coleta o valor da temperatura minima

print(RelativeHumidity)
print(MaxTemp)
print(MinTemp)